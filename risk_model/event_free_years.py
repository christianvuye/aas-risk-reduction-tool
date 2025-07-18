"""Event-free years calculation utilities."""

from typing import Dict, List, Tuple
import numpy as np

from .baseline_constants import AVERAGE_EVENT_AGE, BASELINE_RISKS


def calculate_cumulative_risk_over_time(
    annual_risk: float,
    years: int
) -> float:
    """Calculate cumulative risk over a period.
    
    Args:
        annual_risk: Annual risk rate
        years: Number of years
        
    Returns:
        Cumulative risk probability
    """
    # Using the formula: Cumulative = 1 - (1 - annual_risk)^years
    if annual_risk <= 0:
        return 0.0
    if annual_risk >= 1:
        return 1.0
    
    cumulative = 1 - pow(1 - annual_risk, years)
    return min(cumulative, 0.99)


def years_to_event_probability(
    lifetime_risk: float,
    current_age: int,
    domain: str,
    target_probability: float = 0.5
) -> float:
    """Calculate years until a target event probability.
    
    Args:
        lifetime_risk: Lifetime risk (0-1)
        current_age: Current age
        domain: Health domain
        target_probability: Target cumulative probability
        
    Returns:
        Estimated years to target probability
    """
    avg_event_age = AVERAGE_EVENT_AGE.get(domain, 65)
    remaining_years = max(1, 80 - current_age)
    
    # Estimate annual risk
    annual_risk = 1 - pow(1 - lifetime_risk, 1 / remaining_years)
    
    # Calculate years to target probability
    if annual_risk <= 0:
        return float('inf')
    
    years = np.log(1 - target_probability) / np.log(1 - annual_risk)
    
    # Adjust based on typical event age
    if current_age < avg_event_age:
        # Events are less likely before average age
        adjustment = 1 + (avg_event_age - current_age) / 40
        years *= adjustment
    
    return years


def calculate_quality_adjusted_life_years(
    domain_risks: Dict[str, float],
    current_age: int,
    horizon_age: int = 80
) -> float:
    """Calculate quality-adjusted life years based on risk profile.
    
    Args:
        domain_risks: Dictionary of domain absolute risks
        current_age: Current age
        horizon_age: Time horizon
        
    Returns:
        Estimated QALYs
    """
    years_remaining = max(0, horizon_age - current_age)
    
    # Domain-specific quality weights (simplified)
    quality_weights = {
        "ascvd": 0.8,
        "hf": 0.7,
        "thrombosis": 0.85,
        "ischemic_stroke": 0.6,
        "hemorrhagic_stroke": 0.5,
        "hepatic": 0.85,
        "renal": 0.8,
        "neuro": 0.75,
        "diabetes": 0.85,
        "dementia": 0.4,
        "cancer_colorectal": 0.7,
        "cancer_prostate": 0.9,
        "endocrine": 0.9,
        "dermatologic": 0.95,
    }
    
    # Calculate expected quality adjustment
    total_quality_loss = 0
    
    for domain, risk in domain_risks.items():
        if domain in quality_weights:
            quality_loss = risk * (1 - quality_weights[domain])
            total_quality_loss += quality_loss
    
    # Avoid double counting overlapping conditions
    total_quality_loss = min(total_quality_loss, 0.6)
    
    # Calculate QALYs
    average_quality = 1 - total_quality_loss / 2  # Assume gradual decline
    qalys = years_remaining * average_quality
    
    return qalys


def calculate_intervention_efficiency(
    baseline_risks: Dict[str, Dict],
    intervention_risks: Dict[str, Dict],
    intervention_cost_category: str = "low"
) -> Dict[str, float]:
    """Calculate intervention efficiency metrics.
    
    Args:
        baseline_risks: Risks before intervention
        intervention_risks: Risks after intervention
        intervention_cost_category: Cost category (low, medium, high)
        
    Returns:
        Dictionary of efficiency metrics
    """
    # Cost weights (arbitrary units for comparison)
    cost_weights = {
        "low": 1.0,      # e.g., lifestyle changes
        "medium": 5.0,   # e.g., generic medications
        "high": 20.0,    # e.g., PCSK9 inhibitors
    }
    
    cost = cost_weights.get(intervention_cost_category, 1.0)
    
    # Calculate total event-free years gained
    total_efy_gained = 0
    domain_efy = {}
    
    for domain in baseline_risks:
        if domain in intervention_risks:
            baseline_efy = baseline_risks[domain].get("event_free_years", 0)
            intervention_efy = intervention_risks[domain].get("event_free_years", 0)
            efy_gained = intervention_efy - baseline_efy
            
            domain_efy[domain] = efy_gained
            total_efy_gained += efy_gained
    
    # Calculate efficiency
    efficiency = total_efy_gained / cost if cost > 0 else 0
    
    return {
        "total_efy_gained": total_efy_gained,
        "cost_per_efy": cost / total_efy_gained if total_efy_gained > 0 else float('inf'),
        "efficiency_score": efficiency,
        "domain_contributions": domain_efy,
    }


def project_lifetime_events_avoided(
    risk_reduction: Dict[str, float],
    population_size: int = 1000
) -> Dict[str, int]:
    """Project number of events avoided in a population.
    
    Args:
        risk_reduction: Absolute risk reduction by domain
        population_size: Size of theoretical population
        
    Returns:
        Dictionary of events avoided by domain
    """
    events_avoided = {}
    
    for domain, arr in risk_reduction.items():
        # Convert to events avoided
        avoided = int(round(arr * population_size))
        events_avoided[domain] = avoided
    
    return events_avoided


def calculate_composite_cardiovascular_benefit(
    domain_risks: Dict[str, Dict]
) -> Dict[str, float]:
    """Calculate composite cardiovascular benefit metrics.
    
    Args:
        domain_risks: Risk data by domain
        
    Returns:
        Composite CV metrics
    """
    # Domains contributing to CV composite
    cv_domains = ["ascvd", "hf", "thrombosis", "ischemic_stroke"]
    
    # Calculate composite risk (avoiding double counting)
    composite_risk = 0
    composite_efy = 0
    
    for domain in cv_domains:
        if domain in domain_risks:
            # Weight to avoid double counting
            weight = 1.0
            if domain == "ischemic_stroke":
                weight = 0.3  # Already partially in ASCVD
            
            composite_risk += domain_risks[domain]["absolute_risk"] * weight
            composite_efy += domain_risks[domain]["event_free_years"] * weight
    
    # Cap composite risk
    composite_risk = min(composite_risk, 0.7)
    
    return {
        "composite_cv_risk": composite_risk,
        "composite_cv_risk_pct": composite_risk * 100,
        "composite_cv_efy": composite_efy,
    }