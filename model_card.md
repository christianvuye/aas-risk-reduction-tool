# AAS Risk Reduction Tool - Model Card

## Model Overview

**Model Name**: AAS Risk Reduction Tool  
**Version**: 1.0.0  
**Last Updated**: 2024-01-20  
**Model Type**: Heuristic Risk Assessment Framework  

## Purpose & Scope

### Intended Use
This model provides educational risk assessment for anabolic-androgenic steroid (AAS) use across multiple health domains. It is designed for:

- **Harm reduction education**: Understanding relative risk changes with different protocols
- **Intervention planning**: Evaluating mitigation strategies  
- **Scenario comparison**: A/B testing of protocol modifications
- **Academic research**: Transparent framework for risk modeling discussions

### Intended Users
- Healthcare providers counseling AAS users
- Researchers studying AAS health effects
- Individuals seeking evidence-based harm reduction information
- Public health professionals developing intervention programs

### Out-of-Scope Uses
- **Clinical diagnosis**: Not a diagnostic tool for health conditions
- **Treatment decisions**: Does not replace medical evaluation and treatment
- **Legal guidance**: No guidance on legal aspects of AAS use
- **Precise individual prediction**: Population-level estimates, not personal guarantees

## Model Architecture

### Risk Domains (14 Total)
1. **Cardiovascular**
   - ASCVD (40% baseline lifetime risk)
   - Heart Failure (22% baseline)
   - Thrombosis (7% baseline)
   - Ischemic Stroke (22% baseline)  
   - Hemorrhagic Stroke (1.2% baseline)

2. **Metabolic**
   - Type 2 Diabetes (33% baseline)

3. **Organ Systems**
   - Hepatic Injury (3% baseline)
   - Renal Injury (3% baseline)

4. **Neuropsychiatric**
   - Neuro/Mood/Psychiatric (12% baseline)
   - Dementia (6% baseline)

5. **Cancer**
   - Colorectal Cancer (4.2% baseline)
   - Prostate Cancer (13% baseline)

6. **Endocrine**
   - Endocrine Suppression/Fertility (10% baseline)

7. **Dermatologic**
   - Severe Acne/Androgenic Alopecia (25% baseline)

### Calculation Framework

```
Final Risk = Baseline Risk × Protective Factors × Σ(Exposure Multipliers × Intervention Multipliers)
```

**Step 1: Baseline Adjustment**
- Apply protective factor reductions for optimal health metrics
- Examples: LDL ≤70 (-25% ASCVD), VO2max >50 (-20% CV risk)

**Step 2: Exposure Metrics**
- Weekly Testosterone Equivalent (WTE) normalization across compounds
- Recovery ratio calculation (weeks at physiologic / weeks supra-physiologic)
- Oral 17-alpha alkylated compound exposure tracking

**Step 3: Risk Multipliers**
- Compound-specific potency factors (Trenbolone 2.0x, Primobolan 0.8x)
- Dose-response relationships (per 100mg WTE over 150mg threshold)
- Duration and frequency penalties
- Stacking interaction effects

**Step 4: Intervention Benefits**
- Lifestyle modifications (diet, exercise, sleep optimization)
- Monitoring and early intervention (lipid management, hematocrit control)
- Pharmacological interventions (statins, GLP-1 agonists, etc.)
- Protocol modifications (compound substitution, dose reduction)

## Data Sources & Assumptions

### Baseline Risk Sources
- **Cardiovascular**: Framingham Heart Study, AHA/ACC guidelines, meta-analyses
- **Cancer**: SEER database, epidemiological studies
- **Metabolic**: CDC diabetes statistics, longitudinal cohort studies
- **Neuropsychiatric**: Population-based psychiatric epidemiology

### Risk Multiplier Derivation

**Literature-Derived** (Strong Evidence):
- Cardiovascular effects of supraphysiologic testosterone
- Oral 17-AA hepatotoxicity patterns
- Hematocrit and thrombotic risk relationships

**Expert Synthesis** (Moderate Evidence):
- Compound-specific potency comparisons
- Intervention efficacy estimates
- Dose-response curve modeling

**Heuristic Estimates** (Limited Evidence):
- Novel compound risk profiles
- Complex intervention interactions
- Long-term outcome projections

### Key Assumptions

