"""Risk multiplier calculation and management."""

import yaml
from typing import Dict, List, Any, Tuple
from pathlib import Path

from .baseline_constants import PHYSIOLOGIC_THRESHOLD_MG, PROTECTIVE_FACTOR_ADJUSTMENTS
from .potency_table import (
    calculate_weekly_te, is_oral_17aa, is_dht_derived, 
    is_heavy_compound, is_mild_compound
)


def load_preset_coefficients(preset_name: str) -> Dict[str, Any]:
    """Load coefficient preset from YAML file.
    
    Args:
        preset_name: Name of preset (conservative, moderate, aggressive)
        
    Returns:
        Dictionary of coefficient mappings
    """
    preset_path = Path(__file__).parent.parent / "presets" / f"coefficients_{preset_name.lower()}.yml"
    
    with open(preset_path, 'r') as f:
        return yaml.safe_load(f)


def transform_coefficients(base_coeffs: Dict, transformation: str) -> Dict:
    """Transform base coefficients to create conservative/aggressive variants.
    
    Args:
        base_coeffs: Base coefficient dictionary
        transformation: 'conservative' or 'aggressive'
        
    Returns:
        Transformed coefficients
    """
    if transformation == "conservative":
        # Dampen by 50% of distance from 1
        factor = 0.5
    elif transformation == "aggressive":
        # Exaggerate by 30% of distance from 1
        factor = 1.3
    else:
        return base_coeffs
    
    transformed = {}
    for key, value in base_coeffs.items():
        if isinstance(value, dict):
            transformed[key] = {}
            for domain, mult in value.items():
                if mult > 1:
                    transformed[key][domain] = 1 + (mult - 1) * factor
                else:
                    transformed[key][domain] = 1 - (1 - mult) * factor
        else:
            transformed[key] = value
    
    return transformed


def calculate_exposure_metrics(user_data: Dict) -> Dict[str, float]:
    """Calculate exposure metrics from user AAS regimen.
    
    Args:
        user_data: User input data including AAS regimen
        
    Returns:
        Dictionary of exposure metrics
    """
    metrics = {
        "weekly_te_total": 0,
        "max_weekly_te": 0,
        "weeks_supra_per_year": 0,
        "recovery_ratio": 1.0,
        "oral_17aa_weeks": 0,
        "oral_17aa_high_dose_weeks": 0,
        "has_heavy_compounds": False,
        "has_dht_compounds": False,
        "longest_continuous_weeks": 0,
    }
    
    # Process AAS regimen
    regimen = user_data.get("aas_regimen", [])
    if not regimen:
        return metrics
    
    # Calculate weekly timeline (52 weeks)
    weekly_te = [0] * 52
    weekly_orals = [False] * 52
    weekly_oral_dose = [0] * 52
    
    for compound_data in regimen:
        compound = compound_data["compound"]
        weekly_mg = compound_data["weekly_mg"]
        start_week = compound_data.get("start_week", 1) - 1  # Convert to 0-based
        duration = compound_data["duration_weeks"]
        is_oral = compound_data.get("is_oral", False)
        
        # Calculate TE
        te = calculate_weekly_te(compound, weekly_mg)
        
        # Update heavy/DHT flags
        if is_heavy_compound(compound):
            metrics["has_heavy_compounds"] = True
        if is_dht_derived(compound):
            metrics["has_dht_compounds"] = True
        
        # Fill timeline
        for week in range(start_week, min(start_week + duration, 52)):
            if not is_oral:
                weekly_te[week] += te
            else:
                weekly_orals[week] = True
                weekly_oral_dose[week] += weekly_mg
                if is_oral_17aa(compound):
                    metrics["oral_17aa_weeks"] += 1/len([c for c in regimen if c.get("is_oral")])
                    if weekly_mg > 50:  # High dose threshold
                        metrics["oral_17aa_high_dose_weeks"] += 1/len([c for c in regimen if c.get("is_oral")])
    
    # Calculate metrics
    metrics["weekly_te_total"] = sum(weekly_te) / sum(1 for x in weekly_te if x > 0) if any(weekly_te) else 0
    metrics["max_weekly_te"] = max(weekly_te)
    metrics["weeks_supra_per_year"] = sum(1 for te in weekly_te if te > PHYSIOLOGIC_THRESHOLD_MG)
    
    # Recovery ratio
    weeks_above = sum(1 for te in weekly_te if te > PHYSIOLOGIC_THRESHOLD_MG)
    weeks_at_or_below = 52 - weeks_above
    if weeks_above > 0:
        metrics["recovery_ratio"] = weeks_at_or_below / weeks_above
    
    # Longest continuous supra-physiologic period
    current_streak = 0
    max_streak = 0
    for te in weekly_te:
        if te > PHYSIOLOGIC_THRESHOLD_MG:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    metrics["longest_continuous_weeks"] = max_streak
    
    return metrics


