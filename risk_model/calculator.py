"""Core risk calculation engine."""

from typing import Dict, Any, Tuple
import numpy as np

from .baseline_constants import BASELINE_RISKS, AVERAGE_EVENT_AGE
from .multipliers import (
    load_preset_coefficients, collect_active_multipliers,
    adjust_baseline_for_protective_factors, calculate_exposure_metrics
)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def compute_event_free_years(domain: str, arr: float, current_age: int, horizon_age: int = 80) -> float:
    """Calculate event-free years gained.
    
    Args:
        domain: Health domain
        arr: Absolute risk reduction (as decimal)
        current_age: User's current age
        horizon_age: Time horizon for calculation
        
    Returns:
        Event-free years gained
    """
    avg_event_age = AVERAGE_EVENT_AGE.get(domain, 65)
    horizon_remaining = max(0, horizon_age - current_age)
    
    # Calculate offset
    avg_event_age_offset = max(0, avg_event_age - current_age)
    
    # EFY = ARR * (HorizonRemaining - AvgEventAgeOffset)
    efy = arr * (horizon_remaining - avg_event_age_offset)
    
    return max(0, efy)


def compute_domain_risks(user_data: Dict, preset_name: str = "moderate") -> Dict[str, Dict[str, float]]:
    """Compute risk metrics for all domains.
    
    Args:
        user_data: User input data
        preset_name: Coefficient preset to use
        
    Returns:
        Dictionary of domain risk metrics
    """
    # Load coefficients
    coefficients = load_preset_coefficients(preset_name)
    
    # Get baseline risks and adjust for protective factors
    baseline_risks = BASELINE_RISKS.copy()
    physiologic_reference = adjust_baseline_for_protective_factors(user_data, baseline_risks)
    
    # Collect active multipliers
    multipliers = collect_active_multipliers(user_data, coefficients)
    
    # Calculate adjusted risks
    adjusted_risks = {}
    
    for domain, base_risk in physiologic_reference.items():
        # Apply multipliers
        relative_risk = 1.0
        if domain in multipliers:
            for mult in multipliers[domain]:
                relative_risk *= mult
        
        # Calculate absolute risk
        adjusted_absolute = base_risk * relative_risk
        adjusted_absolute = clamp(adjusted_absolute, 0.0, 0.99)
        
        # Calculate metrics
        rr_vs_population = adjusted_absolute / baseline_risks[domain] if baseline_risks[domain] > 0 else 1.0
        rr_vs_physio = adjusted_absolute / physiologic_reference[domain] if physiologic_reference[domain] > 0 else 1.0
        
        # Absolute risk reduction vs baseline
        arr_vs_baseline = baseline_risks[domain] - adjusted_absolute
        
        # Event-free years
        current_age = user_data.get("demographics", {}).get("age", 30)
        efy = compute_event_free_years(domain, arr_vs_baseline, current_age)
        
        adjusted_risks[domain] = {
            "absolute_risk": adjusted_absolute,
            "absolute_risk_pct": adjusted_absolute * 100,
            "rr_vs_population": rr_vs_population,
            "rr_vs_physio": rr_vs_physio,
            "arr_vs_baseline": arr_vs_baseline,
            "event_free_years": efy,
            "active_multipliers": multipliers.get(domain, []),
        }
    
    return adjusted_risks


