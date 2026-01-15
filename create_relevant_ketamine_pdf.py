#!/usr/bin/env python3
"""
Script to create a PDF with highly relevant ketamine therapy keywords.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime

def create_highly_relevant_ketamine_pdf(filename="highly_relevant_ketamine_info.pdf"):
    """Create a PDF with highly relevant ketamine therapy keywords."""

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
    title = Paragraph("KETAMINE THERAPY: TREATMENT-RESISTANT DEPRESSION", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Strong opening with keywords
    intro_text = """
    KETAMINE THERAPY represents a breakthrough in treating treatment-resistant depression (TRD).
    This psychiatric intervention targets NMDA receptors and glutamate systems in the brain,
    offering rapid relief for patients who have not responded to traditional antidepressants.
    Clinical evidence demonstrates significant efficacy in ketamine treatment for depression.
    """
    elements.append(Paragraph(intro_text, body_style))
    elements.append(Spacer(1, 12))

    # Keywords-focused sections
    elements.append(Paragraph("KEY BENEFITS OF KETAMINE THERAPY", heading_style))

    benefits = [
        "RAPID ONSET: Relief within hours to days, not weeks like traditional antidepressants",
        "EFFECTIVE FOR TRD: Proven efficacy in treatment-resistant depression patients",
        "SUICIDAL IDEATION REDUCTION: Quick decrease in suicidal thoughts",
        "INFUSION THERAPY: Safe, controlled administration in clinical settings",
        "MENTAL HEALTH IMPROVEMENT: Significant mood enhancement in clinical trials"
    ]

    for benefit in benefits:
        elements.append(Paragraph(f"• {benefit}", body_style))

    elements.append(Spacer(1, 12))

    # Treatment methodology
    elements.append(Paragraph("KETAMINE INFUSION PROTOCOL", heading_style))

    protocol_text = """
    Standard ketamine therapy involves low-dose IV infusions over 40-60 minutes.
    Treatment-resistant depression patients undergo 6 sessions over 2-3 weeks.
    The sub-anesthetic ketamine dosage ensures safety while promoting neuroplasticity.
    Psychiatrists monitor patients throughout each ketamine session for safety.
    Dissociative effects during infusion are normal and temporary.
    """
    elements.append(Paragraph(protocol_text, body_style))
    elements.append(Spacer(1, 12))

    # Scientific mechanism
    elements.append(Paragraph("NEUROBIOLOGICAL MECHANISM", heading_style))

    mechanism_text = """
    Ketamine acts as an N-methyl-D-aspartate (NMDA) receptor antagonist, distinct from
    traditional monoaminergic antidepressants. This mechanism triggers rapid synaptic
    plasticity and new neural pathway formation. Glutamate system modulation leads to
    significant antidepressant effects. Clinical trials confirm ketamine's role in
    treatment-resistant depression management.
    """
    elements.append(Paragraph(mechanism_text, body_style))
    elements.append(Spacer(1, 12))

    # Conditions treated
    elements.append(Paragraph("CONDITIONS TREATED WITH KETAMINE", heading_style))

    conditions = [
        "Treatment-resistant depression (TRD)",
        "Major depressive disorder",
        "Post-traumatic stress disorder (PTSD)",
        "Anxiety disorders",
        "Suicidal ideation",
        "Chronic pain conditions",
        "Obsessive-compulsive disorder (OCD)"
    ]

    for condition in conditions:
        elements.append(Paragraph(f"• {condition}", body_style))

    elements.append(Spacer(1, 12))

    # Safety and side effects
    elements.append(Paragraph("SAFETY PROFILE AND MONITORING", heading_style))

    safety_text = """
    Ketamine therapy requires medical supervision during administration. Common side effects
    include transient dissociation, mild dizziness, and temporary blood pressure elevation.
    These effects resolve quickly post-infusion. Serious adverse events are rare when
    ketamine is administered by trained psychiatric professionals in controlled clinical
    environments. Pre-treatment evaluation ensures patient suitability for ketamine therapy.
    """
    elements.append(Paragraph(safety_text, body_style))
    elements.append(Spacer(1, 12))

    # Clinical outcomes
    elements.append(Paragraph("CLINICAL OUTCOMES AND EFFICACY", heading_style))

    outcomes_text = """
    Clinical studies demonstrate 70-80% response rates in treatment-resistant depression patients.
    Ketamine therapy shows rapid antidepressant effects within hours. Sustained improvement
    occurs in most patients following the complete infusion series. Long-term maintenance
    protocols help maintain therapeutic benefits. Patient-reported outcome measures confirm
    significant quality of life improvements post-ketamine treatment.
    """
    elements.append(Paragraph(outcomes_text, body_style))
    elements.append(Spacer(1, 12))

    # Footer
    footer_text = f"Document generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(footer_text, styles['Italic']))

    # Build the PDF
    doc.build(elements)
    print(f"Highly relevant ketamine PDF created successfully: {filename}")

if __name__ == "__main__":
    create_highly_relevant_ketamine_pdf("highly_relevant_ketamine_info.pdf")