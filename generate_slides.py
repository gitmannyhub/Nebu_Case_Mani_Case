import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas tool to dynamically add slide counts on top of the layout."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.setFillColor(colors.HexColor("#9CA3AF"))
            self.setFont("Helvetica", 9)
            slide_num = f"Slide {self._pageNumber} of {num_pages}"
            self.drawRightString(756, 22, slide_num)
            super().showPage()
        super().save()

def draw_slide_background(canvas, doc):
    """Draws the dark dashboard background canvas before text layers load."""
    canvas.saveState()
    # Deep slate black background
    canvas.setFillColor(colors.HexColor("#0B0E14"))
    canvas.rect(0, 0, 792, 612, fill=True, stroke=False)
    
    # Bottom footer divider line
    canvas.setStrokeColor(colors.HexColor("#1F2937"))
    canvas.setLineWidth(1)
    canvas.line(36, 40, 756, 40)
    
    # Running footer brand identification text
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.setFont("Helvetica", 9)
    canvas.drawString(36, 22, "Nabu Casa | Supply Planning Framework | Final Release")
    canvas.restoreState()

def build_presentation():
    pdf_filename = "Nabu_Casa_Presentation_Slides.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=55
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Themes matching the Dashboard UX
    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.white,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#9CA3AF"),
        spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#D1D5DB"),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'SlideBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=5
    )
    
    metric_label = ParagraphStyle(
        'MetricLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#9CA3AF")
    )
    
    metric_val = ParagraphStyle(
        'MetricValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=32,
        textColor=colors.white
    )

    story = []
    
    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE & EXECUTIVE VIEW
    # -------------------------------------------------------------------------
    story.append(Paragraph("Supply Planning Decision Framework", title_style))
    story.append(Paragraph("Nabu Casa business case presentation | Prepared by Manikandan Sankaran", subtitle_style))
    
    # Row of 4 Premium KPI Cards matching the screenshot design
    card_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#161B26")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#242F41")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])
    
    c1 = Table([[Paragraph("Current WOS", metric_label)], [Spacer(1,6)], [Paragraph("4.8", metric_val)]], colWidths=[165])
    c1.setStyle(card_style)
    c1_wrapper = Table([[c1]], colWidths=[165])
    c1_wrapper.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor("#38BDF8"))])) # Light Blue Bar
    
    c2 = Table([[Paragraph("Backlog Risk", metric_label)], [Spacer(1,6)], [Paragraph("Critical", metric_val)]], colWidths=[165])
    c2.setStyle(card_style)
    c2_wrapper = Table([[c2]], colWidths=[165])
    c2_wrapper.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor("#F87171"))])) # Pink/Red Bar
    
    c3 = Table([[Paragraph("New Buy", metric_label)], [Spacer(1,6)], [Paragraph("15,000", metric_val)]], colWidths=[165])
    c3.setStyle(card_style)
    c3_wrapper = Table([[c3]], colWidths=[165])
    c3_wrapper.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor("#34D399"))])) # Mint Bar
    
    c4 = Table([[Paragraph("MOQ Block", metric_label)], [Spacer(1,6)], [Paragraph("5,000", metric_val)]], colWidths=[165])
    c4.setStyle(card_style)
    c4_wrapper = Table([[c4]], colWidths=[165])
    c4_wrapper.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,0), 3, colors.HexColor("#FBBF24"))])) # Amber Bar
    
    kpi_table = Table([[c1_wrapper, c2_wrapper, c3_wrapper, c4_wrapper]], colWidths=[180, 180, 180, 180])
    story.append(kpi_table)
    story.append(Spacer(1, 20))
    
    # Executive View Panel Text
    exec_text = (
        "<b>Executive Summary Statement:</b> This framework establishes a highly automated, "
        "mathematically locked planning sequence for Nabu Casa. It transitions out of "
        "unstructured spreadsheets into a robust model designed to protect regional launch revenue, "
        "isolate unallocated inventory assets, and enforce strict factory production parameters."
    )
    exec_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[720])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#111827")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1F2937")),
    ]))
    story.append(exec_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 2: CORE PLANNING ASSUMPTIONS (11 MOVEMENT LOOPS)
    # -------------------------------------------------------------------------
    story.append(Paragraph("Core Operational Architecture & Assumptions", title_style))
    story.append(Paragraph("The 11 verified structural parameters driving network logic", subtitle_style))
    
    col1_content = [
        Paragraph("<b>1. Lifecycle Stage:</b> New phase launch status for part number FLAGSHIP123.", bullet_style),
        Paragraph("<b>2. Supplier Identification:</b> Core contract manufacturing node is locked as CMHK.", bullet_style),
        Paragraph("<b>3. Gateway Code:</b> Central hub sort facility is designated as HK111 in Hong Kong.", bullet_style),
        Paragraph("<b>4. Disruption Timing:</b> Shortage alert arrived exactly 2 days before standard departure window.", bullet_style),
        Paragraph("<b>5. True Lead Time:</b> 8-week production lifecycle plus a 2-week ocean shipping buffer block.", bullet_style),
        Paragraph("<b>6. Demand Baseline:</b> Calculations evaluate hard customer backlogs, not speculative projections.", bullet_style)
    ]
    
    col2_content = [
        Paragraph("<b>7. On-Hand Isolation Rule:</b> 8,000 units on hand are fully pre-allocated and cannot fill new gaps.", bullet_style),
        Paragraph("<b>8. Split Delivery Timelines:</b> 4,000 units land immediately; 6,000 units face a 3-week factory delay.", bullet_style),
        Paragraph("<b>9. Factory Batch MOQ:</b> Fixed 5,000-unit production runs requiring math ceiling ceiling rounding.", bullet_style),
        Paragraph("<b>10. 3PL Node Framework:</b> Central sorting gate splits stock out straight to US, EU, and APAC hubs.", bullet_style),
        Paragraph("<b>11. Confirmed Open Demand:</b> Total current network backlog layer is locked at exactly 9,500 units.", bullet_style)
    ]
    
    assumptions_table = Table([[col1_content, col2_content]], colWidths=[355, 355])
    assumptions_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(assumptions_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 3: PART A: SUPPLY DISRUPTION MANAGEMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part A: Supply Disruption Management", title_style))
    story.append(Paragraph("Immediate response sequences and factory capacity optimization loops", subtitle_style))
    
    part_a_left = [
        Paragraph("<b>The First 48 Hours: Stabilization Sequence</b>", body_style),
        Paragraph("* <b>Isolate the Constraint:</b> Align directly with CMHK to lock down the split-shipment numbers (4,000 immediate vs 6,000 delayed by 3 weeks) to plan against facts.", bullet_style),
        Paragraph("* <b>Execute Net Asset Accounting:</b> Calculate Net Assets = On Hand + Open PO - Backlog. Apply the On-Hand Isolation Rule to define true current network exposure.", bullet_style),
        Paragraph("* <b>Protect Commercial Launch Vectors:</b> Isolate high-risk windows, routing the immediate 4,000 physical pool directly to the upcoming US promo launch.", bullet_style)
    ]
    
    part_a_right = [
        Paragraph("<b>Supplier Cross-Portfolio Mitigation Strategy</b>", body_style),
        Paragraph("* <b>Portfolio Capacity Swapping (Push Logic):</b> Evaluate the broader factory floor. Request CMHK to push out low-priority sustaining lines (e.g. SUSTAINING456 under PO10003) by 4 weeks to immediately free up factory capacity slots for our flagship run.", bullet_style),
        Paragraph("* <b>Logistics Expediting (Pull Logic):</b> Switch the delayed 6,000 balance to a priority air corridor out of HK111 to eliminate standard ocean legs and recover the 3-week gap.", bullet_style)
    ]
    
    part_a_table = Table([[part_a_left, part_a_right]], colWidths=[355, 355])
    part_a_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (1,0), (1,0), 10)]))
    story.append(part_a_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 4: PART B: INVENTORY ALLOCATION STRATEGY
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part B: Inventory Allocation Strategy", title_style))
    story.append(Paragraph("Commercial priority cascade and strategic hub allocation modeling", subtitle_style))
    
    alloc_headers = ["Regional 3PL Hub", "Open Backlog", "Allocated Pool", "Net Deficit", "Fill Rate"]
    alloc_rows = [
        [Paragraph(f"<b>{h}</b>", body_style) for h in alloc_headers],
        ["US Hub (Promo Launch)", "4,500 Units", "4,000 Units", "500 Units", "88.8%"],
        ["EU Hub (Stable Demand)", "3,000 Units", "0 Units", "3,000 Units", "0.0%"],
        ["APAC Hub (Strategic Growth)", "2,000 Units", "0 Units", "2,000 Units", "0.0%"],
        ["Total Network Portfolio", "9,500 Units", "4,000 Units", "5,500 Units", "42.1%"]
    ]
    
    alloc_table = Table(alloc_rows, colWidths=[180, 135, 135, 135, 135])
    alloc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#161B26")),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#242F41")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor("#D1D5DB")),
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor("#111827")),
    ]))
    story.append(alloc_table)
    story.append(Spacer(1, 15))
    
    tradeoff_text = (
        "<b>Strategic Trade-off Justification:</b> 100% of the arriving pool is routed to the United States "
        "to protect a high-exposure promotional launch next week, accepting a minor 500-unit short. "
        "EU and APAC nodes are intentionally deferred, programmatically receiving 0 units from this immediate intake. "
        "This localized deficit is managed proactively by providing partners a firm, data-verified logistics "
        "roadmap locking their backlogs into the incoming expedited air freight balance clearing on July 24, 2026."
    )
    story.append(Paragraph(tradeoff_text, body_style))
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 5: PART C: INVENTORY PLANNING & REPLENISHMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part C: Replenishment & Planning Deficit", title_style))
    story.append(Paragraph("Mathematical modeling of network inventory positions and production MOQ reorder rules", subtitle_style))
    
    repl_left = [
        Paragraph("<b>Operational Calculation Inputs</b>", body_style),
        Paragraph("* <b>Weekly Demand Run-Rate:</b> 1,673 units/week (Average monthly forecast of 7,250 units / 4.33 weeks).", bullet_style),
        Paragraph("* <b>Target Safety Cover Buffer:</b> Strict 12-week network safety target requires <b>20,076 units</b> in position.", bullet_style),
        Paragraph("* <b>True Inventory Position Formula:</b> On Hand (8,000) + Open PO (10,000) - Backlog (9,500) = <b>8,500 net units</b>.", bullet_style),
        Spacer(1, 5),
        Paragraph("<b>MOQ Step-Batch Ceiling Rounding Function</b>", body_style),
        Paragraph("Net Deficit = 20,076 (Target) - 8,500 (Position) = <b>11,576 units raw deficit</b>.<br/>"
                  "Dividing 11,576 by the strict 5,000-unit factory MOQ block yields 2.315 batches. "
                  "Applying a mathematical ceiling function rounds the procurement proposal up to 3 full production batches, "
                  "generating an optimized <b>15,000-unit New Buy order</b> placed on July 4, 2026. This hits the floor in "
                  "Month 3 to completely insulate the peak 9,000-unit demand spike.", bullet_style)
    ]
    
    repl_right = [
        Paragraph("<b>Justification to Finance (Working Capital Strategy)</b>", body_style),
        Paragraph("An order of only 10,000 units would fail to clear the deficit, leaving a critical 1,576-unit exposure gap "
                  "below safety targets. The 15,000-unit order protects high-margin revenue and market share during the "
                  "critical New product lifecycle phase where stockout costs far outweigh localized holding expenses.", bullet_style),
        Spacer(1, 5),
        Paragraph("<b>ERP Systems & NetSuite Architecture Requirements</b>", body_style),
        Paragraph("Introduce automated dashboard tracking configurations to eliminate manual tracking overhead:<br/>"
                  "1. <b>Days of Inventory Coverage:</b> Live metric mapping physical stocks against rolling forward forecasts.<br/>"
                  "2. <b>PO Lifecycle Pipeline:</b> Track production milestones at CMHK alongside transit gates via HK111.<br/>"
                  "3. <b>Exception Alert Engine:</b> Automated flags for lead-time drift greater than 5% or forecast accuracy slips.", bullet_style)
    ]
    
    part_c_table = Table([[repl_left, repl_right]], colWidths=[355, 355])
    part_c_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (1,0), (1,0), 10)]))
    story.append(part_c_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 6: PART D: OPERATING MODEL & GOVERNANCE
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part D: Operating Model & Governance Architecture", title_style))
    story.append(Paragraph("Documented Standard Operating Procedures, cross-functional ownership, and risk reduction", subtitle_style))
    
    sop_text = (
        "<b>Standard Operating Procedure (SOP) Sequence:</b><br/>"
        "<b>Step 1: Alert Trigger</b> (Automated ERP tracking flags a production constraint at CMHK) -> "
        "<b>Step 2: Split Validation</b> (Procurement confirms exact split quantities and arrival windows within 24 hours) -> "
        "<b>Step 3: Asset Processing</b> (Planning applies net asset formulas to compute deficits against safety cover) -> "
        "<b>Step 4: Priority Cascade</b> (Allocation engine triggers priority commercial cascade protecting launch lines) -> "
        "<b>Step 5: Governance Loop</b> (Procurement executes step-batch reorders through appropriate authorization gates)."
    )
    story.append(Table([[Paragraph(sop_text, body_style)]], colWidths=[720], style=[
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#161B26")), ('PADDING', (0,0), (-1,-1), 10), ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#242F41"))
    ]))
    story.append(Spacer(1, 10))
    
    gov_left = [
        Paragraph("<b>Weeks of Supply (WOS) Escalation Triggers</b>", body_style),
        Paragraph("<b>Green: Normal (WOS >= 12):</b> Routine automated monitoring handled completely by the <b>Supply Planner</b>.", bullet_style),
        Paragraph("<b>Yellow: Planner Review (WOS < 8):</b> Flagged constraint window; local 3PL rebalancing activated by the <b>Supply Planner</b>.", bullet_style),
        Paragraph("<b>Orange: Management Sync (WOS < 6):</b> Daily tracking cycles and cross-functional synchronization led by the <b>Supply Planning Manager</b>.", bullet_style),
        Paragraph("<b>Red: Executive Isolation (WOS < 4):</b> Emergency meeting with CMHK leadership driven directly by the <b>Operations Director</b>.", bullet_style)
    ]
    
    gov_right = [
        Paragraph("<b>Long-Term Global Risk Mitigation</b>", body_style),
        Paragraph("* <b>Supplier Diversification:</b> Establish a formal dual-sourcing strategy by qualifying a secondary manufacturing node outside Hong Kong to remove single-source exposure.", bullet_style),
        Paragraph("* <b>Safety Stock Calibration:</b> Transition to differentiated inventory models: holding higher component buffers for New lines while keeping mature items lean.", bullet_style),
        Paragraph("* <b>Inventory Positioning:</b> Move away from pure central storage; position inventory nodes closer to regional 3PL hubs (US/EU) to compress transit legs and absorb unexpected demand spikes.", bullet_style)
    ]
    
    gov_table = Table([[gov_left, gov_right]], colWidths=[355, 355])
    gov_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (1,0), (1,0), 10)]))
    story.append(gov_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 7: PART E: QUALITY & RETURNS MANAGEMENT
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part E: Quality & Returns Management", title_style))
    story.append(Paragraph("Real-time exception workflows, automated quarantines, and rapid customer response pipelines", subtitle_style))
    
    part_e_left = [
        Paragraph("<b>Real-Time Outlier Detection & Quarantining</b>", body_style),
        Paragraph("* <b>Z-Score Monitoring Dashboard:</b> Configured to process regional return log data fields continuously. The absolute millisecond returns cross a strict <b>1.5% defect threshold</b>, an emergency system hold triggers.", bullet_style),
        Paragraph("* <b>Instant Gateway Isolation:</b> Systemic hold codes execute immediately across the ERP architecture, freezing and quarantining remaining lots at the central <b>HK111</b> gateway and regional 3PL networks before defective items reach downstream customers.", bullet_style),
        Spacer(1, 5),
        Paragraph("<b>Accelerated RMA Pipeline & Scrap-in-Place Protocol</b>", body_style),
        Paragraph("Distributors log failing serial strings via a dedicated online portal. To bypass expensive cross-border reverse logistics freight and customs friction, regional 3PLs execute an immediate local scrap-in-place protocol within a <b>15-minute resolution SLA</b>, auto-generating instant credit memos or replacement allocations.", bullet_style)
    ]
    
    part_e_right = [
        Paragraph("<b>Root Cause Investigation & Supplier Integration</b>", body_style),
        Paragraph("Dispatch technical engineering resource partners directly to the CMHK manufacturing floor to audit assembly lines and component sub-tiers. Proactively distribute clear automated status notifications and engineering recovery timelines directly to global distribution networks to preserve retail shelf confidence.", bullet_style),
        Spacer(1, 5),
        Paragraph("<b>Corrective and Preventive Actions (CAPA)</b>", body_style),
        Paragraph("Mandate automated optical inspection loops on the factory floor, enforce strict component screening gates at intake, and implement isolated pilot-run verification cycles on all subsequent production lots.", bullet_style)
    ]
    
    part_e_table = Table([[part_e_left, part_e_right]], colWidths=[355, 355])
    part_e_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (1,0), (1,0), 10)]))
    story.append(part_e_table)
    story.append(PageBreak())
    
    # -------------------------------------------------------------------------
    # SLIDE 8: PART F: STATEMENT OF AI COLLABORATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("Part F: Statement of AI Collaboration & Professional Judgment", title_style))
    story.append(Paragraph("Human-in-the-loop framework balancing automated productivity with professional experience", subtitle_style))
    
    f_text = (
        "Throughout this exercise, I used AI as a collaborative tool to accelerate development and improve the quality of my submission. "
        "I used it to research supply chain concepts, challenge my assumptions, refine my written responses, improve the structure and wording of the PDF presentation, "
        "and assist with the design and development of the interactive Streamlit application. AI also helped me prototype parts of the user interface, "
        "review the planning workflow, and improve the overall presentation of the solution.<br/><br/>"
        "I accepted AI suggestions that improved the clarity, structure and usability of the application and supporting documentation. "
        "I also rejected or modified recommendations that did not align with the business case, practical supply planning principles or my own professional judgement. "
        "Every recommendation included in the final submission was reviewed, validated and adapted before being incorporated.<br/><br/>"
        "I relied entirely on my own judgement and professional experience to define the planning assumptions, develop the planning methodology, "
        "determine the inventory allocation strategy, justify the replenishment recommendation, design the planning hierarchy, and create the Standard Operating Procedure (SOP), "
        "governance model and KPI framework. These decisions were based on my experience in Supply Chain and Service Operations: "
        "incorporating the exact structural concepts I previously implemented at Apple when deploying their new operational processes: "
        "ensuring that the final solution reflected practical operational decision-making rather than generic AI-generated output.<br/><br/>"
        "In a role like this, I would use AI as a decision-support tool rather than a decision-maker. I believe AI can significantly improve productivity "
        "by analysing operational data, identifying supply risks, generating planning scenarios, automated routine reporting and improving documentation. "
        "However, final planning decisions should always remain the responsibility of the planner, combining AI-generated insights with business context, "
        "commercial priorities, organisational objectives and professional judgement."
    )
    story.append(Paragraph(f_text, body_style))
    
    # Build with background template callbacks executing BEFORE content lays down
    doc.build(story, onFirstPage=draw_slide_background, onLaterPages=draw_slide_background, canvasmaker=NumberedCanvas)
    print("Success: 'Nabu_Casa_Presentation_Slides.pdf' generated successfully.")

if __name__ == "__main__":
    build_presentation()