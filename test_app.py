"""Simple test script to validate AAS Risk Reduction Tool functionality."""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path.cwd()))

def test_core_functionality():
    """Test core risk model functionality."""
    print("🧪 Testing Core Functionality...")
    
    try:
        # Test imports
        from risk_model.baseline_constants import BASELINE_RISKS, MODEL_VERSION
        from risk_model.calculator import compute_domain_risks, create_physiologic_reference_scenario, create_high_risk_reference_scenario
        from risk_model.scenarios import ScenarioManager
        from risk_model.multipliers import load_preset_coefficients
        from export.exporter import export_scenario_json, export_scenario_csv
        
        print("✅ All imports successful")
        
        # Test preset loading
        for preset in ['conservative', 'moderate', 'aggressive']:
            coeffs = load_preset_coefficients(preset)
            assert len(coeffs) > 0, f"No coefficients loaded for {preset}"
        print("✅ All presets load successfully")
        
        # Test scenario creation and calculation
        sm = ScenarioManager()
        
        # Test physiologic scenario
        physio_data = create_physiologic_reference_scenario()
        physio_id = sm.create_scenario("Physiologic TRT", physio_data, "moderate")
        physio_scenario = sm.get_scenario(physio_id)
        
        # Verify physiologic scenario has reasonable risks
        ascvd_risk = physio_scenario["risks"]["ascvd"]["absolute_risk_pct"]
        assert 20 <= ascvd_risk <= 50, f"ASCVD risk {ascvd_risk}% seems unreasonable"
        print(f"✅ Physiologic TRT scenario: {ascvd_risk:.1f}% ASCVD risk")
        
        # Test high-risk scenario
        high_risk_data = create_high_risk_reference_scenario()
        high_risk_id = sm.create_scenario("High Risk", high_risk_data, "moderate")
        high_risk_scenario = sm.get_scenario(high_risk_id)
        
        # Verify high-risk scenario has higher risks
        high_ascvd_risk = high_risk_scenario["risks"]["ascvd"]["absolute_risk_pct"]
        assert high_ascvd_risk > ascvd_risk, "High-risk scenario should have higher ASCVD risk"
        print(f"✅ High-risk scenario: {high_ascvd_risk:.1f}% ASCVD risk")
        
        # Test scenario comparison
        comparison = sm.compare_scenarios([physio_id, high_risk_id])
        assert len(comparison["scenarios"]) == 2, "Should compare 2 scenarios"
        print("✅ Scenario comparison works")
        
        # Test exports
        json_export = export_scenario_json(sm, physio_id)
        assert len(json_export) > 1000, "JSON export seems too short"
        
        csv_export = export_scenario_csv(sm, physio_id)
        assert "Domain,Display_Name" in csv_export, "CSV header missing"
        print("✅ Export functionality works")
        
        # Test plugin system
        from risk_model.plugin_loader import PluginManager
        pm = PluginManager()
        plugins = pm.list_plugins()
        print(f"✅ Plugin system initialized ({len(plugins)} plugins loaded)")
        
        print(f"🎉 All core functionality tests passed!")
        print(f"   Model version: {MODEL_VERSION}")
        print(f"   Domains: {len(BASELINE_RISKS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Core functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_risk_calculations():
    """Test specific risk calculation scenarios."""
    print("\n🧮 Testing Risk Calculations...")
    
    try:
        from risk_model.calculator import compute_domain_risks
        
        # Test basic testosterone scenario
        basic_test = {
            "demographics": {"age": 30},
            "aas_regimen": [{
                "compound": "testosterone",
                "weekly_mg": 250,
                "start_week": 1,
                "duration_weeks": 12,
                "is_oral": False
            }],
            "labs": {"hdl": 45, "hematocrit": 48},
            "lifestyle": {"mediterranean_adherence": 5},
            "interventions": {}
        }
        
        risks = compute_domain_risks(basic_test, "moderate")
        
        # Verify reasonable results
        ascvd_rr = risks["ascvd"]["rr_vs_population"]
        assert 0.8 <= ascvd_rr <= 2.0, f"ASCVD RR {ascvd_rr} seems unreasonable"
        print(f"✅ Basic testosterone 250mg: RR {ascvd_rr:.2f}")
        
        # Test with interventions
        with_interventions = basic_test.copy()
        with_interventions["interventions"] = {
            "statin_intensity": "moderate",
            "vo2max_improvement": 5,
            "bodyfat_reduction": 5
        }
        
        intervention_risks = compute_domain_risks(with_interventions, "moderate")
        intervention_rr = intervention_risks["ascvd"]["rr_vs_population"]
        
        assert intervention_rr < ascvd_rr, "Interventions should reduce risk"
        print(f"✅ With interventions: RR {intervention_rr:.2f} (improvement)")
        
        # Test oral compounds
        oral_test = basic_test.copy()
        oral_test["aas_regimen"].append({
            "compound": "anadrol",
            "weekly_mg": 350,  # 50mg/day
            "start_week": 1,
            "duration_weeks": 6,
            "is_oral": True
        })
        
        oral_risks = compute_domain_risks(oral_test, "moderate")
        hepatic_rr = oral_risks["hepatic"]["rr_vs_population"]
        
        assert hepatic_rr > 1.1, "Oral compounds should increase hepatic risk"
        print(f"✅ With oral Anadrol: Hepatic RR {hepatic_rr:.2f}")
        
        print("🎉 Risk calculation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Risk calculation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_presets():
    """Test different risk presets."""
    print("\n⚙️ Testing Risk Presets...")
    
    try:
        from risk_model.calculator import compute_domain_risks
        
        test_data = {
            "demographics": {"age": 25},
            "aas_regimen": [{
                "compound": "testosterone",
                "weekly_mg": 500,
                "start_week": 1,
                "duration_weeks": 16,
                "is_oral": False
            }],
            "labs": {"hdl": 35, "hematocrit": 52},
            "lifestyle": {"mediterranean_adherence": 4},
        }
        
        results = {}
        for preset in ['conservative', 'moderate', 'aggressive']:
            risks = compute_domain_risks(test_data, preset)
            results[preset] = risks["ascvd"]["rr_vs_population"]
        
        # Conservative should be lowest, aggressive highest
        assert results['conservative'] <= results['moderate'] <= results['aggressive'], \
            "Preset ordering incorrect"
        
        print(f"✅ Conservative: RR {results['conservative']:.2f}")
        print(f"✅ Moderate: RR {results['moderate']:.2f}")
        print(f"✅ Aggressive: RR {results['aggressive']:.2f}")
        
        print("🎉 Preset tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Preset test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 AAS Risk Reduction Tool - Test Suite")
    print("=" * 50)
    
    results = []
    results.append(test_core_functionality())
    results.append(test_risk_calculations())
    results.append(test_presets())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 ALL TESTS PASSED! Application ready to run.")
        print("\nTo start the application, run:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print(f"Results: {sum(results)}/{len(results)} tests passed")
    
    return all(results)


if __name__ == "__main__":
    main()