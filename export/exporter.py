"""Export functionality for scenarios and reports."""

import json
import csv
from io import StringIO, BytesIO
import zipfile
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from risk_model.scenarios import ScenarioManager
from risk_model.baseline_constants import DOMAIN_DISPLAY_NAMES


def export_scenario_json(scenario_manager: ScenarioManager, scenario_id: str) -> str:
    """Export scenario to JSON format.
    
    Args:
        scenario_manager: Scenario manager instance
        scenario_id: Scenario ID to export
        
    Returns:
        JSON string
    """
    scenario = scenario_manager.get_scenario(scenario_id)
    
    # Create export data structure
    export_data = {
        "metadata": {
            "export_date": datetime.now().isoformat(),
            "tool_name": "AAS Risk Reduction Tool",
            "model_version": scenario.get("preset", "moderate"),
        },
        "scenario": {
            "name": scenario.get("name", "Unknown"),
            "id": scenario.get("id", ""),
            "created_at": scenario.get("created_at", ""),
            "category": scenario.get("category", "unknown"),
            "preset": scenario.get("preset", "moderate"),
        },
        "user_data": scenario.get("user_data", {}),
        "exposure_metrics": scenario.get("exposure_metrics", {}),
        "risks": scenario.get("risks", {}),
        "interventions": scenario.get("interventions", []),
    }
    
    return json.dumps(export_data, indent=2, default=str)


def export_scenario_csv(scenario_manager: ScenarioManager, scenario_id: str) -> str:
    """Export scenario to CSV format.
    
    Args:
        scenario_manager: Scenario manager instance
        scenario_id: Scenario ID to export
        
    Returns:
        CSV string
    """
    scenario = scenario_manager.get_scenario(scenario_id)
    risks = scenario.get("risks", {})
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Domain",
        "Display_Name", 
        "Absolute_Risk_Percent",
        "RR_vs_Population",
        "RR_vs_Physio",
        "Event_Free_Years",
        "Active_Multipliers_Count"
    ])
    
    # Write risk data
    for domain, risk_data in risks.items():
        writer.writerow([
            domain,
            DOMAIN_DISPLAY_NAMES.get(domain, domain),
            f"{risk_data.get('absolute_risk_pct', 0):.2f}",
            f"{risk_data.get('rr_vs_population', 1):.3f}",
            f"{risk_data.get('rr_vs_physio', 1):.3f}",
            f"{risk_data.get('event_free_years', 0):.1f}",
            len(risk_data.get('active_multipliers', []))
        ])
    
    # Add scenario metadata
    output.write("\n# Scenario Metadata\n")
    writer.writerow(["Scenario_Name", scenario.get("name", "Unknown")])
    writer.writerow(["Category", scenario.get("category", "unknown")])
    writer.writerow(["Preset", scenario.get("preset", "moderate")])
    writer.writerow(["Export_Date", datetime.now().isoformat()])
    
    # Add interventions
    output.write("\n# Active Interventions\n")
    for intervention in scenario.get("interventions", []):
        writer.writerow(["Intervention", intervention])
    
    return output.getvalue()


