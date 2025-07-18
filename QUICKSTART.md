# Quick Start Guide

## Installation & Setup (5 minutes)

1. **Ensure Python 3.8+ is installed**
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation**
   ```bash
   python test_app.py
   ```
   You should see "🎉 ALL TESTS PASSED!"

5. **Start the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser to** `http://localhost:8501`

## Quick Tour (10 minutes)

### 1. Create Your First Scenario
- Go to the **"Input Data"** tab
- Fill in basic demographics (age, weight, etc.)
- Add at least one AAS compound in the regimen section
- Click **"Calculate & Save"**

### 2. View Your Risk Analysis
- Switch to the **"Analysis"** tab  
- Your risk profile will display with:
  - **Risk category badge** (Physiologic/Moderate/High-Risk)
  - **Domain-specific risks** across 14 health areas
  - **Interactive charts** showing risk trajectories

### 3. Compare Scenarios
- Create a second scenario with different parameters
- Use the sidebar to select comparison scenarios
- See side-by-side risk comparisons

### 4. Test Interventions
- In the "Input Data" tab, enable various interventions
- Save as a new scenario or update existing
- See how interventions reduce risks in real-time

## Example Scenarios to Try

### Physiologic TRT
- Age: 45
- Testosterone: 140mg/week for 52 weeks
- Good labs and lifestyle
- **Expected**: Green "Physiologic TRT" badge

### Moderate Cycle
- Age: 30  
- Testosterone: 250mg/week for 12 weeks
- Standard labs
- **Expected**: Yellow "Moderate Enhancement" badge

### High-Risk Stack
- Age: 25
- Testosterone: 500mg/week + Trenbolone: 300mg/week
- Anadrol: 50mg/day for 6 weeks
- Poor recovery ratio
- **Expected**: Red "High-Risk" badge

## Key Features to Explore

### Layout Modes (Sidebar)
- **Epoch Tabs**: Domain-organized detailed analysis
- **Multi-Panel Dashboard**: Overview with comparisons
- **Single Dynamic Chart**: Customizable visualizations

### Risk Presets (Sidebar)
- **Conservative**: Lower risk estimates
- **Moderate**: Balanced assessment  
- **Aggressive**: Higher risk estimates

### Export Options (Sidebar)
- **JSON**: Complete scenario data
- **CSV**: Tabular risk summary
- **PDF**: Formatted report (requires ReportLab)
- **ZIP**: All formats combined

### Interventions to Test
- **Lifestyle**: VO2max improvement, body fat reduction
- **Medications**: Statins, GLP-1 agonists, metformin
- **Monitoring**: Hematocrit management, lipid control
- **Protocol**: Eliminate orals, replace heavy compounds

## Understanding the Results

### Risk Metrics
- **Absolute Risk**: Lifetime probability (e.g., 45% ASCVD risk)
- **Relative Risk**: Compared to general population (e.g., 1.2x higher)
- **Event-Free Years**: Years of life gained by reducing risk

### Risk Categories
- **🟢 Physiologic**: ≤150mg/week TE, minimal elevation
- **🟡 Moderate**: 151-300mg TE, manageable with interventions  
- **🔴 High-Risk**: >300mg TE or other high-risk factors

### Chart Types
- **Gauge**: Current absolute risk level
- **Waterfall**: Step-by-step intervention impacts
- **Line**: Risk trajectory over time
- **Radar**: Multi-domain risk profile
- **Bar**: Domain comparison

## Tips for Effective Use

1. **Start Simple**: Begin with basic scenarios before complex stacks
2. **Compare Systematically**: Use A/B testing for interventions
3. **Focus on Major Risks**: Prioritize cardiovascular and hepatic domains
4. **Consider Uncertainty**: Use different presets to explore ranges
5. **Export for Records**: Save scenarios for future reference

## Common Questions

**Q: Are these risks clinically validated?**
A: No, this is a heuristic educational model. Always consult healthcare providers.

**Q: Why do some interventions show large benefits?**
A: The model may be optimistic about intervention effects. Real-world results vary.

**Q: Can I add custom compounds?**
A: Yes, use "custom" in the compound list and manually set potency.

**Q: How accurate are the baseline risks?**
A: Based on population averages for reference males. Individual variation is significant.

## Next Steps

- **Read the full README.md** for detailed documentation
- **Review the Model Card** for assumptions and limitations
- **Try the plugin system** for specialized modeling
- **Export scenarios** for discussion with healthcare providers

**Remember**: This tool is for educational harm reduction only, not medical advice.

## Need Help?

- **Check the Model Card** for detailed methodology
- **Review CONTRIBUTING.md** for technical details
- **Open GitHub Issues** for bugs or feature requests
- **Run test_app.py** if something seems broken

Happy modeling! 🧬📊