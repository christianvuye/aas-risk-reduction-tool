"""Layout components and variant managers."""

import streamlit as st
from typing import Dict, List, Any, Optional

from .badges import render_category_badge, render_risk_badge, render_metric_card
from .charts import (
    create_risk_gauge, create_waterfall_chart, create_risk_trajectory_chart,
    create_radar_chart, create_domain_bar_chart, create_scenario_comparison_table
)
from risk_model.baseline_constants import DOMAIN_CATEGORIES, DOMAIN_DISPLAY_NAMES


def render_epoch_tabs_layout(
    scenario_data: Dict[str, Any],
    comparison_scenarios: Optional[List[Dict]] = None
):
    """Render Epoch-style tabbed layout.
    
    Args:
        scenario_data: Current scenario data
        comparison_scenarios: Optional scenarios for comparison
    """
    st.header(f"Risk Analysis: {scenario_data.get('name', 'Current Scenario')}")
    
    # Category badge
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_category_badge(scenario_data.get("category", "unknown"))
    
    # Create tabs for each domain category
    tabs = st.tabs(list(DOMAIN_CATEGORIES.keys()))
    
    for idx, (category, domains) in enumerate(DOMAIN_CATEGORIES.items()):
        with tabs[idx]:
            # Filter domains that exist in scenario
            available_domains = [d for d in domains if d in scenario_data.get("risks", {})]
            
            if not available_domains:
                st.info(f"No data available for {category} domains")
                continue
            
            # Create sub-tabs for individual domains
            if len(available_domains) > 1:
                domain_tabs = st.tabs([DOMAIN_DISPLAY_NAMES.get(d, d) for d in available_domains])
                
                for d_idx, domain in enumerate(available_domains):
                    with domain_tabs[d_idx]:
                        render_domain_analysis(domain, scenario_data, comparison_scenarios)
            else:
                # Single domain - no sub-tabs needed
                render_domain_analysis(available_domains[0], scenario_data, comparison_scenarios)


