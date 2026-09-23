import io
import datetime
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

def generate_itinerary_pdf(
    destination: str,
    trip_inputs: Dict[str, Any],
    itinerary_data: List[Dict[str, Any]],
    heritage_data: List[Dict[str, Any]],
    weather_data: Dict[str, Any],
    budget_data: Dict[str, Any]
) -> bytes:
    """
    Generates a professional downloadable PDF of the TripGenie itinerary.
    Returns bytes of the PDF file.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0f172a") # Dark slate
    accent_color = colors.HexColor("#0d9488")  # Teal accent
    bg_light = colors.HexColor("#f8fafc")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    bold_body_style = ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=primary_color
    )

    story = []

    # Title & Header Banner
    story.append(Paragraph("TRIPGENIE", title_style))
    story.append(Paragraph(f"Smart Gateway to Your Destination &bull; Travel Itinerary for <b>{destination.title()}</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceBefore=0, spaceAfter=12))

    # Summary Metadata Grid
    duration = trip_inputs.get('duration', 1)
    mood = trip_inputs.get('mood', 'Relaxed')
    style = trip_inputs.get('travel_style', 'Solo')
    budget_tier = trip_inputs.get('budget', 'Moderate')
    interests = ", ".join(trip_inputs.get('interests', []))

    gen_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    meta_table_data = [
        [
            Paragraph("<b>Destination:</b>", body_style), Paragraph(destination.title(), body_style),
            Paragraph("<b>Duration:</b>", body_style), Paragraph(f"{duration} Days", body_style)
        ],
        [
            Paragraph("<b>Mood:</b>", body_style), Paragraph(mood, body_style),
            Paragraph("<b>Travel Style:</b>", body_style), Paragraph(style, body_style)
        ],
        [
            Paragraph("<b>Budget Tier:</b>", body_style), Paragraph(budget_tier, body_style),
            Paragraph("<b>Generated:</b>", body_style), Paragraph(gen_date, body_style)
        ],
        [
            Paragraph("<b>Interests:</b>", body_style), Paragraph(interests, body_style),
            Paragraph("", body_style), Paragraph("", body_style)
        ]
    ]

    meta_table = Table(meta_table_data, colWidths=[80, 180, 80, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Budget Overview
    if budget_data:
        story.append(Paragraph("Trip Budget Estimate", section_heading))
        est_total = budget_data.get('total_estimated', 0)
        breakdown = budget_data.get('breakdown', {})
        
        budget_rows = [
            [Paragraph("<b>Category</b>", bold_body_style), Paragraph("<b>Estimated Cost</b>", bold_body_style)]
        ]
        for cat, amt in breakdown.items():
            budget_rows.append([Paragraph(cat, body_style), Paragraph(f"₹{amt:,.0f} / ${amt/83:,.0f}", body_style)])
        budget_rows.append([Paragraph("<b>Total Estimated</b>", bold_body_style), Paragraph(f"<b>₹{est_total:,.0f} / ${est_total/83:,.0f}</b>", bold_body_style)])

        b_table = Table(budget_rows, colWidths=[260, 260])
        b_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(b_table)
        story.append(Spacer(1, 15))

    # Day-wise Itinerary
    story.append(Paragraph("Day-by-Day Personalized Itinerary", section_heading))

    for day_info in itinerary_data:
        day_num = day_info.get('day', 1)
        theme = day_info.get('theme', f'Exploring {destination}')
        story.append(Paragraph(f"<b>Day {day_num}: {theme}</b>", bold_body_style))

        slots = day_info.get('slots', [])
        day_rows = [[
            Paragraph("<b>Time</b>", bold_body_style),
            Paragraph("<b>Place & Activity</b>", bold_body_style),
            Paragraph("<b>Est. Distance & Travel</b>", bold_body_style)
        ]]

        for slot in slots:
            period = slot.get('period', 'Morning').capitalize()
            place = slot.get('place', 'Local Spot')
            activity = slot.get('activity', '')
            duration_str = slot.get('duration', '1-2 hrs')
            reason = slot.get('reason', '')
            dist = slot.get('distance_km', 'N/A')
            ttime = slot.get('travel_time', 'N/A')

            content_text = f"<b>{place}</b> ({duration_str})<br/>{activity}"
            if reason:
                content_text += f"<br/><i>Note: {reason}</i>"

            dist_text = f"{dist} km<br/>{ttime}" if dist != 'N/A' else "Local attraction"

            day_rows.append([
                Paragraph(period, bold_body_style),
                Paragraph(content_text, body_style),
                Paragraph(dist_text, body_style)
            ])

        d_table = Table(day_rows, colWidths=[70, 330, 120])
        d_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8fafc")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(d_table)
        story.append(Spacer(1, 10))

    # Heritage & Cultural Highlights
    if heritage_data:
        story.append(Spacer(1, 10))
        story.append(Paragraph("Local Heritage & Cultural Highlights", section_heading))
        
        h_rows = [[
            Paragraph("<b>Heritage Site</b>", bold_body_style),
            Paragraph("<b>Category</b>", bold_body_style),
            Paragraph("<b>Description & Significance</b>", bold_body_style)
        ]]

        for h in heritage_data[:6]:  # Top 6 heritage sites
            h_rows.append([
                Paragraph(h.get('name', 'Heritage Site'), bold_body_style),
                Paragraph(h.get('category', 'Historical'), body_style),
                Paragraph(f"{h.get('description', '')}<br/><b>Relevance:</b> {h.get('cultural_relevance', 'Local heritage landmark')}", body_style)
            ])

        h_table = Table(h_rows, colWidths=[130, 100, 290])
        h_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(h_table)

    # Footer note
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=10, spaceAfter=8))
    footer_text = "Generated by TripGenie &bull; Community Service Tourism & Heritage Initiative &bull; Safe Travels!"
    story.append(Paragraph(f"<font color='#64748b' size=8>{footer_text}</font>", body_style))

    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data
