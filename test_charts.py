"""Test chart creation to verify the color parsing fix."""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path.cwd()))

def test_chart_creation():
    """Test that all chart types can be created without color parsing errors."""
    print("🧪 Testing Chart Creation...")
    
    try:
        from ui.charts import (
            create_risk_trajectory_chart, create_risk_gauge, 
            create_waterfall_chart, create_radar_chart, create_domain_bar_chart
        )
        from risk_model.scenarios import ScenarioManager
        from risk_model.calculator import create_physiologic_reference_scenario, create_high_risk_reference_scenario
        
        # Create test scenarios
        sm = ScenarioManager()
        
        # Physiologic scenario
        physio_data = create_physiologic_reference_scenario()
        physio_id = sm.create_scenario("Physiologic", physio_data, "moderate")
        physio_scenario = sm.get_scenario(physio_id)
        
        # High-risk scenario
        high_data = create_high_risk_reference_scenario()
        high_id = sm.create_scenario("High Risk", high_data, "moderate")
        high_scenario = sm.get_scenario(high_id)
        
        scenarios = [physio_scenario, high_scenario]
        
        # Test trajectory chart (this was the problematic one)
        print("  📈 Testing risk trajectory chart...")
        fig_trajectory = create_risk_trajectory_chart(
            scenarios=scenarios,
            domains=['ascvd', 'hf', 'thrombosis'],
            current_age=30
        )
        print(f"    ✅ Created with {len(fig_trajectory.data)} traces")
        
        # Test gauge chart
        print("  📊 Testing risk gauge chart...")
        fig_gauge = create_risk_gauge("ascvd", physio_scenario["risks"]["ascvd"])
        print(f"    ✅ Created gauge chart")
        
        # Test waterfall chart
        print("  📉 Testing waterfall chart...")
        interventions = [
            {"name": "Statin", "impact": -0.05},
            {"name": "Exercise", "impact": -0.03}
        ]
        fig_waterfall = create_waterfall_chart(
            "ascvd", 0.40, interventions, 0.32
        )
        print(f"    ✅ Created waterfall chart")
        
        # Test radar chart
        print("  🎯 Testing radar chart...")
        fig_radar = create_radar_chart(physio_scenario["risks"])
        print(f"    ✅ Created radar chart")
        
        # Test bar chart
        print("  📊 Testing domain bar chart...")
        fig_bar = create_domain_bar_chart(physio_scenario["risks"])
        print(f"    ✅ Created bar chart")
        
        print("🎉 All chart creation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Chart creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_chart_creation()
    if success:
        print("\n✅ Chart creation fix verified - application should work without color errors!")
    else:
        print("\n❌ Chart creation issues detected - please check the errors above.")