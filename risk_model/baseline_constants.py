"""Baseline lifetime risk constants for various health domains."""

MODEL_VERSION = "1.0.0"

# Baseline lifetime risks for reference male population (approximate)
BASELINE_RISKS = {
    "ascvd": 0.40,  # ASCVD (coronary + ischemic stroke): 40% baseline
    "hf": 0.22,  # Cardiomyopathy / Heart Failure: 22%
    "thrombosis": 0.07,  # Clinically significant VTE/arterial thrombosis: 7%
    "ischemic_stroke": 0.22,  # Ischemic Stroke (component of ASCVD): 22%
    "hemorrhagic_stroke": 0.012,  # Hemorrhagic Stroke: 1.2%
    "hepatic": 0.03,  # Hepatic clinically relevant injury: 3%
    "renal": 0.03,  # Renal clinically significant injury: 3%
    "neuro": 0.12,  # Neuro/Mood/Psychiatric: 12%
    "diabetes": 0.33,  # Type 2 Diabetes: 33%
    "dementia": 0.06,  # Dementia/Alzheimer's: 6%
    "cancer_colorectal": 0.042,  # Colorectal cancer: 4.2%
    "cancer_prostate": 0.13,  # Prostate cancer diagnosis: 13%
    "endocrine": 0.10,  # Endocrine suppression/fertility impairment: 10%
    "dermatologic": 0.25,  # Severe acne/alopecia progression: 25%
}

# Average age of first event for each domain (used for event-free years calculation)
AVERAGE_EVENT_AGE = {
    "ascvd": 65,
    "hf": 70,
    "thrombosis": 60,
    "ischemic_stroke": 70,
    "hemorrhagic_stroke": 65,
    "hepatic": 55,
    "renal": 60,
    "neuro": 45,
    "diabetes": 55,
    "dementia": 75,
    "cancer_colorectal": 65,
    "cancer_prostate": 65,
    "endocrine": 35,
    "dermatologic": 30,
}

# Risk category thresholds
PHYSIOLOGIC_THRESHOLD_MG = 150  # mg/week testosterone equivalent

# Risk badge thresholds (relative risk vs population)
RISK_BADGE_THRESHOLDS = {
    "reduced": 0.75,
    "average_low": 1.25,
    "elevated_low": 1.75,
}

# Protective factor adjustments for personalized baseline
PROTECTIVE_FACTOR_ADJUSTMENTS = {
    "ldl_optimal": {"ascvd": 0.75, "ischemic_stroke": 0.80},  # LDL ≤70
    "vo2max_excellent": {"ascvd": 0.80, "hf": 0.75, "diabetes": 0.70},  # VO2max >50
    "bodyfat_optimal": {"ascvd": 0.85, "diabetes": 0.65, "hf": 0.85},  # BF ≤15%
    "diet_excellent": {"ascvd": 0.85, "cancer_colorectal": 0.80, "dementia": 0.85},  # Mediterranean ≥8
    "non_smoker": {"ascvd": 0.90, "cancer_colorectal": 0.90, "dementia": 0.95},
    "osa_treated": {"ascvd": 0.90, "hf": 0.85, "diabetes": 0.90},
}

# Domain display names
DOMAIN_DISPLAY_NAMES = {
    "ascvd": "ASCVD",
    "hf": "Heart Failure",
    "thrombosis": "Thrombosis",
    "ischemic_stroke": "Ischemic Stroke",
    "hemorrhagic_stroke": "Hemorrhagic Stroke",
    "hepatic": "Hepatic Injury",
    "renal": "Renal Injury",
    "neuro": "Neuro/Psychiatric",
    "diabetes": "Type 2 Diabetes",
    "dementia": "Dementia",
    "cancer_colorectal": "Colorectal Cancer",
    "cancer_prostate": "Prostate Cancer",
    "endocrine": "Endocrine Suppression",
    "dermatologic": "Dermatologic",
}

# Domain categories for UI organization
DOMAIN_CATEGORIES = {
    "Cardiovascular": ["ascvd", "hf", "thrombosis", "ischemic_stroke", "hemorrhagic_stroke"],
    "Metabolic": ["diabetes"],
    "Organ Systems": ["hepatic", "renal"],
    "Neuropsychiatric": ["neuro", "dementia"],
    "Cancer": ["cancer_colorectal", "cancer_prostate"],
    "Endocrine": ["endocrine"],
    "Dermatologic": ["dermatologic"],
}