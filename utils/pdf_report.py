# utils/pdf_report.py
import os
import unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# ------------------------------
# Unicode font register
# Arial Unicode destekli bir font örneği
# arialuni.ttf dosyasını projenin kök dizinine koymalısınız
pdfmetrics.registerFont(TTFont('ArialUnicode', 'arialuni.ttf'))


# ------------------------------

def normalize_text(text: str) -> str:
    """Ensure text is Unicode normalized (avoid broken characters in PDF)."""
    return unicodedata.normalize('NFC', str(text))


def create_pdf_report(result_data: dict):
    """
    Create a professional PDF report of the code analysis with Unicode support.

    Sections:
    1. Title
    2. File Path
    3. Suggestions / Recommendations
    4. PEP8 Issues
    5. Security Warnings
    6. Code Metrics
    7. Final Score
    """

    # Create reports directory if not exists
    os.makedirs("reports", exist_ok=True)
    file_name = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(
        file_name,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    styles = getSampleStyleSheet()
    story = []

    # Custom styles using Unicode font
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], fontName='ArialUnicode', fontSize=24, leading=28)
    section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontName='ArialUnicode', fontSize=18,
                                   leading=22)
    normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontName='ArialUnicode', fontSize=12,
                                  leading=15)

    # Title
    story.append(Paragraph("PyClear - Code Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # --- File Path ---
    file_path = normalize_text(result_data.get("file_path", "Unknown file"))
    story.append(Paragraph(f"Analyzed File: {file_path}", normal_style))
    story.append(Spacer(1, 12))

    # --- Suggestions ---
    story.append(Paragraph("Suggestions / Recommendations", section_style))
    story.append(Spacer(1, 6))
    suggestions = result_data.get("suggestions", [])
    if suggestions:
        for s in suggestions:
            story.append(Paragraph(f"• {normalize_text(s)}", normal_style))
    else:
        story.append(Paragraph("No suggestions.", normal_style))
    story.append(Spacer(1, 12))

    # --- PEP8 Issues ---
    story.append(Paragraph("PEP8 Issues", section_style))
    story.append(Spacer(1, 6))
    pep8_issues = result_data.get("pep8_issues", [])
    if pep8_issues:
        for issue in pep8_issues:
            story.append(Paragraph(f"• {normalize_text(issue)}", normal_style))
    else:
        story.append(Paragraph("No PEP8 issues found.", normal_style))
    story.append(Spacer(1, 12))

    # --- Security Warnings ---
    story.append(Paragraph("Security Warnings", section_style))
    story.append(Spacer(1, 6))
    security_issues = result_data.get("security_issues", [])
    if security_issues:
        for s in security_issues:
            story.append(Paragraph(f"• {normalize_text(s)}", normal_style))
    else:
        story.append(Paragraph("No security warnings found.", normal_style))
    story.append(Spacer(1, 12))

    # --- Code Metrics Table ---
    story.append(Paragraph("Code Metrics", section_style))
    story.append(Spacer(1, 6))
    metrics = result_data.get("metrics", {})
    if metrics:
        data = [["Metric", "Value"]]
        for k, v in metrics.items():
            data.append([normalize_text(k), normalize_text(v)])
        table = Table(data, hAlign='LEFT', colWidths=[200, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, -1), 'ArialUnicode')
        ]))
        story.append(table)
    else:
        story.append(Paragraph("No metrics found.", normal_style))
    story.append(Spacer(1, 12))

    # --- Final Score ---
    final_score = result_data.get('final_score', 0)
    story.append(Paragraph(f"Final Score: {final_score}/100", section_style))

    # Build PDF
    doc.build(story)
    print(f"✅ PDF created: {file_name}")