1. **Linear Risk Scaling**: Risk increases proportionally with exposure intensity
2. **Multiplicative Interactions**: Risk factors multiply rather than add
3. **Population Homogeneity**: Same baseline risks apply across users
4. **Intervention Independence**: Benefits combine without antagonism
5. **Temporal Stability**: Risk relationships constant over time
6. **Recovery Completeness**: Full risk normalization possible with cessation

## Model Limitations

### Scientific Limitations
- **Limited Longitudinal Data**: Few long-term studies on AAS health outcomes
- **Publication Bias**: Overrepresentation of adverse effects in literature
- **Dose-Response Uncertainty**: Limited data on high-dose, long-duration effects
- **Individual Variation**: Genetic and metabolic factors not incorporated
- **Interaction Complexity**: Simplified modeling of multi-drug protocols

### Technical Limitations
- **Static Coefficients**: Risk multipliers don't adapt to new evidence automatically
- **Discrete Time Modeling**: Simplified timeline representation
- **Missing Domains**: Some health effects not captured (sleep, mood, etc.)
- **Validation Gap**: No prospective validation studies completed

### Operational Limitations
- **User Input Quality**: Relies on accurate self-reported data
- **Interpretation Complexity**: Requires understanding of relative vs. absolute risk
- **Update Frequency**: Manual coefficient updates as new evidence emerges

## Uncertainty & Calibration

### Uncertainty Quantification
- **Standard Uncertainty Bands**: ±15% relative uncertainty on all risk estimates
- **Preset Variation**: Conservative/Moderate/Aggressive presets span reasonable ranges
- **Sensitivity Analysis**: Plugin system allows testing alternative assumptions

### Calibration Status
- **Face Validity**: Expert review of coefficient reasonableness
- **Internal Consistency**: Logical relationships between domains and interventions
- **External Validation**: Not yet validated against real-world outcomes

### Known Biases
- **Severity Bias**: May overestimate rare but severe outcomes
- **Intervention Optimism**: May overestimate mitigation effectiveness
- **Population Mismatch**: Male reference population may not represent all users

## Ethical Considerations

### Potential Benefits
- **Informed Decision Making**: Transparent risk information supports autonomy
- **Harm Reduction**: Identifies most effective risk mitigation strategies
- **Research Advancement**: Standardized framework for comparing interventions
- **Clinical Support**: Assists healthcare providers in counseling users

### Potential Harms
- **False Reassurance**: Conservative estimates may encourage risky behavior
- **Anxiety Induction**: Risk visualization may cause disproportionate concern
- **Misinterpretation**: Complex risk concepts may be misunderstood
- **Liability Concerns**: Inappropriate use for medical decision-making

### Mitigation Strategies
- **Clear Disclaimers**: Prominent educational-only warnings
- **Professional Guidance**: Encouragement to consult healthcare providers
- **Uncertainty Communication**: Explicit discussion of model limitations
- **Regular Updates**: Incorporation of new evidence as available

## Governance & Maintenance

### Model Versioning
- **Major Versions**: Fundamental architecture changes
- **Minor Versions**: Coefficient updates, new domains/interventions
- **Patch Versions**: Bug fixes, UI improvements

### Update Process
1. **Evidence Review**: Quarterly literature scanning
2. **Expert Consultation**: Annual review with clinical experts
3. **User Feedback**: Continuous collection via GitHub issues
4. **Validation Studies**: Planned prospective validation research

### Quality Assurance
- **Code Review**: All changes reviewed by multiple developers
- **Testing Suite**: Automated tests for calculation consistency
- **Documentation**: Maintained change log and version history

## Version History

### Version 1.0.0 (2024-01-20)
- Initial release with 14 health domains
- Three preset coefficient sets (Conservative/Moderate/Aggressive)
- Plugin system for extensibility
- Export functionality (JSON/CSV/PDF)
- Streamlit-based interactive interface

### Planned Updates
- **v1.1**: Enhanced cardiovascular sub-modeling
- **v1.2**: Genetics integration (APOE, thrombophilia)
- **v1.3**: Temporal risk modeling improvements
- **v2.0**: Machine learning coefficient optimization

## Contact & Support

**Development Team**: AAS Risk Reduction Tool Contributors  
**Repository**: GitHub.com/[repository-url]  
**Issues**: GitHub Issues for bug reports and feature requests  
**Documentation**: README.md and inline code documentation  

**Medical Disclaimer**: This model is for educational purposes only and does not constitute medical advice. Always consult qualified healthcare providers for personalized risk assessment and management decisions.

---

*Last Updated: January 20, 2024*  
*Next Review: April 20, 2024*