def compute_uncertainty_band(value: float, relative_uncertainty: float = 0.15) -> Tuple[float, float]:
    """Calculate uncertainty band around a value.
    
    Args:
        value: Central value
        relative_uncertainty: Relative uncertainty (default 15%)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    lower = value * (1 - relative_uncertainty)
    upper = value * (1 + relative_uncertainty)
    return (lower, upper)


def calculate_intervention_impact(
    user_data_base: Dict, 
    user_data_intervention: Dict, 
    preset_name: str = "moderate"
) -> Dict[str, Dict[str, float]]:
    """Calculate the impact of an intervention.
    
    Args:
        user_data_base: User data before intervention
        user_data_intervention: User data with intervention
        preset_name: Coefficient preset to use
        
    Returns:
        Dictionary of intervention impacts by domain
    """
    risks_base = compute_domain_risks(user_data_base, preset_name)
    risks_intervention = compute_domain_risks(user_data_intervention, preset_name)
    
    impact = {}
    for domain in risks_base:
        base_risk = risks_base[domain]["absolute_risk"]
        intervention_risk = risks_intervention[domain]["absolute_risk"]
        
        impact[domain] = {
            "absolute_risk_reduction": base_risk - intervention_risk,
            "relative_risk_reduction": (base_risk - intervention_risk) / base_risk if base_risk > 0 else 0,
            "risk_ratio": intervention_risk / base_risk if base_risk > 0 else 1.0,
            "efy_gained": risks_intervention[domain]["event_free_years"] - risks_base[domain]["event_free_years"],
        }
    
    return impact


def create_physiologic_reference_scenario() -> Dict[str, Any]:
    """Create a physiologic TRT reference scenario.
    
    Returns:
        User data for physiologic TRT scenario
    """
    return {
        "demographics": {"age": 45, "sex": "male"},
        "aas_regimen": [{
            "compound": "testosterone",
            "weekly_mg": 140,
            "start_week": 1,
            "duration_weeks": 52,
            "is_oral": False,
        }],
        "labs": {
            "hdl": 45,
            "ldl": 90,
            "hematocrit": 48,
        },
        "lifestyle": {
            "mediterranean_adherence": 6,
            "osa_status": "none",
            "smoking": False,
        },
        "performance": {
            "vo2max": 42,
        },
        "anthropometrics": {
            "body_fat_pct": 18,
        },
    }


def create_high_risk_reference_scenario() -> Dict[str, Any]:
    """Create a high-risk reference scenario.
    
    Returns:
        User data for high-risk scenario
    """
    return {
        "demographics": {"age": 30, "sex": "male"},
        "aas_regimen": [
            {
                "compound": "testosterone",
                "weekly_mg": 500,
                "start_week": 1,
                "duration_weeks": 20,
                "is_oral": False,
            },
            {
                "compound": "trenbolone",
                "weekly_mg": 300,
                "start_week": 1,
                "duration_weeks": 16,
                "is_oral": False,
            },
            {
                "compound": "anadrol",
                "weekly_mg": 350,  # 50mg/day
                "start_week": 1,
                "duration_weeks": 8,
                "is_oral": True,
            },
        ],
        "labs": {
            "hdl": 35,
            "ldl": 120,
            "hematocrit": 55,
        },
        "lifestyle": {
            "mediterranean_adherence": 4,
            "osa_status": "untreated",
            "smoking": False,
        },
        "performance": {
            "vo2max": 38,
        },
        "anthropometrics": {
            "body_fat_pct": 22,
        },
    }


def interpolate_risk_trajectory(
    current_age: int,
    current_risk: float,
    domain: str,
    horizon_age: int = 80,
    method: str = "linear"
) -> Dict[int, float]:
    """Interpolate risk trajectory over time.
    
    Args:
        current_age: Current age
        current_risk: Current absolute risk
        domain: Health domain
        horizon_age: Maximum age for projection
        method: Interpolation method ('linear' or 'logistic')
        
    Returns:
        Dictionary mapping age to projected risk
    """
    trajectory = {}
    avg_event_age = AVERAGE_EVENT_AGE.get(domain, 65)
    
    if method == "linear":
        # Simple linear interpolation
        for age in range(current_age, horizon_age + 1):
            if age <= avg_event_age:
                # Slower progression before average event age
                progress = (age - current_age) / (avg_event_age - current_age + 1)
                trajectory[age] = current_risk * progress * 0.7
            else:
                # Faster progression after average event age
                base = trajectory.get(avg_event_age, current_risk * 0.7)
                remaining = current_risk - base
                progress = (age - avg_event_age) / (horizon_age - avg_event_age + 1)
                trajectory[age] = base + remaining * progress
    
    elif method == "logistic":
        # S-curve progression
        midpoint = (current_age + avg_event_age) / 2
        steepness = 0.1
        
        for age in range(current_age, horizon_age + 1):
            x = (age - midpoint) * steepness
            sigmoid = 1 / (1 + np.exp(-x))
            trajectory[age] = current_risk * sigmoid
    
    return trajectory