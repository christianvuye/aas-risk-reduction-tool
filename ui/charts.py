"""Chart components for risk visualization."""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Any, Optional
import numpy as np

from risk_model.baseline_constants import DOMAIN_DISPLAY_NAMES, BASELINE_RISKS
from risk_model.calculator import interpolate_risk_trajectory, compute_uncertainty_band


def create_risk_gauge(domain: str, risk_data: Dict, show_baseline: bool = True) -> go.Figure:
    """Create a gauge chart for absolute risk.
    
    Args:
        domain: Health domain
        risk_data: Risk data for domain
        show_baseline: Whether to show baseline marker
        
    Returns:
        Plotly figure
    """
    abs_risk = risk_data.get("absolute_risk_pct", 0)
    baseline = BASELINE_RISKS.get(domain, 0.5) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=abs_risk,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{DOMAIN_DISPLAY_NAMES.get(domain, domain)} Risk"},
        delta={'reference': baseline if show_baseline else None},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': '#0b8f55'},
                {'range': [25, 50], 'color': '#ffb347'},
                {'range': [50, 75], 'color': '#ff7f50'},
                {'range': [75, 100], 'color': '#d93d3d'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': baseline if show_baseline else abs_risk
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig


def create_waterfall_chart(
    domain: str,
    baseline_risk: float,
    interventions: List[Dict[str, float]],
    final_risk: float
) -> go.Figure:
    """Create waterfall chart showing intervention impacts.
    
    Args:
        domain: Health domain
        baseline_risk: Starting risk
        interventions: List of intervention impacts
        final_risk: Final risk after all interventions
        
    Returns:
        Plotly figure
    """
    # Build waterfall data
    x_labels = ["Population Baseline"]
    y_values = [baseline_risk * 100]
    measure = ["absolute"]
    
    current_risk = baseline_risk
    
    for intervention in interventions:
        name = intervention.get("name", "Intervention")
        impact = intervention.get("impact", 0) * 100
        
        x_labels.append(name)
        y_values.append(impact)
        measure.append("relative")
        
        current_risk += intervention.get("impact", 0)
    
    # Add final total
    x_labels.append("Final Risk")
    y_values.append(final_risk * 100)
    measure.append("total")
    
    fig = go.Figure(go.Waterfall(
        name="Risk Reduction",
        orientation="v",
        measure=measure,
        x=x_labels,
        textposition="outside",
        text=[f"{val:.1f}%" for val in y_values],
        y=y_values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        decreasing={"marker": {"color": "#0b8f55"}},
        increasing={"marker": {"color": "#d93d3d"}},
        totals={"marker": {"color": "#2d5fff"}}
    ))
    
    fig.update_layout(
        title=f"{DOMAIN_DISPLAY_NAMES.get(domain, domain)} Risk: Intervention Stack",
        xaxis_title="Interventions",
        yaxis_title="Absolute Risk (%)",
        height=400,
        showlegend=False,
        template="plotly_white"
    )
    
    return fig


def create_risk_trajectory_chart(
    scenarios: List[Dict[str, Any]],
    domains: List[str],
    current_age: int,
    horizon_age: int = 80
) -> go.Figure:
    """Create line chart showing risk trajectories over time.
    
    Args:
        scenarios: List of scenario data
        domains: Domains to plot
        current_age: Current age
        horizon_age: Maximum age for projection
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Use reliable hex colors instead of px.colors.qualitative.Set2
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
        """Convert hex color to rgba string."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f'rgba({r}, {g}, {b}, {alpha})'
        else:
            # Fallback for invalid hex
            return f'rgba(100, 100, 100, {alpha})'
    
    for idx, scenario in enumerate(scenarios):
        scenario_name = scenario.get("name", f"Scenario {idx+1}")
        color = colors[idx % len(colors)]
        
        for domain in domains:
            if domain in scenario.get("risks", {}):
                risk_data = scenario["risks"][domain]
                current_risk = risk_data.get("absolute_risk", 0)
                
                # Get trajectory
                trajectory = interpolate_risk_trajectory(
                    current_age, current_risk, domain, horizon_age
                )
                
                ages = list(trajectory.keys())
                risks = [trajectory[age] * 100 for age in ages]
                
                # Add uncertainty band
                lower_bounds = []
                upper_bounds = []
                for risk in risks:
                    lower, upper = compute_uncertainty_band(risk)
                    lower_bounds.append(lower)
                    upper_bounds.append(upper)
                
                # Plot main line
                fig.add_trace(go.Scatter(
                    x=ages,
                    y=risks,
                    mode='lines',
                    name=f"{scenario_name} - {DOMAIN_DISPLAY_NAMES.get(domain, domain)}",
                    line=dict(color=color, width=2),
                    legendgroup=scenario_name
                ))
                
                # Add uncertainty band
                fig.add_trace(go.Scatter(
                    x=ages + ages[::-1],
                    y=upper_bounds + lower_bounds[::-1],
                    fill='toself',
                    fillcolor=hex_to_rgba(color, 0.2),
                    line=dict(color='rgba(255,255,255,0)'),
                    showlegend=False,
                    legendgroup=scenario_name,
                    hoverinfo='skip'
                ))
    
    fig.update_layout(
        title="Risk Trajectories Over Time",
        xaxis_title="Age (years)",
        yaxis_title="Absolute Risk (%)",
        height=500,
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig


def create_radar_chart(
    risk_data: Dict[str, Dict],
    baseline_data: Optional[Dict[str, Dict]] = None,
    title: str = "Risk Profile"
) -> go.Figure:
    """Create radar chart comparing risks across domains.
    
    Args:
        risk_data: Current risk data by domain
        baseline_data: Optional baseline for comparison
        title: Chart title
        
    Returns:
        Plotly figure
    """
    domains = list(risk_data.keys())
    display_names = [DOMAIN_DISPLAY_NAMES.get(d, d) for d in domains]
    
    # Get relative risks
    rr_values = [risk_data[d].get("rr_vs_population", 1.0) for d in domains]
    
    fig = go.Figure()
    
    # Add current risk
    fig.add_trace(go.Scatterpolar(
        r=rr_values,
        theta=display_names,
        fill='toself',
        name='Current Risk',
        line=dict(color='#2d5fff', width=2),
        fillcolor='rgba(45, 95, 255, 0.3)'
    ))
    
    # Add baseline if provided
    if baseline_data:
        baseline_rr = [baseline_data.get(d, {}).get("rr_vs_population", 1.0) for d in domains]
        fig.add_trace(go.Scatterpolar(
            r=baseline_rr,
            theta=display_names,
            fill='toself',
            name='Baseline',
            line=dict(color='#666', width=2, dash='dash'),
            fillcolor='rgba(102, 102, 102, 0.1)'
        ))
    
    # Add reference circle at RR=1
    fig.add_trace(go.Scatterpolar(
        r=[1] * len(domains),
        theta=display_names,
        mode='lines',
        line=dict(color='red', width=1, dash='dot'),
        name='Population Average',
        fill=None
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(2.5, max(rr_values) * 1.1)]
            )
        ),
        showlegend=True,
        title=title,
        height=500,
        template="plotly_white"
    )
    
    return fig


