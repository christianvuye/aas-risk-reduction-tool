"""Scenario management and comparison functionality."""

from typing import Dict, List, Any, Optional
import json
import uuid
from datetime import datetime

from .calculator import compute_domain_risks
from .multipliers import calculate_exposure_metrics, get_user_category


class ScenarioManager:
    """Manage multiple risk scenarios for comparison."""
    
    def __init__(self):
        self.scenarios = {}
        self.active_preset = "moderate"
    
    def create_scenario(
        self, 
        name: str, 
        user_data: Dict[str, Any],
        preset: Optional[str] = None
    ) -> str:
        """Create a new scenario.
        
        Args:
            name: Scenario name
            user_data: User input data
            preset: Risk preset (if different from active)
            
        Returns:
            Scenario ID
        """
        scenario_id = str(uuid.uuid4())
        preset = preset or self.active_preset
        
        # Calculate risks
        risks = compute_domain_risks(user_data, preset)
        
        # Calculate exposure metrics
        exposure_metrics = calculate_exposure_metrics(user_data)
        
        # Get category
        category = get_user_category(exposure_metrics, user_data)
        
        # Store scenario
        self.scenarios[scenario_id] = {
            "id": scenario_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "preset": preset,
            "user_data": user_data.copy(),
            "risks": risks,
            "exposure_metrics": exposure_metrics,
            "category": category,
            "interventions": self._extract_interventions(user_data),
        }
        
        return scenario_id
    
    def update_scenario(
        self, 
        scenario_id: str, 
        user_data: Dict[str, Any],
        name: Optional[str] = None
    ) -> None:
        """Update an existing scenario.
        
        Args:
            scenario_id: Scenario ID to update
            user_data: Updated user data
            name: Optional new name
        """
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.scenarios[scenario_id]
        if name:
            scenario["name"] = name
        
        # Recalculate
        scenario["user_data"] = user_data.copy()
        scenario["risks"] = compute_domain_risks(user_data, scenario["preset"])
        scenario["exposure_metrics"] = calculate_exposure_metrics(user_data)
        scenario["category"] = get_user_category(scenario["exposure_metrics"], user_data)
        scenario["interventions"] = self._extract_interventions(user_data)
        scenario["updated_at"] = datetime.now().isoformat()
    
    def clone_scenario(self, scenario_id: str, new_name: str) -> str:
        """Clone an existing scenario.
        
        Args:
            scenario_id: Scenario to clone
            new_name: Name for the clone
            
        Returns:
            New scenario ID
        """
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        original = self.scenarios[scenario_id]
        return self.create_scenario(
            new_name, 
            original["user_data"].copy(), 
            original["preset"]
        )
    
    def delete_scenario(self, scenario_id: str) -> None:
        """Delete a scenario.
        
        Args:
            scenario_id: Scenario to delete
        """
        if scenario_id in self.scenarios:
            del self.scenarios[scenario_id]
    
    def get_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Get a specific scenario.
        
        Args:
            scenario_id: Scenario ID
            
        Returns:
            Scenario data
        """
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        return self.scenarios[scenario_id]
    
    def list_scenarios(self) -> List[Dict[str, Any]]:
        """List all scenarios.
        
        Returns:
            List of scenario summaries
        """
        summaries = []
        for scenario in self.scenarios.values():
            summaries.append({
                "id": scenario["id"],
                "name": scenario["name"],
                "created_at": scenario["created_at"],
                "category": scenario["category"],
                "preset": scenario["preset"],
                "ascvd_risk": scenario["risks"]["ascvd"]["absolute_risk_pct"],
                "intervention_count": len(scenario["interventions"]),
            })
        return sorted(summaries, key=lambda x: x["created_at"], reverse=True)
    
    def compare_scenarios(self, scenario_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple scenarios.
        
        Args:
            scenario_ids: List of scenario IDs to compare
            
        Returns:
            Comparison data
        """
        if not scenario_ids:
            return {"scenarios": [], "domains": []}
        
        scenarios_data = []
        all_domains = set()
        
        for sid in scenario_ids:
            if sid in self.scenarios:
                scenario = self.scenarios[sid]
                scenarios_data.append(scenario)
                all_domains.update(scenario["risks"].keys())
        
        # Build comparison structure
        comparison = {
            "scenarios": [],
            "domains": sorted(all_domains),
        }
        
        for scenario in scenarios_data:
            scenario_summary = {
                "id": scenario["id"],
                "name": scenario["name"],
                "category": scenario["category"],
                "preset": scenario["preset"],
                "risks": {},
                "interventions": scenario["interventions"],
            }
            
            for domain in all_domains:
                if domain in scenario["risks"]:
                    risk_data = scenario["risks"][domain]
                    scenario_summary["risks"][domain] = {
                        "absolute_risk_pct": risk_data["absolute_risk_pct"],
                        "rr_vs_population": risk_data["rr_vs_population"],
                        "event_free_years": risk_data["event_free_years"],
                    }
            
            comparison["scenarios"].append(scenario_summary)
        
        return comparison
    
    def export_scenario(self, scenario_id: str, format: str = "json") -> str:
        """Export a scenario.
        
        Args:
            scenario_id: Scenario to export
            format: Export format (json, csv)
            
        Returns:
            Exported data as string
        """
        if scenario_id not in self.scenarios:
            raise ValueError(f"Scenario {scenario_id} not found")
        
        scenario = self.scenarios[scenario_id]
        
        if format == "json":
            return json.dumps(scenario, indent=2)
        
        elif format == "csv":
            # Build CSV format
            lines = ["Domain,Absolute Risk %,RR vs Population,RR vs Physio,Event Free Years"]
            
            for domain, risk_data in scenario["risks"].items():
                line = f"{domain},{risk_data['absolute_risk_pct']:.2f},"
                line += f"{risk_data['rr_vs_population']:.2f},"
                line += f"{risk_data['rr_vs_physio']:.2f},"
                line += f"{risk_data['event_free_years']:.1f}"
                lines.append(line)
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _extract_interventions(self, user_data: Dict) -> List[str]:
        """Extract active interventions from user data.
        
        Args:
            user_data: User input data
            
        Returns:
            List of active intervention names
        """
        interventions = []
        intervention_data = user_data.get("interventions", {})
        
        # Check each intervention type
        if intervention_data.get("eliminate_orals"):
            interventions.append("Eliminate orals")
        
        if intervention_data.get("replace_heavy_mild"):
            interventions.append("Replace heavy with mild")
        
        if intervention_data.get("vo2max_improvement", 0) > 0:
            interventions.append(f"VO2max +{intervention_data['vo2max_improvement']}")
        
        if intervention_data.get("bodyfat_reduction", 0) > 0:
            interventions.append(f"Body fat -{intervention_data['bodyfat_reduction']}%")
        
        statin = intervention_data.get("statin_intensity", "none")
        if statin != "none":
            interventions.append(f"{statin.capitalize()} statin")
        
        # Medications
        med_mapping = {
            "ezetimibe": "Ezetimibe",
            "pcsk9": "PCSK9 inhibitor",
            "omega3": "Omega-3",
            "glp1_agonist": "GLP-1/GIP agonist",
            "metformin": "Metformin",
            "pde5_daily": "PDE5 daily",
            "finasteride": "Finasteride/Dutasteride",
            "serm_pct": "SERM PCT",
            "hcg": "HCG support",
        }
        
        for key, label in med_mapping.items():
            if intervention_data.get(key):
                interventions.append(label)
        
        return interventions