def export_scenario_pdf(scenario_manager: ScenarioManager, scenario_id: str) -> Optional[bytes]:
    """Export scenario to PDF format.
    
    Args:
        scenario_manager: Scenario manager instance
        scenario_id: Scenario ID to export
        
    Returns:
        PDF bytes if successful, None if ReportLab not available
    """
    if not REPORTLAB_AVAILABLE:
        return None
    
    scenario = scenario_manager.get_scenario(scenario_id)
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph("AAS Risk Reduction Tool - Risk Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Scenario information
    scenario_info = [
        ["Scenario Name:", scenario.get("name", "Unknown")],
        ["Category:", scenario.get("category", "unknown").upper()],
        ["Risk Preset:", scenario.get("preset", "moderate").capitalize()],
        ["Export Date:", datetime.now().strftime("%Y-%m-%d %H:%M")],
    ]
    
    scenario_table = Table(scenario_info, colWidths=[2*inch, 3*inch])
    scenario_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTWEIGHT', (0, 0), (0, -1), 'BOLD'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(scenario_table)
    story.append(Spacer(1, 20))
    
    # Risk summary table
    story.append(Paragraph("Risk Summary", styles['Heading2']))
    
    risks = scenario.get("risks", {})
    risk_data = [["Domain", "Absolute Risk (%)", "RR vs Population", "Event-Free Years"]]
    
    for domain, risk_info in risks.items():
        risk_data.append([
            DOMAIN_DISPLAY_NAMES.get(domain, domain),
            f"{risk_info.get('absolute_risk_pct', 0):.1f}%",
            f"{risk_info.get('rr_vs_population', 1):.2f}x",
            f"{risk_info.get('event_free_years', 0):.1f}"
        ])
    
    risk_table = Table(risk_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    risk_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTWEIGHT', (0, 0), (-1, 0), 'BOLD'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ]))
    
    story.append(risk_table)
    story.append(Spacer(1, 20))
    
    # Interventions
    interventions = scenario.get("interventions", [])
    if interventions:
        story.append(Paragraph("Active Interventions", styles['Heading2']))
        
        for intervention in interventions:
            story.append(Paragraph(f"• {intervention}", styles['Normal']))
        
        story.append(Spacer(1, 20))
    
    # Disclaimer
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.red,
        leftIndent=20,
        rightIndent=20,
    )
    
    story.append(Paragraph(
        "<b>Disclaimer:</b> This is a prototype heuristic model for educational purposes only. "
        "Risk calculations are not clinically validated. Always consult healthcare professionals "
        "for medical decisions.",
        disclaimer_style
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def export_all_scenarios_zip(scenario_manager: ScenarioManager) -> bytes:
    """Export all scenarios as a ZIP file.
    
    Args:
        scenario_manager: Scenario manager instance
        
    Returns:
        ZIP file bytes
    """
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        scenarios = scenario_manager.list_scenarios()
        
        for scenario in scenarios:
            scenario_id = scenario["id"]
            scenario_name = scenario["name"].replace(" ", "_").replace("/", "_")
            
            # Add JSON
            json_data = export_scenario_json(scenario_manager, scenario_id)
            zip_file.writestr(f"{scenario_name}.json", json_data)
            
            # Add CSV
            csv_data = export_scenario_csv(scenario_manager, scenario_id)
            zip_file.writestr(f"{scenario_name}.csv", csv_data)
            
            # Add PDF if available
            if REPORTLAB_AVAILABLE:
                pdf_data = export_scenario_pdf(scenario_manager, scenario_id)
                if pdf_data:
                    zip_file.writestr(f"{scenario_name}.pdf", pdf_data)
        
        # Add summary CSV
        summary_data = export_scenarios_summary_csv(scenario_manager)
        zip_file.writestr("scenarios_summary.csv", summary_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def export_scenarios_summary_csv(scenario_manager: ScenarioManager) -> str:
    """Export summary of all scenarios to CSV.
    
    Args:
        scenario_manager: Scenario manager instance
        
    Returns:
        CSV string
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Scenario_Name",
        "Category", 
        "Preset",
        "ASCVD_Risk_Percent",
        "HF_Risk_Percent",
        "Thrombosis_Risk_Percent",
        "Diabetes_Risk_Percent",
        "Intervention_Count",
        "Created_Date"
    ])
    
    # Write scenario data
    scenarios = scenario_manager.list_scenarios()
    for scenario_summary in scenarios:
        scenario = scenario_manager.get_scenario(scenario_summary["id"])
        risks = scenario.get("risks", {})
        
        writer.writerow([
            scenario.get("name", "Unknown"),
            scenario.get("category", "unknown"),
            scenario.get("preset", "moderate"),
            f"{risks.get('ascvd', {}).get('absolute_risk_pct', 0):.1f}",
            f"{risks.get('hf', {}).get('absolute_risk_pct', 0):.1f}",
            f"{risks.get('thrombosis', {}).get('absolute_risk_pct', 0):.1f}",
            f"{risks.get('diabetes', {}).get('absolute_risk_pct', 0):.1f}",
            len(scenario.get("interventions", [])),
            scenario.get("created_at", "")
        ])
    
    return output.getvalue()


def export_scenario(
    scenario_manager: ScenarioManager, 
    scenario_id: str, 
    format: str
) -> Optional[Dict[str, Any]]:
    """Export scenario in specified format.
    
    Args:
        scenario_manager: Scenario manager instance
        scenario_id: Scenario ID to export
        format: Export format (JSON, CSV, PDF, ZIP)
        
    Returns:
        Dictionary with content, filename, and mime_type, or None if failed
    """
    scenario = scenario_manager.get_scenario(scenario_id)
    scenario_name = scenario.get("name", "scenario").replace(" ", "_")
    
    if format.upper() == "JSON":
        content = export_scenario_json(scenario_manager, scenario_id)
        return {
            "content": content,
            "filename": f"{scenario_name}.json",
            "mime_type": "application/json"
        }
    
    elif format.upper() == "CSV":
        content = export_scenario_csv(scenario_manager, scenario_id)
        return {
            "content": content,
            "filename": f"{scenario_name}.csv",
            "mime_type": "text/csv"
        }
    
    elif format.upper() == "PDF":
        if REPORTLAB_AVAILABLE:
            content = export_scenario_pdf(scenario_manager, scenario_id)
            if content:
                return {
                    "content": content,
                    "filename": f"{scenario_name}.pdf",
                    "mime_type": "application/pdf"
                }
        return None
    
    elif format.upper() == "ZIP (ALL)" or format.upper() == "ZIP":
        content = export_all_scenarios_zip(scenario_manager)
        return {
            "content": content,
            "filename": f"aas_risk_scenarios_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
            "mime_type": "application/zip"
        }
    
    return None