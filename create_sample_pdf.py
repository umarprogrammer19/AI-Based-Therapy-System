#!/usr/bin/env python3
"""
Simple script to create a proper PDF with ketamine therapy information.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime

def create_ketamine_info_pdf(filename="ketamine_therapy_info.pdf"):
    """Create a PDF with ketamine therapy information."""

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    # Container for the 'Flowable' objects
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )

    # Title
    title = Paragraph("Ketamine Therapy Information", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Introduction
    intro_text = """
    Ketamine therapy is an innovative treatment primarily used for treatment-resistant depression (TRD)
    and other mental health conditions. It works differently from traditional antidepressants by targeting
    the glutamate system in the brain. The treatment has shown promising results for patients who
    haven't responded to other therapies.
    """
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 12))

    # Benefits section
    elements.append(Paragraph("Benefits of Ketamine Therapy", heading_style))

    benefits = [
        "Rapid onset of action (hours to days vs. weeks for traditional antidepressants)",
        "Effectiveness in patients who haven't responded to other treatments",
        "Potential for reducing suicidal ideation quickly",
        "Relatively short treatment duration"
    ]

    for benefit in benefits:
        elements.append(Paragraph(f"• {benefit}", body_style))

    elements.append(Paragraph(
        "Many patients experience significant mood improvements after just a few sessions.",
        body_style
    ))
    elements.append(Spacer(1, 12))

    # Treatment Process section
    elements.append(Paragraph("Treatment Process", heading_style))

    process_text = """
    Ketamine therapy sessions typically involve intravenous (IV) infusions lasting about 40-60 minutes.
    Patients are monitored continuously by medical professionals. A typical course consists of 6 infusions
    over 2-3 weeks, though this varies by individual. During the infusion, patients may experience
    dissociative effects, which are normal and temporary. Most patients begin to notice improvements
    after 2-3 sessions. Follow-up sessions may be recommended based on individual response.
    """
    elements.append(Paragraph(process_text, body_style))
    elements.append(Spacer(1, 12))

    # Potential Side Effects section
    elements.append(Paragraph("Potential Side Effects", heading_style))

    side_effects_text = """
    Like any medical treatment, ketamine therapy has potential side effects. Common side effects
    may include dissociation, dizziness, nausea, increased blood pressure, and temporary perceptual
    changes during the infusion. These effects are typically mild and resolve shortly after the
    infusion ends. Serious side effects are rare when administered by trained professionals in
    a controlled medical setting. Your healthcare provider will discuss all potential risks
    and benefits with you before treatment.
    """
    elements.append(Paragraph(side_effects_text, body_style))
    elements.append(Spacer(1, 12))

    # Scientific Background
    elements.append(Paragraph("Scientific Background", heading_style))

    science_text = """
    Ketamine acts as an N-methyl-D-aspartate (NMDA) receptor antagonist, which is fundamentally
    different from traditional monoaminergic antidepressants. This mechanism allows for rapid
    synaptic plasticity changes and the formation of new neural pathways. Clinical studies have
    demonstrated significant efficacy in treating major depressive episodes in patients with
    treatment-resistant depression, with response rates often exceeding 70% in clinical trials.

    The therapy is typically administered in sub-anesthetic doses under medical supervision,
    ensuring patient safety while maximizing therapeutic benefit. Treatment protocols are
    individualized based on patient response and tolerance.
    """
    elements.append(Paragraph(science_text, body_style))
    elements.append(Spacer(1, 12))

    # Footer
    footer_text = f"Document generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(footer_text, styles['Italic']))

    # Build the PDF
    doc.build(elements)
    print(f"PDF created successfully: {filename}")

if __name__ == "__main__":
    create_ketamine_info_pdf("sample_ketamine_therapy_info.pdf")