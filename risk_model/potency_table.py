"""Compound potency factors for testosterone equivalent (TE) normalization."""

# Potency factors relative to testosterone (testosterone = 1.0)
COMPOUND_POTENCY = {
    # Injectable compounds
    "testosterone": 1.0,
    "testosterone_enanthate": 1.0,
    "testosterone_cypionate": 1.0,
    "testosterone_propionate": 1.0,
    "testosterone_undecanoate": 1.0,
    "sustanon": 1.0,
    
    # High potency compounds
    "trenbolone": 2.0,
    "trenbolone_acetate": 2.0,
    "trenbolone_enanthate": 2.0,
    
    # Moderate potency compounds
    "nandrolone": 1.2,
    "nandrolone_decanoate": 1.2,
    "nandrolone_phenylpropionate": 1.2,
    "boldenone": 1.1,
    "boldenone_undecylenate": 1.1,
    "masteron": 1.1,
    "drostanolone_propionate": 1.1,
    "drostanolone_enanthate": 1.1,
    
    # Mild compounds
    "primobolan": 0.8,
    "methenolone_enanthate": 0.8,
    "methenolone_acetate": 0.8,
    
    # Oral compounds (still get potency factor, but treated separately)
    "oxandrolone": 0.9,
    "anavar": 0.9,
    "winstrol": 1.0,
    "stanozolol": 1.0,
    "anadrol": 1.5,
    "oxymetholone": 1.5,
    "dianabol": 1.3,
    "methandrostenolone": 1.3,
    "turinabol": 1.0,
    "halotestin": 2.5,
    "fluoxymesterone": 2.5,
    "superdrol": 2.0,
    "methyldrostanolone": 2.0,
    
    # Other
    "custom": 1.0,  # Default for unlisted compounds
}

# Oral 17-alpha alkylated compounds
ORAL_17AA_COMPOUNDS = {
    "oxandrolone", "anavar", "winstrol", "stanozolol", "anadrol", 
    "oxymetholone", "dianabol", "methandrostenolone", "turinabol",
    "halotestin", "fluoxymesterone", "superdrol", "methyldrostanolone"
}

# DHT-derived compounds (for dermatologic risk)
DHT_DERIVED_COMPOUNDS = {
    "masteron", "drostanolone_propionate", "drostanolone_enanthate",
    "primobolan", "methenolone_enanthate", "methenolone_acetate",
    "winstrol", "stanozolol", "anavar", "oxandrolone",
    "halotestin", "fluoxymesterone"
}

# Heavy compounds (for replacement strategies)
HEAVY_COMPOUNDS = {
    "trenbolone", "trenbolone_acetate", "trenbolone_enanthate",
    "anadrol", "oxymetholone", "halotestin", "fluoxymesterone",
    "superdrol", "methyldrostanolone"
}

# Mild compounds (for replacement strategies)
MILD_COMPOUNDS = {
    "primobolan", "methenolone_enanthate", "methenolone_acetate",
    "oxandrolone", "anavar", "boldenone", "boldenone_undecylenate"
}


def get_potency_factor(compound_name: str) -> float:
    """Get the potency factor for a compound.
    
    Args:
        compound_name: Name of the compound (case-insensitive)
        
    Returns:
        Potency factor relative to testosterone
    """
    normalized_name = compound_name.lower().replace(" ", "_").replace("-", "_")
    return COMPOUND_POTENCY.get(normalized_name, COMPOUND_POTENCY["custom"])


def is_oral_17aa(compound_name: str) -> bool:
    """Check if a compound is an oral 17-alpha alkylated compound.
    
    Args:
        compound_name: Name of the compound (case-insensitive)
        
    Returns:
        True if compound is oral 17-aa
    """
    normalized_name = compound_name.lower().replace(" ", "_").replace("-", "_")
    return normalized_name in ORAL_17AA_COMPOUNDS


def is_dht_derived(compound_name: str) -> bool:
    """Check if a compound is DHT-derived.
    
    Args:
        compound_name: Name of the compound (case-insensitive)
        
    Returns:
        True if compound is DHT-derived
    """
    normalized_name = compound_name.lower().replace(" ", "_").replace("-", "_")
    return normalized_name in DHT_DERIVED_COMPOUNDS


def is_heavy_compound(compound_name: str) -> bool:
    """Check if a compound is considered 'heavy'.
    
    Args:
        compound_name: Name of the compound (case-insensitive)
        
    Returns:
        True if compound is heavy
    """
    normalized_name = compound_name.lower().replace(" ", "_").replace("-", "_")
    return normalized_name in HEAVY_COMPOUNDS


def is_mild_compound(compound_name: str) -> bool:
    """Check if a compound is considered 'mild'.
    
    Args:
        compound_name: Name of the compound (case-insensitive)
        
    Returns:
        True if compound is mild
    """
    normalized_name = compound_name.lower().replace(" ", "_").replace("-", "_")
    return normalized_name in MILD_COMPOUNDS


def calculate_weekly_te(compound_name: str, weekly_mg: float) -> float:
    """Calculate weekly testosterone equivalent.
    
    Args:
        compound_name: Name of the compound
        weekly_mg: Weekly dosage in mg
        
    Returns:
        Weekly testosterone equivalent in mg
    """
    potency = get_potency_factor(compound_name)
    return weekly_mg * potency