def create_intervention_impact_chart(
    interventions: List[Dict[str, Any]],
    domain: str = "ascvd"
) -> go.Figure:
    """Create bar chart showing intervention impacts.
    
    Args:
        interventions: List of interventions with impacts
        domain: Domain to show impacts for
        
    Returns:
        Plotly figure
    """
    # Sort by impact magnitude
    sorted_interventions = sorted(
        interventions,
        key=lambda x: abs(x.get("impact", {}).get(domain, 0)),
        reverse=True
    )
    
    names = []
    impacts = []
    colors = []
    
    for intervention in sorted_interventions:
        impact = intervention.get("impact", {}).get(domain, 0) * 100
        if abs(impact) > 0.1:  # Only show meaningful impacts
            names.append(intervention.get("name", "Unknown"))
            impacts.append(impact)
            colors.append("#0b8f55" if impact < 0 else "#d93d3d")
    
    fig = go.Figure(go.Bar(
        x=impacts,
        y=names,
        orientation='h',
        marker_color=colors,
        text=[f"{val:+.1f}%" for val in impacts],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"Intervention Impacts on {DOMAIN_DISPLAY_NAMES.get(domain, domain)} Risk",
        xaxis_title="Risk Change (%)",
        yaxis_title="Intervention",
        height=max(300, len(names) * 40),
        template="plotly_white",
        xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
    )
    
    return fig


def create_scenario_comparison_table(scenarios: List[Dict]) -> go.Figure:
    """Create comparison table for multiple scenarios.
    
    Args:
        scenarios: List of scenario data
        
    Returns:
        Plotly figure
    """
    if not scenarios:
        return go.Figure()
    
    # Prepare data
    headers = ["Scenario", "Category", "ASCVD %", "HF %", "Thrombosis %", 
               "Diabetes %", "EFY ASCVD", "Interventions"]
    
    cells = [[] for _ in headers]
    
    for scenario in scenarios:
        cells[0].append(scenario.get("name", "Unknown"))
        cells[1].append(scenario.get("category", "unknown"))
        
        risks = scenario.get("risks", {})
        cells[2].append(f"{risks.get('ascvd', {}).get('absolute_risk_pct', 0):.1f}")
        cells[3].append(f"{risks.get('hf', {}).get('absolute_risk_pct', 0):.1f}")
        cells[4].append(f"{risks.get('thrombosis', {}).get('absolute_risk_pct', 0):.1f}")
        cells[5].append(f"{risks.get('diabetes', {}).get('absolute_risk_pct', 0):.1f}")
        cells[6].append(f"{risks.get('ascvd', {}).get('event_free_years', 0):.1f}")
        cells[7].append(len(scenario.get("interventions", [])))
    
    # Color coding for categories
    category_colors = {
        "physiologic": "#0b8f55",
        "moderate": "#ffb347",
        "high_risk": "#d93d3d"
    }
    
    cell_colors = [
        ["white"] * len(scenarios),  # Scenario names
        [category_colors.get(cat, "white") for cat in cells[1]],  # Categories
        ["white"] * len(scenarios),  # ASCVD
        ["white"] * len(scenarios),  # HF
        ["white"] * len(scenarios),  # Thrombosis
        ["white"] * len(scenarios),  # Diabetes
        ["white"] * len(scenarios),  # EFY
        ["white"] * len(scenarios),  # Interventions
    ]
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=headers,
            fill_color='#2d5fff',
            font=dict(color='white', size=14),
            align='left'
        ),
        cells=dict(
            values=cells,
            fill_color=cell_colors,
            font=dict(size=12),
            align='left',
            height=30
        )
    )])
    
    fig.update_layout(
        title="Scenario Comparison",
        height=200 + len(scenarios) * 40,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


def create_domain_bar_chart(
    risk_data: Dict[str, Dict],
    show_baseline: bool = True,
    sort_by: str = "absolute"
) -> go.Figure:
    """Create bar chart comparing risks across domains.
    
    Args:
        risk_data: Risk data by domain
        show_baseline: Whether to show baseline comparison
        sort_by: How to sort domains ('absolute', 'relative', 'name')
        
    Returns:
        Plotly figure
    """
    domains = list(risk_data.keys())
    
    # Sort domains
    if sort_by == "absolute":
        domains = sorted(domains, key=lambda d: risk_data[d].get("absolute_risk_pct", 0), reverse=True)
    elif sort_by == "relative":
        domains = sorted(domains, key=lambda d: risk_data[d].get("rr_vs_population", 1), reverse=True)
    
    display_names = [DOMAIN_DISPLAY_NAMES.get(d, d) for d in domains]
    
    fig = go.Figure()
    
    # Current risks
    current_risks = [risk_data[d].get("absolute_risk_pct", 0) for d in domains]
    fig.add_trace(go.Bar(
        name='Current Risk',
        x=display_names,
        y=current_risks,
        marker_color='#2d5fff',
        text=[f"{r:.1f}%" for r in current_risks],
        textposition='outside'
    ))
    
    # Baseline risks
    if show_baseline:
        baseline_risks = [BASELINE_RISKS.get(d, 0) * 100 for d in domains]
        fig.add_trace(go.Bar(
            name='Population Baseline',
            x=display_names,
            y=baseline_risks,
            marker_color='lightgray',
            text=[f"{r:.1f}%" for r in baseline_risks],
            textposition='outside'
        ))
    
    fig.update_layout(
        title="Absolute Risk by Domain",
        xaxis_title="Health Domain",
        yaxis_title="Lifetime Risk (%)",
        barmode='group',
        height=500,
        template="plotly_white",
        xaxis_tickangle=-45
    )
    
    return fig