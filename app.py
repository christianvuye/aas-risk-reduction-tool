"""AAS Risk Reduction Tool - Main Streamlit Application."""

import streamlit as st
from typing import Dict, Any, List
import uuid
from datetime import datetime

# Import risk model components
from risk_model.scenarios import ScenarioManager
from risk_model.calculator import (
    compute_domain_risks, create_physiologic_reference_scenario,
    create_high_risk_reference_scenario
)
from risk_model.plugin_loader import PluginManager

# Import UI components
from ui.forms import (
    render_demographics_form, render_vitals_performance_form,
    render_labs_form, render_genetics_form, render_aas_regimen_form,
    render_lifestyle_form, render_interventions_form
)
from ui.layout import (
    render_epoch_tabs_layout, render_multi_panel_dashboard,
    render_single_dynamic_chart, render_model_info_sidebar
)

# Import export functionality
from export.exporter import export_scenario


# Page configuration
st.set_page_config(
    page_title="AAS Risk Reduction Tool",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f5f5f5;
        border-radius: 8px 8px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2d5fff;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "scenario_manager" not in st.session_state:
        st.session_state.scenario_manager = ScenarioManager()
    
    if "plugin_manager" not in st.session_state:
        st.session_state.plugin_manager = PluginManager()
    
    if "current_scenario_id" not in st.session_state:
        st.session_state.current_scenario_id = None
    
    if "comparison_scenario_ids" not in st.session_state:
        st.session_state.comparison_scenario_ids = []
    
    if "layout_mode" not in st.session_state:
        st.session_state.layout_mode = "epoch_tabs"
    
    if "show_disclaimer" not in st.session_state:
        st.session_state.show_disclaimer = True


def collect_user_data() -> Dict[str, Any]:
    """Collect all user input data.
    
    Returns:
        Combined user data dictionary
    """
    user_data = {}
    
    # Demographics & Anthropometrics
    demo_data = render_demographics_form()
    user_data.update(demo_data)
    
    # Vitals & Performance
    vitals_data = render_vitals_performance_form()
    user_data.update(vitals_data)
    
    # Labs
    labs_data = render_labs_form()
    user_data.update(labs_data)
    
    # Genetics
    genetics_data = render_genetics_form()
    user_data.update(genetics_data)
    
    # AAS Regimen
    aas_data = render_aas_regimen_form()
    user_data.update(aas_data)
    
    # Lifestyle
    lifestyle_data = render_lifestyle_form()
    user_data.update(lifestyle_data)
    
    # Interventions
    interventions_data = render_interventions_form()
    user_data.update(interventions_data)
    
    return user_data


def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Title and description
    st.title("AAS Risk Reduction Tool")
    st.markdown("*Prototype heuristic model for educational harm-reduction exploration*")
    
    # Disclaimer
    if st.session_state.show_disclaimer:
        with st.warning("⚠️ **Disclaimer**"):
            st.markdown(
                "This is a prototype heuristic model for educational harm-reduction exploration. "
                "It is not medical advice. Risk multipliers are not clinically validated. "
                "Always consult healthcare professionals for medical decisions."
            )
            if st.button("I Understand", key="dismiss_disclaimer"):
                st.session_state.show_disclaimer = False
                st.rerun()
    
    # Sidebar
    preset = render_model_info_sidebar()
    st.session_state.scenario_manager.active_preset = preset
    
    # Layout mode selector
    st.sidebar.markdown("### Display Mode")
    layout_mode = st.sidebar.radio(
        "Select Layout",
        ["Epoch Tabs", "Multi-Panel Dashboard", "Single Dynamic Chart"],
        index=["epoch_tabs", "multi_panel", "single_chart"].index(st.session_state.layout_mode)
    )
    
    layout_mapping = {
        "Epoch Tabs": "epoch_tabs",
        "Multi-Panel Dashboard": "multi_panel",
        "Single Dynamic Chart": "single_chart"
    }
    st.session_state.layout_mode = layout_mapping[layout_mode]
    
    # Scenario management sidebar
    st.sidebar.markdown("### Scenario Management")
    
    # List scenarios
    scenarios = st.session_state.scenario_manager.list_scenarios()
    if scenarios:
        scenario_names = [s["name"] for s in scenarios]
        
        # Current scenario selector
        if st.session_state.current_scenario_id:
            current_scenario = st.session_state.scenario_manager.get_scenario(
                st.session_state.current_scenario_id
            )
            current_idx = next(
                (i for i, s in enumerate(scenarios) if s["id"] == st.session_state.current_scenario_id),
                0
            )
        else:
            current_idx = 0
        
        selected_scenario_name = st.sidebar.selectbox(
            "Active Scenario",
            scenario_names,
            index=current_idx
        )
        
        # Find selected scenario ID
        selected_scenario = next(s for s in scenarios if s["name"] == selected_scenario_name)
        st.session_state.current_scenario_id = selected_scenario["id"]
        
        # Comparison scenarios
        st.sidebar.markdown("**Compare With:**")
        comparison_names = st.sidebar.multiselect(
            "Select scenarios",
            [s for s in scenario_names if s != selected_scenario_name],
            default=[]
        )
        
        st.session_state.comparison_scenario_ids = [
            s["id"] for s in scenarios if s["name"] in comparison_names
        ]
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📝 Input Data", "🔧 Scenarios"])
    
    with tab1:
        # Analysis tab
        if st.session_state.current_scenario_id:
            # Get current scenario
            current_scenario = st.session_state.scenario_manager.get_scenario(
                st.session_state.current_scenario_id
            )
            
            # Get comparison scenarios
            comparison_scenarios = [
                st.session_state.scenario_manager.get_scenario(sid)
                for sid in st.session_state.comparison_scenario_ids
            ]
            
            # Render selected layout
            if st.session_state.layout_mode == "epoch_tabs":
                render_epoch_tabs_layout(current_scenario, comparison_scenarios)
            elif st.session_state.layout_mode == "multi_panel":
                render_multi_panel_dashboard(current_scenario, comparison_scenarios)
            else:  # single_chart
                render_single_dynamic_chart(current_scenario, comparison_scenarios)
        else:
            st.info("No scenario selected. Please create a scenario in the Input Data tab.")
    
    with tab2:
        # Input data tab
        st.header("Input Data")
        
        # Collect user data
        user_data = collect_user_data()
        
        # Save/Update scenario buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            scenario_name = st.text_input(
                "Scenario Name",
                value=f"Scenario {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
        
        with col2:
            if st.button("Calculate & Save", type="primary"):
                # Create new scenario
                scenario_id = st.session_state.scenario_manager.create_scenario(
                    scenario_name,
                    user_data,
                    preset
                )
                st.session_state.current_scenario_id = scenario_id
                st.success(f"Scenario '{scenario_name}' saved!")
                st.rerun()
        
        with col3:
            if st.session_state.current_scenario_id and st.button("Update Current"):
                # Update existing scenario
                st.session_state.scenario_manager.update_scenario(
                    st.session_state.current_scenario_id,
                    user_data
                )
                st.success("Scenario updated!")
                st.rerun()
    
    with tab3:
        # Scenarios tab
        st.header("Scenario Management")
        
        # Quick scenario creation
        st.subheader("Quick Scenarios")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Create Physiologic TRT Reference"):
                ref_data = create_physiologic_reference_scenario()
                scenario_id = st.session_state.scenario_manager.create_scenario(
                    "Physiologic TRT Reference",
                    ref_data,
                    preset
                )
                st.success("Physiologic TRT reference scenario created!")
                st.rerun()
        
        with col2:
            if st.button("Create High-Risk Reference"):
                ref_data = create_high_risk_reference_scenario()
                scenario_id = st.session_state.scenario_manager.create_scenario(
                    "High-Risk Reference",
                    ref_data,
                    preset
                )
                st.success("High-risk reference scenario created!")
                st.rerun()
        
        # Scenario list
        st.subheader("Saved Scenarios")
        scenarios = st.session_state.scenario_manager.list_scenarios()
        
        if scenarios:
            for scenario in scenarios:
                with st.expander(f"{scenario['name']} - {scenario['category'].upper()}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("ASCVD Risk", f"{scenario['ascvd_risk']:.1f}%")
                    
                    with col2:
                        st.metric("Interventions", scenario['intervention_count'])
                    
                    with col3:
                        if st.button("Clone", key=f"clone_{scenario['id']}"):
                            new_id = st.session_state.scenario_manager.clone_scenario(
                                scenario['id'],
                                f"{scenario['name']} (Copy)"
                            )
                            st.success("Scenario cloned!")
                            st.rerun()
                    
                    with col4:
                        if st.button("Delete", key=f"delete_{scenario['id']}"):
                            st.session_state.scenario_manager.delete_scenario(scenario['id'])
                            if st.session_state.current_scenario_id == scenario['id']:
                                st.session_state.current_scenario_id = None
                            st.success("Scenario deleted!")
                            st.rerun()
        else:
            st.info("No scenarios saved yet. Create one in the Input Data tab.")
    
    # Handle export requests
    if hasattr(st.session_state, 'export_requested') and st.session_state.export_requested:
        if st.session_state.current_scenario_id:
            export_data = export_scenario(
                st.session_state.scenario_manager,
                st.session_state.current_scenario_id,
                st.session_state.export_format
            )
            
            if export_data:
                st.download_button(
                    label=f"Download {st.session_state.export_format}",
                    data=export_data['content'],
                    file_name=export_data['filename'],
                    mime=export_data['mime_type']
                )
        
        st.session_state.export_requested = False
    
    # Handle model card display
    if hasattr(st.session_state, 'show_model_card') and st.session_state.show_model_card:
        with st.expander("Model Card", expanded=True):
            try:
                with open("model_card.md", "r") as f:
                    st.markdown(f.read())
            except FileNotFoundError:
                st.warning("Model card not found.")
        
        st.session_state.show_model_card = False


if __name__ == "__main__":
    main()