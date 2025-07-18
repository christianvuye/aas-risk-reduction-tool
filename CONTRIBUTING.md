# Contributing to AAS Risk Reduction Tool

Thank you for your interest in contributing to the AAS Risk Reduction Tool! This document provides guidelines for contributing to the project.

## 🎯 Types of Contributions

We welcome several types of contributions:

### 1. Scientific Contributions
- **Literature Evidence**: New research supporting or refining risk multipliers
- **Clinical Data**: Real-world outcome data for model validation
- **Expert Review**: Clinical expert feedback on risk estimates and assumptions
- **Validation Studies**: Proposals for prospective validation research

### 2. Technical Contributions
- **Bug Fixes**: Fixing calculation errors, UI issues, or crashes
- **Feature Enhancements**: New visualization modes, export formats, or analysis tools
- **Performance Optimization**: Improving calculation speed or memory usage
- **Code Quality**: Refactoring, documentation, or test coverage improvements

### 3. Content Contributions
- **Plugin Development**: New risk domains or specialized modeling modules
- **Documentation**: Improving guides, tutorials, or model explanations
- **Internationalization**: Translations or region-specific adaptations
- **User Interface**: Improving usability, accessibility, or visual design

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Familiarity with Streamlit (for UI changes)
- Basic understanding of epidemiology/risk assessment (for model changes)

### Development Setup
1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/[your-username]/AAS_Risk_Reduction_Tool.git
   cd AAS_Risk_Reduction_Tool
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```
5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Contribution Process

### 1. Before You Start
- **Check existing issues** to see if your idea is already being worked on
- **Open a new issue** to discuss major changes before implementing
- **Read the model card** (`model_card.md`) to understand current assumptions
- **Review the architecture** in `README.md` to understand the codebase

### 2. Making Changes

#### Code Style Guidelines
- **Follow PEP 8** for Python code formatting
- **Use type hints** for function parameters and return values
- **Add docstrings** for all public functions and classes
- **Keep functions focused** on single responsibilities
- **Use descriptive variable names** and avoid abbreviations

#### Example of Good Code Style:
```python
def calculate_risk_multiplier(
    compound_name: str,
    weekly_dose_mg: float,
    duration_weeks: int
) -> float:
    """Calculate risk multiplier for a specific compound and dosage.
    
    Args:
        compound_name: Name of the AAS compound
        weekly_dose_mg: Weekly dosage in milligrams
        duration_weeks: Duration of use in weeks
        
    Returns:
        Risk multiplier (1.0 = no change, >1.0 = increased risk)
        
    Raises:
        ValueError: If dosage or duration are negative
    """
    if weekly_dose_mg < 0 or duration_weeks < 0:
        raise ValueError("Dosage and duration must be non-negative")
    
    # Implementation here...
    return multiplier
```

#### Testing Requirements
- **Add unit tests** for new functions using pytest
- **Include integration tests** for new features
- **Test edge cases** and error conditions
- **Verify calculations** manually for key scenarios

#### Documentation Requirements
- **Update README.md** for new features or architectural changes
- **Update model_card.md** for new risk domains or major assumption changes
- **Add inline comments** for complex calculation logic
- **Include examples** in docstrings where helpful

### 3. Scientific Contributions

#### Evidence Standards
When proposing changes to risk multipliers or baseline risks:

- **Cite peer-reviewed sources** with proper references
- **Provide confidence intervals** or uncertainty ranges when available
- **Explain methodology** used to derive the proposed values
- **Consider population differences** and generalizability

#### Evidence Quality Hierarchy
1. **Systematic reviews and meta-analyses** (highest quality)
2. **Large prospective cohort studies** (>1000 participants)
3. **Case-control studies** with appropriate controls
4. **Expert consensus** from recognized authorities
5. **Case series** or expert opinion (lowest quality)

#### Example Evidence Submission:
```yaml
# evidence/cardiovascular_update_2024.yml
domain: ascvd
multiplier_name: per_100mg_wte_over_150mg_26wks
current_value: 1.08
proposed_value: 1.12
confidence_interval: [1.05, 1.20]

sources:
  - citation: "Smith et al. (2024). Cardiovascular effects of supraphysiologic testosterone: A meta-analysis. JACC, 83(4), 123-135."
    study_type: "meta-analysis"
    sample_size: 15000
    effect_size: 1.12
    confidence_interval: [1.05, 1.20]
    
  - citation: "Jones et al. (2023). Long-term cardiovascular outcomes in testosterone users. Circulation, 147(8), 234-245."
    study_type: "prospective_cohort"
    sample_size: 3500
    follow_up_years: 10
    effect_size: 1.15
    confidence_interval: [1.02, 1.28]

rationale: |
  Recent meta-analysis with larger sample size and longer follow-up 
  suggests higher cardiovascular risk than previously estimated.
  
limitations: |
  Studies predominantly in middle-aged men. Limited data on 
  younger users or female populations.
