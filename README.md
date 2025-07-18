# AAS Risk Reduction Tool

> **⚠️ EARLY PROTOTYPE DISCLAIMER**  
> This is an **experimental proof-of-concept** generated as a single development iteration. It serves as a **starting point for future development** rather than a production-ready application. The risk model, calculations, UI design, and overall implementation require significant refinement, validation, and expert review before any real-world application.

A prototype web application for modeling and visualizing health risks associated with Anabolic-Androgenic Steroid (AAS) use, with interactive scenario comparison and intervention analysis.

## 🚧 Development Status

**Current State: Early Prototype (v0.1.0)**

This codebase represents:
- ✅ **Architectural foundation** - Modular structure ready for enhancement
- ✅ **Feature demonstration** - Core functionality implemented
- ❌ **Production readiness** - Requires extensive development and validation
- ❌ **Clinical accuracy** - Risk calculations need medical expert review
- ❌ **UI polish** - Interface needs significant UX/UI improvements

## 🎯 Purpose & Vision

**Intended Vision:** A comprehensive framework for understanding how AAS compounds, dosages, cycles, and mitigation strategies might affect lifetime health risks across multiple domains, designed for educational harm-reduction purposes.

**Current Reality:** A functional prototype demonstrating the concept, with placeholder risk calculations, basic UI implementation, and minimal validation.

## ⚠️ Critical Limitations

### Scientific Limitations
- **Unvalidated Risk Model:** All risk multipliers are heuristic estimates, not clinically validated
- **Placeholder Calculations:** Baseline risks and intervention effects require expert review
- **No Medical Oversight:** Developed without clinical supervision or peer review
- **Limited Evidence Base:** Risk relationships based on incomplete literature synthesis

### Technical Limitations  
- **Basic UI Implementation:** Interface design needs professional UX/UI development
- **Minimal Testing:** Limited validation of calculations and edge cases
- **No Production Features:** Missing authentication, proper data validation, security measures
- **Performance Issues:** Not optimized for scale or concurrent users

### Operational Limitations
- **Educational Use Only:** Absolutely not for medical decision-making
- **No Support:** Prototype-level documentation and error handling
- **Rapid Development:** Code quality reflects single-iteration development constraints

## 🔮 Future Development Roadmap

This prototype establishes the foundation for a more robust application. Key development priorities include:

### Phase 1: Scientific Validation
- [ ] **Clinical Expert Review** - Collaborate with endocrinologists, cardiologists, and sports medicine physicians
- [ ] **Literature Review** - Comprehensive systematic review of AAS health effects
- [ ] **Risk Model Validation** - Statistical validation against real-world outcomes data
- [ ] **Uncertainty Quantification** - Proper confidence intervals and sensitivity analysis

### Phase 2: Technical Enhancement
- [ ] **Professional UI/UX Design** - Complete interface redesign with user research
- [ ] **Robust Backend** - Database integration, API development, security implementation
- [ ] **Comprehensive Testing** - Unit tests, integration tests, user acceptance testing
- [ ] **Performance Optimization** - Scalability, caching, and optimization

### Phase 3: Production Features
- [ ] **User Management** - Authentication, authorization, data privacy
- [ ] **Clinical Integration** - EHR compatibility, healthcare provider tools
- [ ] **Regulatory Compliance** - Medical device regulations, data protection
- [ ] **Quality Assurance** - Clinical validation, regulatory approval pathways

## 🚀 Quick Start (Prototype)

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Test the installation:
   ```bash
   python test_app.py
   python test_charts.py  # Optional: test chart rendering
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

6. Open your browser to `http://localhost:8501`

## 📊 Features

### Risk Modeling
- **14 Health Domains**: Cardiovascular, metabolic, organ systems, neuropsychiatric, cancer, endocrine, and dermatologic risks
- **Compound Normalization**: Testosterone equivalent (TE) calculations for consistent dosage comparison  
- **Exposure Metrics**: Weekly TE totals, recovery ratios, oral compound exposure tracking
- **Intervention Analysis**: 20+ mitigation strategies including lifestyle, medications, and protocol modifications

### Visualization Modes
- **Epoch Tabs**: Domain-organized tabs with gauges, waterfalls, and trajectory charts
- **Multi-Panel Dashboard**: Comprehensive overview with scenario comparison tables
- **Single Dynamic Chart**: Customizable charts with domain and scenario selection

### Scenario Management
- **Unlimited Scenarios**: Save and compare multiple risk profiles
- **Quick References**: Pre-built physiologic TRT and high-risk scenarios
- **Clone & Modify**: Easy A/B testing of interventions
- **Export Options**: JSON, CSV, PDF, and ZIP formats

### Plugin System
- **Extensible Architecture**: Custom risk factors and inputs
- **Example Plugins**: Enhanced fertility modeling template
- **Developer-Friendly**: Simple class or function-based plugin creation

## 🏗️ Architecture

```
AAS_Risk_Reduction_Tool/
├── app.py                     # Main Streamlit application
├── risk_model/               # Core risk calculation engine
│   ├── baseline_constants.py  # Domain risks and thresholds
│   ├── potency_table.py       # Compound potency factors
│   ├── multipliers.py         # Risk multiplier calculations
│   ├── calculator.py          # Core risk computation
│   ├── scenarios.py           # Scenario management
│   ├── event_free_years.py    # EFY calculations
│   └── plugin_loader.py       # Plugin system
├── ui/                       # User interface components
│   ├── forms.py              # Input forms
│   ├── charts.py             # Plotly visualizations
│   ├── badges.py             # Status indicators
│   └── layout.py             # Layout variants
├── presets/                  # Risk coefficient presets
│   ├── coefficients_conservative.yml
│   ├── coefficients_moderate.yml
│   └── coefficients_aggressive.yml
├── export/                   # Export functionality
├── plugins/                  # Plugin directory
└── docs/                    # Documentation
```