def render_domain_analysis(
    domain: str,
    scenario_data: Dict[str, Any],
    comparison_scenarios: Optional[List[Dict]] = None
):
    """Render analysis for a single domain.
    
    Args:
        domain: Domain to analyze
        scenario_data: Current scenario data
        comparison_scenarios: Optional comparison scenarios
    """
    risk_data = scenario_data["risks"].get(domain, {})
    
    # Risk overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            "Absolute Risk",
            risk_data.get("absolute_risk_pct", 0),
            "%"
        )
    
    with col2:
        render_metric_card(
            "RR vs Population",
            risk_data.get("rr_vs_population", 1.0),
            "x",
            color="#2d5fff"
        )
    
    with col3:
        render_metric_card(
            "Event-Free Years",
            risk_data.get("event_free_years", 0),
            " years",
            color="#0b8f55"
        )
    
    with col4:
        render_risk_badge(domain, risk_data)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge chart
        fig_gauge = create_risk_gauge(domain, risk_data)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Waterfall chart (if interventions exist)
        if scenario_data.get("interventions"):
            # Build intervention impacts (simplified for now)
            interventions = []
            for intervention in scenario_data["interventions"]:
                interventions.append({
                    "name": intervention,
                    "impact": -0.01  # Placeholder impact
                })
            
            fig_waterfall = create_waterfall_chart(
                domain,
                risk_data.get("absolute_risk", 0.5),
                interventions,
                risk_data.get("absolute_risk", 0.4)
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # Trajectory chart if comparisons available
    if comparison_scenarios:
        all_scenarios = [scenario_data] + comparison_scenarios
        current_age = scenario_data.get("user_data", {}).get("demographics", {}).get("age", 30)
        
        fig_trajectory = create_risk_trajectory_chart(
            all_scenarios,
            [domain],
            current_age
        )
        st.plotly_chart(fig_trajectory, use_container_width=True)


def render_multi_panel_dashboard(
    scenario_data: Dict[str, Any],
    comparison_scenarios: Optional[List[Dict]] = None
):
    """Render multi-panel dashboard layout.
    
    Args:
        scenario_data: Current scenario data
        comparison_scenarios: Optional scenarios for comparison
    """
    st.header("Risk Dashboard")
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    risks = scenario_data.get("risks", {})
    
    with col1:
        render_category_badge(scenario_data.get("category", "unknown"))
    
    with col2:
        ascvd_risk = risks.get("ascvd", {}).get("absolute_risk_pct", 0)
        render_metric_card("ASCVD Risk", ascvd_risk, "%")
    
    with col3:
        hf_risk = risks.get("hf", {}).get("absolute_risk_pct", 0)
        render_metric_card("Heart Failure", hf_risk, "%")
    
    with col4:
        diabetes_risk = risks.get("diabetes", {}).get("absolute_risk_pct", 0)
        render_metric_card("Diabetes", diabetes_risk, "%")
    
    # Main panels
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Combined cardiovascular chart
        st.subheader("Cardiovascular Risk Trajectory")
        if comparison_scenarios:
            all_scenarios = [scenario_data] + comparison_scenarios
        else:
            all_scenarios = [scenario_data]
        
        cv_domains = ["ascvd", "hf", "thrombosis"]
        current_age = scenario_data.get("user_data", {}).get("demographics", {}).get("age", 30)
        
        fig_trajectory = create_risk_trajectory_chart(
            all_scenarios,
            cv_domains,
            current_age
        )
        st.plotly_chart(fig_trajectory, use_container_width=True)
        
        # Domain comparison bar chart
        st.subheader("Risk by Domain")
        fig_bars = create_domain_bar_chart(risks, show_baseline=True)
        st.plotly_chart(fig_bars, use_container_width=True)
    
    with col2:
        # Radar chart
        st.subheader("Risk Profile")
        fig_radar = create_radar_chart(risks)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Interventions list
        if scenario_data.get("interventions"):
            st.subheader("Active Interventions")
            for intervention in scenario_data["interventions"]:
                st.write(f"• {intervention}")
    
    # Scenario comparison table
    if comparison_scenarios:
        st.subheader("Scenario Comparison")
        all_scenarios = [scenario_data] + comparison_scenarios
        fig_table = create_scenario_comparison_table(all_scenarios)
        st.plotly_chart(fig_table, use_container_width=True)


def render_single_dynamic_chart(
    scenario_data: Dict[str, Any],
    comparison_scenarios: Optional[List[Dict]] = None
):
    """Render single dynamic chart layout.
    
    Args:
        scenario_data: Current scenario data
        comparison_scenarios: Optional scenarios for comparison
    """
    st.header("Dynamic Risk Visualization")
    
    # Chart type selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            ["Line", "Bar", "Waterfall", "Radar"],
            index=0
        )
    
    with col2:
        # Domain selection
        available_domains = list(scenario_data.get("risks", {}).keys())
        selected_domains = st.multiselect(
            "Domains",
            available_domains,
            default=available_domains[:3] if len(available_domains) >= 3 else available_domains
        )
    
    with col3:
        # Scenario selection
        if comparison_scenarios:
            scenario_names = [s.get("name", f"Scenario {i}") for i, s in enumerate(comparison_scenarios)]
            selected_scenarios = st.multiselect(
                "Compare Scenarios",
                scenario_names,
                default=scenario_names[:2] if len(scenario_names) >= 2 else scenario_names
            )
            
            # Filter selected scenarios
            selected_scenario_data = [
                s for s in comparison_scenarios 
                if s.get("name") in selected_scenarios
            ]
        else:
            selected_scenario_data = []
    
    # Render selected chart
    if chart_type == "Line":
        if selected_domains:
            all_scenarios = [scenario_data] + selected_scenario_data
            current_age = scenario_data.get("user_data", {}).get("demographics", {}).get("age", 30)
            
            fig = create_risk_trajectory_chart(
                all_scenarios,
                selected_domains,
                current_age
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Bar":
        # Filter risks to selected domains
        filtered_risks = {
            d: data for d, data in scenario_data["risks"].items()
            if d in selected_domains
        }
        
        fig = create_domain_bar_chart(filtered_risks)
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Waterfall":
        if selected_domains:
            domain = selected_domains[0]  # Use first selected domain
            risk_data = scenario_data["risks"].get(domain, {})
            
            # Simplified intervention impacts
            interventions = []
            if scenario_data.get("interventions"):
                for intervention in scenario_data["interventions"]:
                    interventions.append({
                        "name": intervention,
                        "impact": -0.01
                    })
            
            fig = create_waterfall_chart(
                domain,
                risk_data.get("absolute_risk", 0.5),
                interventions,
                risk_data.get("absolute_risk", 0.4)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Radar":
        # Filter risks to selected domains
        filtered_risks = {
            d: data for d, data in scenario_data["risks"].items()
            if d in selected_domains
        }
        
        fig = create_radar_chart(filtered_risks)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk details table
    with st.expander("Detailed Risk Metrics"):
        for domain in selected_domains:
            if domain in scenario_data["risks"]:
                risk_data = scenario_data["risks"][domain]
                st.subheader(DOMAIN_DISPLAY_NAMES.get(domain, domain))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Absolute Risk", f"{risk_data.get('absolute_risk_pct', 0):.1f}%")
                with col2:
                    st.metric("RR vs Population", f"{risk_data.get('rr_vs_population', 1):.2f}x")
                with col3:
                    st.metric("Event-Free Years", f"{risk_data.get('event_free_years', 0):.1f}")


def render_model_info_sidebar():
    """Render model information in sidebar."""
    with st.sidebar:
        st.markdown("### Model Information")
        
        # Model version
        from risk_model.baseline_constants import MODEL_VERSION
        st.info(f"Model Version: {MODEL_VERSION}")
        
        # Preset selector
        preset = st.selectbox(
            "Risk Preset",
            ["Conservative", "Moderate", "Aggressive"],
            index=1,
            help="Select risk calculation preset"
        )
        
        # Model card link
        if st.button("View Model Card"):
            st.session_state.show_model_card = True
        
        # Export options
        st.markdown("### Export Options")
        export_format = st.selectbox(
            "Export Format",
            ["JSON", "CSV", "PDF", "ZIP (All)"]
        )
        
        if st.button("Export Current Scenario"):
            st.session_state.export_requested = True
            st.session_state.export_format = export_format
        
        return preset.lower()