"""Plugin loading and management system."""

import os
import importlib.util
import inspect
from typing import Dict, List, Any, Callable
from pathlib import Path


class Plugin:
    """Base plugin interface."""
    
    def __init__(self):
        self.name = "Base Plugin"
        self.version = "1.0.0"
        self.description = "Base plugin description"
    
    def get_new_multipliers(self, user_inputs: Dict[str, Any]) -> Dict[str, List[float]]:
        """Get additional risk multipliers from plugin.
        
        Args:
            user_inputs: User input data
            
        Returns:
            Dictionary mapping domain to list of multipliers
        """
        return {}
    
    def additional_inputs(self) -> Dict[str, Any]:
        """Define additional input fields needed by plugin.
        
        Returns:
            Dictionary of input field definitions
        """
        return {}


class PluginManager:
    """Manage loading and execution of plugins."""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = {}
        self.load_plugins()
    
    def load_plugins(self):
        """Load all plugins from plugin directory."""
        if not self.plugin_dir.exists():
            return
        
        for file_path in self.plugin_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
            
            try:
                self._load_plugin_from_file(file_path)
            except Exception as e:
                print(f"Failed to load plugin {file_path}: {e}")
    
    def _load_plugin_from_file(self, file_path: Path):
        """Load a single plugin from file.
        
        Args:
            file_path: Path to plugin file
        """
        # Load module
        spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, Plugin) and 
                    obj is not Plugin):
                    
                    # Instantiate plugin
                    plugin_instance = obj()
                    self.plugins[plugin_instance.name] = plugin_instance
                    
                    # Also check for register_plugin function
                elif name == "register_plugin" and callable(obj):
                    plugin_data = obj()
                    if isinstance(plugin_data, dict):
                        # Create plugin from dictionary
                        plugin = self._create_plugin_from_dict(plugin_data)
                        self.plugins[plugin.name] = plugin
    
    def _create_plugin_from_dict(self, plugin_data: Dict) -> Plugin:
        """Create a plugin instance from dictionary data.
        
        Args:
            plugin_data: Plugin data dictionary
            
        Returns:
            Plugin instance
        """
        class DynamicPlugin(Plugin):
            def __init__(self, data):
                super().__init__()
                self.name = data.get("name", "Unknown Plugin")
                self.version = data.get("version", "1.0.0")
                self.description = data.get("description", "")
                self._multipliers_func = data.get("get_new_multipliers", lambda x: {})
                self._inputs_func = data.get("additional_inputs", lambda: {})
            
            def get_new_multipliers(self, user_inputs):
                return self._multipliers_func(user_inputs)
            
            def additional_inputs(self):
                return self._inputs_func()
        
        return DynamicPlugin(plugin_data)
    
    def get_plugin(self, name: str) -> Plugin:
        """Get a specific plugin by name.
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance
        """
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """List all loaded plugins.
        
        Returns:
            List of plugin info dictionaries
        """
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
            }
            for plugin in self.plugins.values()
        ]
    
    def apply_plugin_multipliers(
        self, 
        user_inputs: Dict[str, Any], 
        base_multipliers: Dict[str, List[float]]
    ) -> Dict[str, List[float]]:
        """Apply all plugin multipliers to base multipliers.
        
        Args:
            user_inputs: User input data
            base_multipliers: Base multipliers by domain
            
        Returns:
            Updated multipliers including plugin contributions
        """
        combined = base_multipliers.copy()
        
        for plugin in self.plugins.values():
            plugin_multipliers = plugin.get_new_multipliers(user_inputs)
            
            # Merge multipliers
            for domain, multipliers in plugin_multipliers.items():
                if domain not in combined:
                    combined[domain] = []
                combined[domain].extend(multipliers)
        
        return combined
    
    def get_all_additional_inputs(self) -> Dict[str, Dict[str, Any]]:
        """Get additional input definitions from all plugins.
        
        Returns:
            Dictionary mapping plugin name to input definitions
        """
        all_inputs = {}
        
        for plugin in self.plugins.values():
            inputs = plugin.additional_inputs()
            if inputs:
                all_inputs[plugin.name] = inputs
        
        return all_inputs