def estimate_hdl_nadir(user_data: Dict, exposure_metrics: Dict) -> float:
    """Estimate HDL nadir based on exposure.
    
    Args:
        user_data: User input data
        exposure_metrics: Calculated exposure metrics
        
    Returns:
        Estimated HDL nadir
    """
    baseline_hdl = user_data.get("labs", {}).get("hdl", 50)
    
    # Base drop proportional to supra-physiologic exposure
    wte_above = max(0, exposure_metrics["weekly_te_total"] - PHYSIOLOGIC_THRESHOLD_MG)
    base_drop_fraction = min(0.5, wte_above / 300)  # Max 50% drop at 300mg above threshold
    
    # Additional drop for orals
    oral_factor = 1.0
    if exposure_metrics["oral_17aa_weeks"] > 0:
        oral_factor = 1.2
        if exposure_metrics["oral_17aa_high_dose_weeks"] > 4:
            oral_factor = 1.5
    
    # Calculate drop
    hdl_drop = baseline_hdl * base_drop_fraction * oral_factor
    
    # Additional 10 mg/dL for high-dose orals
    if exposure_metrics["oral_17aa_high_dose_weeks"] > 8:
        hdl_drop += 10
    
    return max(15, baseline_hdl - hdl_drop)  # Floor at 15 mg/dL


def get_user_category(exposure_metrics: Dict, user_data: Dict) -> str:
    """Determine user risk category.
    
    Args:
        exposure_metrics: Calculated exposure metrics
        user_data: User input data
        
    Returns:
        Category string: 'physiologic', 'moderate', or 'high_risk'
    """
    wte = exposure_metrics["weekly_te_total"]
    oral_weeks = exposure_metrics["oral_17aa_weeks"]
    recovery_ratio = exposure_metrics["recovery_ratio"]
    hct = user_data.get("labs", {}).get("hematocrit", 45)
    
    # Physiologic TRT
    if wte <= PHYSIOLOGIC_THRESHOLD_MG and oral_weeks == 0:
        return "physiologic"
    
    # High risk criteria
    if (wte > 300 or oral_weeks > 8 or recovery_ratio < 0.75 or hct > 54):
        return "high_risk"
    
    # Otherwise moderate
    return "moderate"


def collect_active_multipliers(user_data: Dict, coefficients: Dict) -> Dict[str, List[float]]:
    """Collect all active multipliers for each domain based on user data.
    
    Args:
        user_data: User input data
        coefficients: Loaded coefficient preset
        
    Returns:
        Dictionary mapping domain to list of applicable multipliers
    """
    exposure_metrics = calculate_exposure_metrics(user_data)
    hdl_nadir = estimate_hdl_nadir(user_data, exposure_metrics)
    labs = user_data.get("labs", {})
    lifestyle = user_data.get("lifestyle", {})
    interventions = user_data.get("interventions", {})
    
    # Initialize multipliers dict
    multipliers = {domain: [] for domain in coefficients.get("physiologic_t_base", {}).keys()}
    
    # Helper function to apply multiplier
    def apply_multiplier(key: str, condition: bool = True):
        if condition and key in coefficients:
            mult_dict = coefficients[key]
            for domain, value in mult_dict.items():
                if domain in multipliers:
                    multipliers[domain].append(value)
    
    # Exposure-based multipliers
    if exposure_metrics["weekly_te_total"] > PHYSIOLOGIC_THRESHOLD_MG:
        # Per 100mg over threshold
        excess_te = exposure_metrics["weekly_te_total"] - PHYSIOLOGIC_THRESHOLD_MG
        if excess_te > 0 and exposure_metrics["weeks_supra_per_year"] >= 26:
            num_100mg_blocks = excess_te / 100
            if "per_100mg_wte_over_150mg_26wks" in coefficients:
                for domain, base_mult in coefficients["per_100mg_wte_over_150mg_26wks"].items():
                    if domain in multipliers:
                        # Compound the multiplier
                        compound_mult = pow(base_mult, num_100mg_blocks)
                        multipliers[domain].append(compound_mult)
    
    # Stack multiplier
    if exposure_metrics["weekly_te_total"] >= 300 and exposure_metrics["weeks_supra_per_year"] >= 20:
        apply_multiplier("stack_300mg_20wks")
    
    # Oral multipliers
    if exposure_metrics["oral_17aa_weeks"] > 0:
        if exposure_metrics["oral_17aa_high_dose_weeks"] > 5:
            apply_multiplier("oral_17aa_10wks_high")
        else:
            apply_multiplier("oral_17aa_10wks_moderate")
    
    # Lab-based multipliers
    apply_multiplier("hdl_nadir_lt25", hdl_nadir < 25)
    apply_multiplier("hematocrit_gt54", labs.get("hematocrit", 45) > 54)
    
    # Recovery ratio
    apply_multiplier("recovery_ratio_lt_0_5", exposure_metrics["recovery_ratio"] < 0.5)
    
    # Protective factors - VO2max improvements
    vo2_improvement = interventions.get("vo2max_improvement", 0)
    if vo2_improvement >= 5:
        apply_multiplier("vo2_plus5")
        if vo2_improvement >= 10:
            apply_multiplier("additional_vo2_plus5")
    
    # Body fat reduction
    bf_reduction = interventions.get("bodyfat_reduction", 0)
    if bf_reduction >= 5:
        apply_multiplier("bodyfat_minus5pts")
    
    # Lifestyle factors
    apply_multiplier("med_diet_high", lifestyle.get("mediterranean_adherence", 5) >= 8)
    apply_multiplier("osa_treated", lifestyle.get("osa_status") == "treated")
    
    # Mitigation strategies
    if interventions.get("eliminate_orals"):
        # This is handled by not applying oral multipliers when recalculating
        pass
    
    apply_multiplier("replace_heavy_with_mild", interventions.get("replace_heavy_mild", False))
    
    # Medications
    statin_intensity = interventions.get("statin_intensity", "none")
    if statin_intensity == "low":
        apply_multiplier("statin_low_intensity")
    elif statin_intensity == "moderate":
        apply_multiplier("statin_moderate")
    elif statin_intensity == "high":
        apply_multiplier("statin_high")
    
    apply_multiplier("ezetimibe_addon", interventions.get("ezetimibe", False))
    apply_multiplier("pcsk9_inhibitor", interventions.get("pcsk9", False))
    apply_multiplier("omega3_high_purity", interventions.get("omega3", False))
    apply_multiplier("glp1_gip", interventions.get("glp1_agonist", False))
    apply_multiplier("metformin", interventions.get("metformin", False))
    apply_multiplier("pde5_daily", interventions.get("pde5_daily", False))
    apply_multiplier("finasteride_dutasteride", interventions.get("finasteride", False))
    
    # AI misuse
    apply_multiplier("ai_excess_use", interventions.get("ai_excess", False))
    
    # PCT/support
    apply_multiplier("serm_post_cycle", interventions.get("serm_pct", False))
    apply_multiplier("hcg_support", interventions.get("hcg", False))
    
    # Hematocrit management
    if labs.get("hematocrit", 45) > 54:
        if interventions.get("dose_reduction_hct", False):
            apply_multiplier("dose_reduction_for_hct")
        elif interventions.get("blood_donation_only", False):
            apply_multiplier("blood_donation_only_without_dose_reduction")
    
    return multipliers