## 📝 Risk Model Overview

### Baseline Risks (Reference Male Population)
- **ASCVD**: 40% lifetime risk
- **Heart Failure**: 22%
- **Thrombosis**: 7%  
- **Type 2 Diabetes**: 33%
- **Hepatic Injury**: 3%
- **Renal Injury**: 3%
- **Neuropsychiatric**: 12%
- **Dementia**: 6%
- **Prostate Cancer**: 13%
- **Colorectal Cancer**: 4.2%
- **Endocrine Suppression**: 10%
- **Dermatologic**: 25%

### Risk Categories
- **🟢 Physiologic TRT**: ≤150mg/week TE, no orals
- **🟡 Moderate Enhancement**: 151-300mg TE and/or ≤8 weeks orals/year  
- **🔴 High-Risk**: >300mg TE, >8 weeks orals, recovery ratio <0.75, or Hct >54%

### Calculation Method
1. **Baseline Adjustment**: Apply protective factors (optimal lipids, fitness, diet, etc.)
2. **Exposure Metrics**: Calculate weekly TE, recovery ratios, oral exposure
3. **Risk Multipliers**: Apply compound, dosage, duration, and intervention multipliers
4. **Final Risk**: Absolute risk, relative risk vs. population, event-free years gained

## 🛠️ Usage Guide

### 1. Input Data Collection
- **Demographics**: Age, anthropometrics, vitals
- **Laboratory Values**: Lipids, metabolic markers, hormones
- **AAS Regimen**: Compounds, doses, timing, routes
- **Lifestyle**: Diet, exercise, sleep, substance use
- **Interventions**: Medications, monitoring, protocol modifications

### 2. Scenario Creation
- Enter your data in the "Input Data" tab
- Click "Calculate & Save" to create a scenario
- Use "Quick Scenarios" for reference comparisons

### 3. Analysis & Visualization  
- Switch between layout modes for different perspectives
- Compare up to 4 scenarios simultaneously
- Export results for documentation or sharing

### 4. Intervention Testing
- Clone existing scenarios to test "what-if" changes
- Modify interventions to see risk reduction potential
- Use waterfall charts to visualize intervention stacking

## 🔌 Plugin Development

Create custom plugins to extend the risk model:

### Class-Based Plugin
```python
from risk_model.plugin_loader import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "My Custom Plugin"
        self.version = "1.0.0"
    
    def get_new_multipliers(self, user_inputs):
        # Return dict of domain: [multipliers]
        return {"ascvd": [1.1], "diabetes": [0.9]}
    
    def additional_inputs(self):
        # Streamlit input widgets
        return {"my_plugin": {"custom_factor": st.checkbox("Custom Factor")}}
```

### Function-Based Plugin
```python
def register_plugin():
    return {
        "name": "My Plugin",
        "get_new_multipliers": lambda inputs: {"ascvd": [1.05]},
        "additional_inputs": lambda: {"factor": st.slider("Factor", 0, 10)}
    }
```

## 📊 Risk Presets

- **Conservative**: Dampened risk increases and mitigation benefits (50% of moderate)
- **Moderate**: Balanced assessment based on available evidence  
- **Aggressive**: Exaggerated effects (+30% distance from neutral)

Switch presets in the sidebar to explore uncertainty ranges.

## 💾 Export Formats

- **JSON**: Complete scenario data with metadata
- **CSV**: Tabular risk data for analysis
- **PDF**: Formatted report with charts (requires ReportLab)
- **ZIP**: All scenarios in multiple formats

## 🧪 Example Scenarios

### Physiologic TRT
- 140mg/week testosterone
- Regular monitoring
- Lifestyle optimization
- **Result**: Minimal risk elevation

### High-Risk Cycle
- 500mg testosterone + 300mg trenbolone + 50mg/day Anadrol
- 20-week duration, poor recovery
- **Result**: Significant risk elevation across multiple domains

### Optimized Enhancement
- Moderate doses with comprehensive interventions
- **Result**: Risk reduction through mitigation strategies

## 🔬 Model Limitations

- **Heuristic Multipliers**: Based on literature synthesis, not clinical validation
- **Individual Variation**: Population-level estimates may not reflect personal risk
- **Temporal Assumptions**: Simplified timeline modeling
- **Interaction Effects**: Limited modeling of complex drug-drug interactions
- **Mortality vs. Morbidity**: Mix of endpoints with different clinical significance

## 🤝 Contributing

We welcome contributions to improve the model:

1. **Data & Evidence**: Submit research supporting risk multiplier refinements
2. **Plugin Development**: Create domain-specific risk modules
3. **Validation Studies**: Propose validation methodologies
4. **Interface Improvements**: Enhance usability and accessibility
5. **Documentation**: Improve guides and explanations

### Contribution Process
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request with clear description
5. Ensure all checks pass

### Code Style
- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings for functions and classes
- Include unit tests for new functionality

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support & Feedback

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Additional guides available in `/docs`
- **Updates**: Check releases for new features and improvements

## 🙏 Acknowledgments

This tool synthesizes research from numerous studies on AAS health effects. While not a substitute for clinical guidance, it aims to support informed harm reduction decisions through transparent risk modeling.

---

**Disclaimer**: This tool is for educational purposes only. Risk estimates are based on heuristic models and should not replace professional medical advice. Always consult qualified healthcare providers for personalized risk assessment and management.