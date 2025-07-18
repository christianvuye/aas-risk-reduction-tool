"""Form components for user input."""

import streamlit as st
from typing import Dict, List, Any, Optional
from risk_model.potency_table import COMPOUND_POTENCY


def render_demographics_form() -> Dict[str, Any]:
    """Render demographics and anthropometrics form.
    
    Returns:
        Dictionary of demographic data
    """
    st.subheader("Demographics & Anthropometrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
        sex = st.selectbox("Sex", ["male", "female"], index=0)
        height_cm = st.number_input("Height (cm)", min_value=120, max_value=250, value=178, step=1)
        weight_kg = st.number_input("Weight (kg)", min_value=40, max_value=200, value=85, step=1)
    
    with col2:
        body_fat_pct = st.number_input("Body Fat %", min_value=3.0, max_value=50.0, value=18.0, step=0.5)
        waist_cm = st.number_input("Waist (cm)", min_value=50, max_value=150, value=85, step=1)
    
    return {
        "demographics": {
            "age": age,
            "sex": sex,
        },
        "anthropometrics": {
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "body_fat_pct": body_fat_pct,
            "waist_cm": waist_cm,
        }
    }


def render_vitals_performance_form() -> Dict[str, Any]:
    """Render vitals and performance form.
    
    Returns:
        Dictionary of vitals and performance data
    """
    st.subheader("Vitals & Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        systolic = st.number_input("Systolic BP", min_value=80, max_value=200, value=125, step=1)
        diastolic = st.number_input("Diastolic BP", min_value=40, max_value=130, value=80, step=1)
        resting_hr = st.number_input("Resting HR", min_value=35, max_value=120, value=65, step=1)
    
    with col2:
        vo2max_method = st.selectbox("VO2max Entry Method", ["Direct", "12-min run", "Beep test"])
        
        if vo2max_method == "Direct":
            vo2max = st.number_input("VO2max (ml/kg/min)", min_value=15.0, max_value=90.0, value=42.0, step=0.5)
        elif vo2max_method == "12-min run":
            distance_m = st.number_input("12-min run distance (meters)", min_value=1000, max_value=4000, value=2400, step=50)
            vo2max = (distance_m - 504.9) / 44.73  # Cooper formula
        else:  # Beep test
            level = st.number_input("Beep Test Level", min_value=1, max_value=21, value=10, step=1)
            shuttle = st.number_input("Beep Test Shuttle", min_value=1, max_value=16, value=5, step=1)
            vo2max = 3.46 * (level + shuttle / (level * 0.4325 + 7.0048)) + 12.2  # Approximate formula
        
        steps_day = st.number_input("Steps/day", min_value=0, max_value=50000, value=8000, step=500)
    
    return {
        "vitals": {
            "systolic_bp": systolic,
            "diastolic_bp": diastolic,
            "resting_hr": resting_hr,
        },
        "performance": {
            "vo2max": vo2max,
            "steps_day": steps_day,
        }
    }


def render_labs_form() -> Dict[str, Any]:
    """Render laboratory values form.
    
    Returns:
        Dictionary of lab data
    """
    st.subheader("Laboratory Values")
    
    with st.expander("Lipids", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            ldl = st.number_input("LDL (mg/dL)", min_value=20, max_value=300, value=100, step=1)
            hdl = st.number_input("HDL (mg/dL)", min_value=15, max_value=100, value=45, step=1)
            tg = st.number_input("Triglycerides (mg/dL)", min_value=30, max_value=1000, value=120, step=5)
        with col2:
            apob = st.number_input("ApoB (mg/dL)", min_value=30, max_value=200, value=90, step=1, help="Optional")
            lpa = st.number_input("Lp(a) (mg/dL)", min_value=0, max_value=200, value=20, step=1, help="Optional")
    
    with st.expander("Metabolic & Organ Function"):
        col1, col2 = st.columns(2)
        with col1:
            hematocrit = st.number_input("Hematocrit (%)", min_value=30.0, max_value=65.0, value=45.0, step=0.5)
            glucose = st.number_input("Fasting Glucose (mg/dL)", min_value=50, max_value=300, value=95, step=1)
            a1c = st.number_input("HbA1c (%)", min_value=4.0, max_value=15.0, value=5.4, step=0.1)
        with col2:
            ast = st.number_input("AST (U/L)", min_value=5, max_value=500, value=25, step=1)
            alt = st.number_input("ALT (U/L)", min_value=5, max_value=500, value=22, step=1)
            egfr = st.number_input("eGFR (mL/min/1.73m²)", min_value=15, max_value=150, value=90, step=1)
    
    with st.expander("Hormones & Markers"):
        col1, col2 = st.columns(2)
        with col1:
            total_t = st.number_input("Total Testosterone (ng/dL)", min_value=100, max_value=2000, value=500, step=10)
            estradiol = st.number_input("Estradiol (pg/mL)", min_value=5, max_value=200, value=30, step=1)
        with col2:
            psa = st.number_input("PSA (ng/mL)", min_value=0.0, max_value=20.0, value=1.0, step=0.1)
            vitamin_d = st.number_input("25(OH)D (ng/mL)", min_value=5, max_value=100, value=35, step=1)
    
    return {
        "labs": {
            "ldl": ldl,
            "hdl": hdl,
            "triglycerides": tg,
            "apob": apob,
            "lpa": lpa,
            "hematocrit": hematocrit,
            "glucose": glucose,
            "a1c": a1c,
            "ast": ast,
            "alt": alt,
            "egfr": egfr,
            "total_testosterone": total_t,
            "estradiol": estradiol,
            "psa": psa,
            "vitamin_d": vitamin_d,
        }
    }


def render_genetics_form() -> Dict[str, Any]:
    """Render genetics form.
    
    Returns:
        Dictionary of genetic data
    """
    st.subheader("Genetics (Optional)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        apoe_genotype = st.selectbox(
            "APOE Genotype", 
            ["Unknown", "E2/E2", "E2/E3", "E2/E4", "E3/E3", "E3/E4", "E4/E4"],
            index=0
        )
    
    with col2:
        factor_v = st.checkbox("Factor V Leiden")
        prothrombin = st.checkbox("Prothrombin Mutation")
    
    return {
        "genetics": {
            "apoe_genotype": apoe_genotype,
            "factor_v_leiden": factor_v,
            "prothrombin_mutation": prothrombin,
        }
    }


def render_aas_regimen_form() -> List[Dict[str, Any]]:
    """Render AAS regimen input form.
    
    Returns:
        List of compound data
    """
    st.subheader("AAS Regimen")
    
    if "aas_compounds" not in st.session_state:
        st.session_state.aas_compounds = []
    
    # Add compound button
    if st.button("Add Compound"):
        st.session_state.aas_compounds.append({
            "compound": "testosterone",
            "route": "injectable",
            "weekly_mg": 250,
            "start_week": 1,
            "duration_weeks": 12,
            "is_oral": False,
        })
    
    # Display compounds
    compounds_to_remove = []
    
    for idx, compound_data in enumerate(st.session_state.aas_compounds):
        with st.expander(f"Compound {idx + 1}", expanded=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                # Compound selection
                compound_list = sorted(COMPOUND_POTENCY.keys())
                compound_idx = compound_list.index(compound_data.get("compound", "testosterone"))
                compound = st.selectbox(
                    "Compound",
                    compound_list,
                    index=compound_idx,
                    key=f"compound_{idx}"
                )
                
                route = st.selectbox(
                    "Route",
                    ["injectable", "oral"],
                    index=0 if compound_data.get("route") == "injectable" else 1,
                    key=f"route_{idx}"
                )
                
                weekly_mg = st.number_input(
                    "Weekly Dose (mg)",
                    min_value=0,
                    max_value=2000,
                    value=compound_data.get("weekly_mg", 250),
                    step=25,
                    key=f"dose_{idx}"
                )
            
            with col2:
                start_week = st.number_input(
                    "Start Week",
                    min_value=1,
                    max_value=52,
                    value=compound_data.get("start_week", 1),
                    step=1,
                    key=f"start_{idx}"
                )
                
                duration = st.number_input(
                    "Duration (weeks)",
                    min_value=1,
                    max_value=52,
                    value=compound_data.get("duration_weeks", 12),
                    step=1,
                    key=f"duration_{idx}"
                )
            
            with col3:
                st.write("")  # Spacer
                st.write("")  # Spacer
                if st.button("Remove", key=f"remove_{idx}"):
                    compounds_to_remove.append(idx)
            
            # Update compound data
            st.session_state.aas_compounds[idx] = {
                "compound": compound,
                "route": route,
                "weekly_mg": weekly_mg,
                "start_week": start_week,
                "duration_weeks": duration,
                "is_oral": route == "oral",
            }
    
    # Remove compounds
    for idx in reversed(compounds_to_remove):
        st.session_state.aas_compounds.pop(idx)
    
    # Past cycles info
    st.subheader("Past Cycle History")
    col1, col2 = st.columns(2)
    
    with col1:
        past_cycles = st.number_input(
            "Cycles in past 5 years",
            min_value=0,
            max_value=50,
            value=0,
            step=1
        )
    
    with col2:
        longest_continuous = st.number_input(
            "Longest continuous supra-physiologic (weeks)",
            min_value=0,
            max_value=260,
            value=0,
            step=4
        )
    
    return {
        "aas_regimen": st.session_state.aas_compounds,
        "past_cycles": past_cycles,
        "longest_continuous": longest_continuous,
    }


def render_lifestyle_form() -> Dict[str, Any]:
    """Render lifestyle factors form.
    
    Returns:
        Dictionary of lifestyle data
    """
    st.subheader("Lifestyle Factors")
    
    with st.expander("Diet & Exercise", expanded=True):
        mediterranean = st.slider(
            "Mediterranean Diet Adherence (0-10)",
            min_value=0,
            max_value=10,
            value=5,
            step=1
        )
        
        col1, col2 = st.columns(2)
        with col1:
            moderate_aerobic = st.number_input(
                "Moderate Aerobic (min/week)",
                min_value=0,
                max_value=1000,
                value=150,
                step=30
            )
            vigorous_aerobic = st.number_input(
                "Vigorous Aerobic (min/week)",
                min_value=0,
                max_value=500,
                value=75,
                step=15
            )
        
        with col2:
            resistance_sets = st.number_input(
                "Resistance Training (sets/week)",
                min_value=0,
                max_value=200,
                value=40,
                step=5
            )
            sleep_hours = st.number_input(
                "Average Sleep (hours)",
                min_value=3.0,
                max_value=12.0,
                value=7.0,
                step=0.5
            )
    
    with st.expander("Health Conditions & Habits"):
        osa_status = st.selectbox(
            "Sleep Apnea Status",
            ["none", "untreated", "treated", "resolved"],
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            alcohol_occasions = st.number_input(
                "Alcohol (occasions/month)",
                min_value=0,
                max_value=100,
                value=4,
                step=1
            )
            smoking = st.checkbox("Current Smoker/Vaper")
        
        with col2:
            st.write("Recreational Drugs (times/year):")
            cocaine = st.number_input("Cocaine", min_value=0, max_value=365, value=0, step=1)
            mdma = st.number_input("MDMA", min_value=0, max_value=365, value=0, step=1)
            cannabis = st.number_input("Cannabis", min_value=0, max_value=365, value=0, step=1)
    
    return {
        "lifestyle": {
            "mediterranean_adherence": mediterranean,
            "moderate_aerobic_min": moderate_aerobic,
            "vigorous_aerobic_min": vigorous_aerobic,
            "resistance_sets_week": resistance_sets,
            "sleep_hours": sleep_hours,
            "osa_status": osa_status,
            "alcohol_occasions_month": alcohol_occasions,
            "smoking": smoking,
            "recreational_drugs": {
                "cocaine_per_year": cocaine,
                "mdma_per_year": mdma,
                "cannabis_per_year": cannabis,
            }
        }
    }


def render_interventions_form() -> Dict[str, Any]:
    """Render mitigation interventions form.
    
    Returns:
        Dictionary of intervention data
    """
    st.subheader("Mitigation Interventions")
    
    with st.expander("AAS Modifications", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            maintain_hct = st.checkbox("Maintain Hematocrit <52%")
            eliminate_orals = st.checkbox("Eliminate Oral Compounds")
            replace_heavy = st.checkbox("Replace Heavy with Mild Compounds")
        
        with col2:
            dose_reduction_hct = st.checkbox("Dose Reduction for Hematocrit")
            blood_donation = st.checkbox("Blood Donation Only (no dose reduction)")
    
    with st.expander("Lifestyle Improvements"):
        vo2_improvement = st.select_slider(
            "VO2max Improvement Target (ml/kg/min)",
            options=[0, 5, 10],
            value=0
        )
        
        bf_reduction = st.select_slider(
            "Body Fat Reduction Target (%)",
            options=[0, 5, 10],
            value=0
        )
        
        diet_high = st.checkbox("High Mediterranean Diet Adherence (≥8)")
        osa_treated = st.checkbox("Treat Sleep Apnea")
    
    with st.expander("Medications"):
        col1, col2 = st.columns(2)
        
        with col1:
            statin_intensity = st.selectbox(
                "Statin Intensity",
                ["none", "low", "moderate", "high"],
                index=0
            )
            ezetimibe = st.checkbox("Ezetimibe")
            pcsk9 = st.checkbox("PCSK9 Inhibitor")
            omega3 = st.checkbox("High-Purity Omega-3")
            glp1 = st.checkbox("GLP-1/GIP Agonist")
        
        with col2:
            metformin = st.checkbox("Metformin")
            pde5_daily = st.checkbox("PDE5 Inhibitor Daily")
            finasteride = st.checkbox("Finasteride/Dutasteride")
            serm_pct = st.checkbox("SERM Post-Cycle")
            hcg = st.checkbox("HCG Support")
    
    with st.expander("Other"):
        ai_excess = st.checkbox("Aromatase Inhibitor Excess Use", help="Adds penalty")
    
    return {
        "interventions": {
            "maintain_hct_below_52": maintain_hct,
            "eliminate_orals": eliminate_orals,
            "replace_heavy_mild": replace_heavy,
            "dose_reduction_hct": dose_reduction_hct,
            "blood_donation_only": blood_donation,
            "vo2max_improvement": vo2_improvement,
            "bodyfat_reduction": bf_reduction,
            "diet_high_adherence": diet_high,
            "osa_treated": osa_treated,
            "statin_intensity": statin_intensity,
            "ezetimibe": ezetimibe,
            "pcsk9": pcsk9,
            "omega3": omega3,
            "glp1_agonist": glp1,
            "metformin": metformin,
            "pde5_daily": pde5_daily,
            "finasteride": finasteride,
            "serm_pct": serm_pct,
            "hcg": hcg,
            "ai_excess": ai_excess,
        }
    }