def adjust_baseline_for_protective_factors(user_data: Dict, baseline_risks: Dict) -> Dict[str, float]:
    """Adjust baseline risks based on user's protective factors.
    
    Args:
        user_data: User input data
        baseline_risks: Base population risks
        
    Returns:
        Adjusted baseline risks
    """
    adjusted = baseline_risks.copy()
    labs = user_data.get("labs", {})
    anthropometrics = user_data.get("anthropometrics", {})
    performance = user_data.get("performance", {})
    lifestyle = user_data.get("lifestyle", {})
    
    # Check protective factors
    protective_multipliers = {domain: 1.0 for domain in baseline_risks}
    
    # LDL optimal
    if labs.get("ldl", 100) <= 70:
        for domain, factor in PROTECTIVE_FACTOR_ADJUSTMENTS["ldl_optimal"].items():
            if domain in protective_multipliers:
                protective_multipliers[domain] *= factor
    
    # VO2max excellent
    if performance.get("vo2max", 40) > 50:
        for domain, factor in PROTECTIVE_FACTOR_ADJUSTMENTS["vo2max_excellent"].items():
            if domain in protective_multipliers:
                protective_multipliers[domain] *= factor
    
    # Body fat optimal
    if anthropometrics.get("body_fat_pct", 20) <= 15:
        for domain, factor in PROTECTIVE_FACTOR_ADJUSTMENTS["bodyfat_optimal"].items():
            if domain in protective_multipliers:
                protective_multipliers[domain] *= factor
    
    # Mediterranean diet excellent
    if lifestyle.get("mediterranean_adherence", 5) >= 8:
        for domain, factor in PROTECTIVE_FACTOR_ADJUSTMENTS["diet_excellent"].items():
            if domain in protective_multipliers:
                protective_multipliers[domain] *= factor
    
    # Non-smoker
    if not lifestyle.get("smoking", False):
        for domain, factor in PROTECTIVE_FACTOR_ADJUSTMENTS["non_smoker"].items():
            if domain in protective_multipliers:
                protective_multipliers[domain] *= factor
    
    # OSA treated
    if lifestyle.get("osa_status") == "treated":
        for domain, factor in PROTECTIVE_FACTOR_ADJUSTMENTS["osa_treated"].items():
            if domain in protective_multipliers:
                protective_multipliers[domain] *= factor
    
    # Apply adjustments
    for domain in adjusted:
        if domain in protective_multipliers:
            adjusted[domain] *= protective_multipliers[domain]
    
    return adjusted