```

### 4. Plugin Development

#### Plugin Standards
- **Follow the plugin template** in `plugins/example_plugin_template.py`
- **Use clear, descriptive names** for your plugin and its inputs
- **Provide help text** for all user inputs
- **Validate input ranges** and handle edge cases
- **Document your risk model** and cite sources for multipliers

#### Plugin Structure:
```python
class YourPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "Descriptive Plugin Name"
        self.version = "1.0.0"
        self.description = "Clear description of what this plugin models"
    
    def get_new_multipliers(self, user_inputs: Dict[str, Any]) -> Dict[str, List[float]]:
        """Calculate risk multipliers based on plugin logic."""
        # Implementation with clear documentation
        pass
    
    def additional_inputs(self) -> Dict[str, Any]:
        """Collect plugin-specific user inputs."""
        # Streamlit widgets with helpful labels and descriptions
        pass
```

## 🧪 Testing Your Changes

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=risk_model --cov-report=html

# Run specific test file
pytest tests/test_calculator.py

# Run the application locally
streamlit run app.py
```

### Manual Testing Checklist
- [ ] **Input Validation**: Test with invalid/extreme inputs
- [ ] **Calculation Accuracy**: Verify math with known examples  
- [ ] **UI Responsiveness**: Test with different screen sizes
- [ ] **Export Functions**: Test all export formats
- [ ] **Scenario Management**: Test saving, loading, and comparing scenarios
- [ ] **Plugin Integration**: Verify plugins load and function correctly

### Creating Test Cases
```python
import pytest
from risk_model.calculator import compute_domain_risks

def test_physiologic_trt_risk():
    """Test risk calculation for physiologic TRT scenario."""
    user_data = {
        "demographics": {"age": 40},
        "aas_regimen": [{
            "compound": "testosterone",
            "weekly_mg": 140,
            "duration_weeks": 52,
            "is_oral": False
        }]
    }
    
    risks = compute_domain_risks(user_data, "moderate")
    
    # Physiologic doses should have minimal risk elevation
    assert risks["ascvd"]["rr_vs_population"] < 1.1
    assert risks["ascvd"]["absolute_risk_pct"] > 0
```

## 📋 Pull Request Process

### 1. Before Submitting
- [ ] **All tests pass** locally
- [ ] **Code follows style guidelines**
- [ ] **Documentation is updated** as needed
- [ ] **Commit messages are clear** and descriptive
- [ ] **No debugging code** or temporary files included

### 2. Pull Request Template
When submitting a PR, please include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (would cause existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Scientific Justification (if applicable)
- Sources supporting risk multiplier changes
- Confidence intervals or uncertainty estimates
- Discussion of limitations

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes without major version bump
```

### 3. Review Process
- **Automatic checks** will run on your PR
- **At least one maintainer** will review your changes
- **Scientific changes** require review by clinical expert(s)
- **Breaking changes** require additional discussion and approval
- **Feedback incorporation** may require multiple review rounds

## 🔬 Scientific Review Process

### For Risk Model Changes
Major changes to baseline risks or multipliers undergo additional review:

1. **Initial Technical Review**: Code quality and implementation
2. **Scientific Review**: Clinical expert evaluation of evidence
3. **Model Validation**: Testing against known scenarios
4. **Documentation Update**: Model card and assumption updates
5. **Version Update**: Appropriate version increment

### Expert Reviewer Pool
We maintain a pool of clinical experts for scientific review:
- Endocrinologists with AAS experience
- Cardiologists familiar with AAS effects
- Sports medicine physicians
- Epidemiologists and biostatisticians

## 🐛 Reporting Issues

### Bug Reports
Use the GitHub issue template and include:
- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs. actual behavior**
- **Screenshots** if applicable
- **System information** (OS, Python version, browser)
- **Input data** that caused the issue (anonymized)

### Feature Requests
Include:
- **Use case description** and motivation
- **Proposed solution** or implementation ideas
- **Alternatives considered**
- **Scientific justification** for model changes

## 📚 Resources

### Learning Resources
- **Epidemiology Basics**: Understanding risk, relative risk, and absolute risk
- **Streamlit Documentation**: For UI development
- **Plotly Documentation**: For visualization improvements
- **AAS Literature**: Key papers on health effects and risk assessment

### Useful Tools
- **Black**: Python code formatter
- **Flake8**: Linting and style checking
- **MyPy**: Type checking
- **Pytest**: Testing framework
- **Jupyter**: For data analysis and visualization prototyping

## 🤝 Community Guidelines

### Code of Conduct
- **Be respectful** and professional in all interactions
- **Focus on the science** and evidence, not personal opinions
- **Welcome newcomers** and help them contribute effectively
- **Acknowledge contributions** and give credit where due
- **Maintain confidentiality** of any personal health information

### Communication Channels
- **GitHub Issues**: Bug reports, feature requests, technical discussions
- **Pull Request Comments**: Code review and implementation details
- **Discussions**: General questions and community interaction

## 🎉 Recognition

Contributors are recognized in several ways:
- **Contributor list** in README.md
- **Changelog entries** for significant contributions
- **Co-authorship consideration** for major scientific contributions
- **Plugin attribution** for plugin developers

Thank you for contributing to evidence-based harm reduction tools!

---

**Questions?** Open an issue or start a discussion. We're here to help make your contribution successful.