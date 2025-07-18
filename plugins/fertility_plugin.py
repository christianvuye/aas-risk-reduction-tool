"""Enhanced fertility and endocrine suppression modeling plugin."""

import streamlit as st
from typing import Dict, List, Any
from risk_model.plugin_loader import Plugin


class FertilityPlugin(Plugin):
    """Plugin for detailed fertility and endocrine suppression modeling."""
    
    def __init__(self):
        super().__init__()
        self.name = "Enhanced Fertility Model"
        self.version = "1.0.0"
        self.description = "Detailed fertility and endocrine suppression risk modeling with recovery tracking"
    
    def get_new_multipliers(self, user_inputs: Dict[str, Any]) -> Dict[str, List[float]]:
        """Calculate additional fertility-related risk multipliers.
        
        Args:
            user_inputs: User input data
            
        Returns:
            Dictionary mapping domain to list of multipliers
        """
        multipliers = {"endocrine": []}
        
        # Get fertility-specific inputs
        fertility_data = user_inputs.get("fertility_plugin", {})
        aas_regimen = user_inputs.get("aas_regimen", [])
        interventions = user_inputs.get("interventions", {})
        
        # Calculate cumulative suppression severity
        suppression_score = self._calculate_suppression_score(aas_regimen)
        
        # Age factor (recovery harder with age)
        age = user_inputs.get("demographics", {}).get("age", 30)
        age_penalty = 1.0 + max(0, (age - 25) * 0.02)  # 2% penalty per year over 25
        
        # Prior fertility baseline
        if fertility_data.get("baseline_fertility_issues", False):
            multipliers["endocrine"].append(1.3)
        
        # Cumulative suppression multiplier
        if suppression_score > 0:
            base_multiplier = 1.0 + (suppression_score * 0.15)  # 15% per severity point
            age_adjusted = base_multiplier * age_penalty
            multipliers["endocrine"].append(age_adjusted)
        
        # Recovery support interventions
        if interventions.get("hcg", False):
            multipliers["endocrine"].append(0.7)  # Stronger HCG benefit
        
        if interventions.get("serm_pct", False):
            multipliers["endocrine"].append(0.75)  # Enhanced SERM benefit
        
        # Fertility-specific protocols
        if fertility_data.get("fertility_protocol", False):
            multipliers["endocrine"].append(0.6)  # Comprehensive fertility protocol
        
        # Time off between cycles
        time_off_months = fertility_data.get("time_off_between_cycles", 0)
        if time_off_months >= 3:
            recovery_benefit = 0.95 - (time_off_months * 0.02)  # 2% benefit per month, min 0.85
            multipliers["endocrine"].append(max(0.85, recovery_benefit))
        
        # Lifestyle factors affecting fertility
        lifestyle = user_inputs.get("lifestyle", {})
        
        # Smoking penalty
        if lifestyle.get("smoking", False):
            multipliers["endocrine"].append(1.25)
        
        # Alcohol penalty
        alcohol_occasions = lifestyle.get("alcohol_occasions_month", 0)
        if alcohol_occasions > 8:  # More than 2 per week
            multipliers["endocrine"].append(1.15)
        
        # Sleep quality
        sleep_hours = lifestyle.get("sleep_hours", 7)
        if sleep_hours < 6:
            multipliers["endocrine"].append(1.2)
        elif sleep_hours >= 8:
            multipliers["endocrine"].append(0.95)
        
        # Stress management
        if fertility_data.get("stress_management", False):
            multipliers["endocrine"].append(0.9)
        
        return multipliers
    
    def additional_inputs(self) -> Dict[str, Any]:
        """Define additional input fields for fertility modeling.
        
        Returns:
            Dictionary of input field definitions for Streamlit
        """
        st.subheader("Enhanced Fertility Assessment")
        
        fertility_data = {}
        
        with st.expander("Baseline Fertility History", expanded=False):
            fertility_data["baseline_fertility_issues"] = st.checkbox(
                "Pre-existing fertility concerns",
                help="Any fertility issues before AAS use"
            )
            
            fertility_data["family_history_fertility"] = st.checkbox(
                "Family history of fertility issues"
            )
            
            fertility_data["previous_fertility_testing"] = st.selectbox(
                "Previous fertility testing",
                ["None", "Normal", "Abnormal", "Inconclusive"],
                index=0
            )
        
        with st.expander("Cycle History & Recovery", expanded=False):
            fertility_data["total_cycles_lifetime"] = st.number_input(
                "Total AAS cycles (lifetime)",
                min_value=0,
                max_value=100,
                value=0,
                step=1
            )
            
            fertility_data["time_off_between_cycles"] = st.number_input(
                "Average time off between cycles (months)",
                min_value=0,
                max_value=60,
                value=3,
                step=1
            )
            
            fertility_data["longest_continuous_use"] = st.number_input(
                "Longest continuous use (months)",
                min_value=0,
                max_value=120,
                value=0,
                step=1
            )
            
            fertility_data["recovery_time_last_cycle"] = st.number_input(
                "Recovery time after last cycle (months)",
                min_value=0,
                max_value=60,
                value=0,
                step=1,
                help="Time for natural testosterone to return"
            )
        
        with st.expander("Current Protocol & Interventions", expanded=False):
            fertility_data["fertility_protocol"] = st.checkbox(
                "Following comprehensive fertility protocol",
                help="Includes HCG, SERMs, monitoring, lifestyle optimization"
            )
            
            fertility_data["regular_monitoring"] = st.checkbox(
                "Regular hormone monitoring during cycle"
            )
            
            fertility_data["preemptive_hcg"] = st.checkbox(
                "Preemptive HCG during cycle (not just PCT)"
            )
            
            fertility_data["fertility_supplements"] = st.multiselect(
                "Fertility-supporting supplements",
                ["Clomiphene", "HMG", "FSH", "Vitamin D", "Zinc", "CoQ10", "NAC"],
                default=[]
            )
        
        with st.expander("Lifestyle Factors", expanded=False):
            fertility_data["stress_management"] = st.checkbox(
                "Active stress management practices",
                help="Meditation, therapy, stress reduction techniques"
            )
            
            fertility_data["heat_exposure"] = st.selectbox(
                "Regular heat exposure",
                ["None", "Occasional sauna/hot tub", "Frequent sauna/hot tub", "Occupational"],
                index=0,
                help="Heat can affect sperm production"
            )
            
            fertility_data["tight_clothing"] = st.checkbox(
                "Frequently wear tight clothing/underwear"
            )
            
            fertility_data["exercise_intensity"] = st.selectbox(
                "Exercise intensity",
                ["Light", "Moderate", "High", "Extreme"],
                index=2,
                help="Extreme exercise can affect fertility"
            )
        
        return {"fertility_plugin": fertility_data}
    
    def _calculate_suppression_score(self, aas_regimen: List[Dict]) -> float:
        """Calculate cumulative suppression severity score.
        
        Args:
            aas_regimen: List of AAS compound data
            
        Returns:
            Suppression severity score (0-10+)
        """
        score = 0.0
        
        # Suppression potency by compound class
        suppression_factors = {
            "testosterone": 1.0,
            "nandrolone": 1.3,
            "trenbolone": 2.0,
            "anadrol": 1.8,
            "dianabol": 1.5,
            "winstrol": 1.2,
            "anavar": 0.8,
            "primobolan": 0.9,
        }
        
        for compound_data in aas_regimen:
            compound = compound_data.get("compound", "").lower()
            weekly_mg = compound_data.get("weekly_mg", 0)
            duration = compound_data.get("duration_weeks", 0)
            
            # Find suppression factor
            suppression_factor = 1.0
            for compound_type, factor in suppression_factors.items():
                if compound_type in compound:
                    suppression_factor = factor
                    break
            
            # Calculate compound contribution
            # Base: 200mg test = 1 point, scaled by potency and duration
            dose_factor = weekly_mg / 200
            duration_factor = duration / 12  # 12 weeks = baseline
            
            compound_score = dose_factor * duration_factor * suppression_factor
            score += compound_score
        
        return score


# Register plugin function for dynamic loading
def register_plugin():
    """Register the fertility plugin.
    
    Returns:
        Plugin registration data
    """
    return {
        "name": "Enhanced Fertility Model",
        "version": "1.0.0",
        "description": "Detailed fertility and endocrine suppression risk modeling",
        "get_new_multipliers": FertilityPlugin().get_new_multipliers,
        "additional_inputs": FertilityPlugin().additional_inputs,
    }