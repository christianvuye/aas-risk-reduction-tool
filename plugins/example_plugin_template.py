"""Example plugin template for AAS Risk Reduction Tool."""

import streamlit as st
from typing import Dict, List, Any
from risk_model.plugin_loader import Plugin


class ExamplePlugin(Plugin):
    """Example plugin template showing the plugin interface."""
    
    def __init__(self):
        super().__init__()
        self.name = "Example Plugin"
        self.version = "1.0.0"
        self.description = "Template plugin showing how to extend the risk model"
    
    def get_new_multipliers(self, user_inputs: Dict[str, Any]) -> Dict[str, List[float]]:
        """Calculate additional risk multipliers based on plugin logic.
        
        Args:
            user_inputs: Complete user input data
            
        Returns:
            Dictionary mapping domain names to lists of multipliers
        """
        multipliers = {
            "ascvd": [],
            "hf": [],
            "thrombosis": [],
            "hepatic": [],
            "renal": [],
            "neuro": [],
            "diabetes": [],
            "dementia": [],
            "endocrine": [],
            "dermatologic": [],
            "cancer_colorectal": [],
            "cancer_prostate": [],
        }
        
        # Example: Add custom risk factors
        plugin_data = user_inputs.get("example_plugin", {})
        
        # Example custom factor
        if plugin_data.get("custom_risk_factor", False):
            multipliers["ascvd"].append(1.1)  # 10% increase in ASCVD risk
            multipliers["hf"].append(1.05)    # 5% increase in HF risk
        
        # Example protective factor
        if plugin_data.get("custom_protection", False):
            multipliers["diabetes"].append(0.9)  # 10% reduction in diabetes risk
        
        # Example dose-response relationship
        custom_exposure = plugin_data.get("custom_exposure_level", 0)
        if custom_exposure > 0:
            # Calculate risk multiplier based on exposure level
            exposure_multiplier = 1.0 + (custom_exposure * 0.02)  # 2% per unit
            multipliers["hepatic"].append(exposure_multiplier)
        
        return multipliers
    
    def additional_inputs(self) -> Dict[str, Any]:
        """Define additional input fields for the plugin.
        
        Returns:
            Dictionary containing the collected plugin-specific data
        """
        st.subheader("Example Plugin Inputs")
        
        plugin_data = {}
        
        with st.expander("Custom Risk Factors", expanded=False):
            plugin_data["custom_risk_factor"] = st.checkbox(
                "Custom Risk Factor",
                help="Example checkbox for a custom risk factor"
            )
            
            plugin_data["custom_protection"] = st.checkbox(
                "Custom Protective Factor",
                help="Example checkbox for a protective factor"
            )
            
            plugin_data["custom_exposure_level"] = st.slider(
                "Custom Exposure Level",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                help="Example slider for exposure level"
            )
        
        with st.expander("Additional Metrics", expanded=False):
            plugin_data["custom_biomarker"] = st.number_input(
                "Custom Biomarker Level",
                min_value=0.0,
                max_value=1000.0,
                value=100.0,
                step=1.0,
                help="Example numeric input for a biomarker"
            )
            
            plugin_data["risk_category"] = st.selectbox(
                "Risk Category",
                ["Low", "Medium", "High"],
                index=1,
                help="Example categorical risk input"
            )
            
            plugin_data["intervention_history"] = st.multiselect(
                "Previous Interventions",
                ["Intervention A", "Intervention B", "Intervention C"],
                default=[],
                help="Example multi-select for intervention history"
            )
        
        return {"example_plugin": plugin_data}


# Alternative registration method using function
def register_plugin():
    """Register the plugin using function-based approach.
    
    Returns:
        Dictionary with plugin registration information
    """
    
    def get_multipliers(user_inputs):
        """Plugin multiplier calculation function."""
        multipliers = {"ascvd": [], "diabetes": []}
        
        plugin_data = user_inputs.get("example_plugin_functional", {})
        
        # Example: Simple risk modification
        if plugin_data.get("high_risk_behavior", False):
            multipliers["ascvd"].append(1.15)
        
        if plugin_data.get("protective_behavior", False):
            multipliers["diabetes"].append(0.85)
        
        return multipliers
    
    def additional_inputs():
        """Plugin input collection function."""
        st.subheader("Functional Plugin Example")
        
        plugin_data = {}
        
        plugin_data["high_risk_behavior"] = st.checkbox(
            "High Risk Behavior",
            help="Example high-risk behavior factor"
        )
        
        plugin_data["protective_behavior"] = st.checkbox(
            "Protective Behavior",
            help="Example protective behavior factor"
        )
        
        return {"example_plugin_functional": plugin_data}
    
    return {
        "name": "Functional Example Plugin",
        "version": "1.0.0", 
        "description": "Example plugin using functional registration approach",
        "get_new_multipliers": get_multipliers,
        "additional_inputs": additional_inputs,
    }


# Instructions for plugin developers:
"""
To create a new plugin:

1. Create a new .py file in the plugins/ directory
2. Choose either class-based or function-based approach:

CLASS-BASED APPROACH:
- Create a class inheriting from Plugin
- Implement get_new_multipliers() and additional_inputs() methods
- Instantiate and use the class

FUNCTION-BASED APPROACH:
- Create a register_plugin() function that returns a dictionary
- Include get_new_multipliers and additional_inputs functions
- The plugin loader will automatically discover and load your plugin

MULTIPLIER GUIDELINES:
- Return multipliers as floats where >1.0 increases risk, <1.0 decreases risk
- Use domain names from baseline_constants.py
- Multiple multipliers for the same domain will be multiplied together
- Consider reasonable effect sizes (typically 0.8-1.3 range)

INPUT GUIDELINES:  
- Use Streamlit widgets for user input
- Group related inputs in expandable sections
- Provide helpful tooltips and descriptions
- Return data in a nested dictionary with your plugin name as key

TESTING:
- Test your plugin with various input combinations
- Verify multipliers are applied correctly
- Check that inputs are preserved in scenarios
"""