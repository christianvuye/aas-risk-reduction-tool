"""Badge and status indicator components."""

import streamlit as st
from typing import Dict, Tuple


def get_risk_badge_color(rr_vs_population: float) -> Tuple[str, str, str]:
    """Get badge color and label based on relative risk.
    
    Args:
        rr_vs_population: Relative risk vs population
        
    Returns:
        Tuple of (color, label, text_color)
    """
    if rr_vs_population < 0.75:
        return "#0b8f55", "Reduced", "white"
    elif rr_vs_population <= 1.25:
        return "#f5f5f5", "Approx Avg", "#1e1e1e"
    elif rr_vs_population <= 1.75:
        return "#ffb347", "Elevated", "#1e1e1e"
    else:
        return "#d93d3d", "High", "white"


def get_category_badge_color(category: str) -> Tuple[str, str]:
    """Get badge color for risk category.
    
    Args:
        category: Risk category
        
    Returns:
        Tuple of (color, text_color)
    """
    colors = {
        "physiologic": ("#0b8f55", "white"),
        "moderate": ("#ffb347", "#1e1e1e"),
        "high_risk": ("#d93d3d", "white"),
    }
    return colors.get(category, ("#f5f5f5", "#1e1e1e"))


def render_risk_badge(domain: str, risk_data: Dict, show_value: bool = True):
    """Render a risk badge for a domain.
    
    Args:
        domain: Domain name
        risk_data: Risk data for the domain
        show_value: Whether to show the risk value
    """
    rr = risk_data.get("rr_vs_population", 1.0)
    abs_risk = risk_data.get("absolute_risk_pct", 0)
    
    color, label, text_color = get_risk_badge_color(rr)
    
    badge_html = f"""
    <div style="
        display: inline-block;
        background-color: {color};
        color: {text_color};
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 14px;
        font-weight: 500;
        margin: 2px;
    ">
        {label}
        {f' ({abs_risk:.1f}%)' if show_value else ''}
    </div>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)


def render_category_badge(category: str):
    """Render a category badge.
    
    Args:
        category: Risk category
    """
    color, text_color = get_category_badge_color(category)
    
    labels = {
        "physiologic": "Physiologic TRT",
        "moderate": "Moderate Enhancement",
        "high_risk": "High-Risk",
    }
    
    label = labels.get(category, category)
    
    badge_html = f"""
    <div style="
        display: inline-block;
        background-color: {color};
        color: {text_color};
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 16px;
        font-weight: 600;
        margin: 4px;
    ">
        {label}
    </div>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)


def render_intervention_badge(intervention: str):
    """Render an intervention badge.
    
    Args:
        intervention: Intervention name
    """
    badge_html = f"""
    <div style="
        display: inline-block;
        background-color: #2d5fff;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 13px;
        margin: 2px;
    ">
        {intervention}
    </div>
    """
    
    st.markdown(badge_html, unsafe_allow_html=True)


def render_metric_card(
    title: str,
    value: float,
    unit: str = "%",
    delta: float = None,
    delta_label: str = "vs baseline",
    color: str = None
):
    """Render a metric card.
    
    Args:
        title: Metric title
        value: Metric value
        unit: Unit of measurement
        delta: Change value
        delta_label: Label for delta
        color: Optional color override
    """
    if color is None:
        if delta is not None:
            color = "#0b8f55" if delta < 0 else "#d93d3d"
        else:
            color = "#1e1e1e"
    
    card_html = f"""
    <div style="
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    ">
        <div style="
            font-size: 14px;
            color: #666;
            margin-bottom: 4px;
        ">{title}</div>
        <div style="
            font-size: 28px;
            font-weight: 700;
            color: {color};
        ">{value:.1f}{unit}</div>
    """
    
    if delta is not None:
        delta_symbol = "↓" if delta < 0 else "↑"
        card_html += f"""
        <div style="
            font-size: 14px;
            color: {color};
            margin-top: 4px;
        ">{delta_symbol} {abs(delta):.1f}{unit} {delta_label}</div>
        """
    
    card_html += "</div>"
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_progress_bar(
    label: str,
    value: float,
    max_value: float = 100,
    color: str = "#2d5fff",
    show_value: bool = True
):
    """Render a progress bar.
    
    Args:
        label: Bar label
        value: Current value
        max_value: Maximum value
        color: Bar color
        show_value: Whether to show the value
    """
    percentage = min(100, (value / max_value) * 100) if max_value > 0 else 0
    
    bar_html = f"""
    <div style="margin: 8px 0;">
        <div style="
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        ">
            <span style="font-size: 14px; color: #666;">{label}</span>
            {f'<span style="font-size: 14px; color: #1e1e1e; font-weight: 500;">{value:.1f}</span>' if show_value else ''}
        </div>
        <div style="
            background-color: #e0e0e0;
            border-radius: 4px;
            height: 8px;
            overflow: hidden;
        ">
            <div style="
                background-color: {color};
                width: {percentage}%;
                height: 100%;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """
    
    st.markdown(bar_html, unsafe_allow_html=True)