from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from planning_engine import SupplyPlanningEngine
from sample_data import products


OUTPUT_PATH = Path("output/pdf/supply_planning_decision_report.pdf")


def moneyless(value):
    return f"{value:,}"


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            textColor=colors.HexColor("#172033"),
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubtitleCenter",
            parent=styles["BodyText"],
            alignment=TA_CENTER,
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#526071"),
            spaceAfter=28,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#172033"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#27364A"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#526071"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#27364A"),
            spaceAfter=6,
        )
    )
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8DEE8"))
    canvas.line(inch * 0.55, letter[1] - inch * 0.42, letter[0] - inch * 0.55, letter[1] - inch * 0.42)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#687589"))
    canvas.drawString(inch * 0.55, letter[1] - inch * 0.31, "Supply Planning Decision Report")
    canvas.drawRightString(letter[0] - inch * 0.55, inch * 0.35, f"Page {doc.page}")
    canvas.restoreState()


def p(text, styles, style="Body"):
    return Paragraph(text, styles[style])


def section(title, styles):
    return [Spacer(1, 6), p(title, styles, "SectionTitle")]


def table(data, column_widths=None, header=True, body_font_size=8.4):
    wrapped = []
    styles = make_styles()
    header_style = ParagraphStyle(
        name="TableHeader",
        parent=styles["Small"],
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
    for index, row in enumerate(data):
        cell_style = header_style if header and index == 0 else styles["Small"]
        wrapped.append([Paragraph(str(cell), cell_style) for cell in row])

    tbl = Table(wrapped, colWidths=column_widths, hAlign="LEFT", repeatRows=1 if header else 0)
    commands = [
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8DEE8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D8DEE8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("FONTSIZE", (0, 0), (-1, -1), body_font_size),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#27364A")),
            ]
        )
    tbl.setStyle(TableStyle(commands))
    return tbl


def kpi_table(items):
    rows = []
    row = []
    for label, value, note in items:
        row.append(f"<b>{label}</b><br/><font size='14'>{value}</font><br/><font color='#687589'>{note}</font>")
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        row.extend([""] * (4 - len(row)))
        rows.append(row)

    styles = make_styles()
    wrapped = [[Paragraph(cell, styles["Small"]) for cell in table_row] for table_row in rows]
    tbl = Table(wrapped, colWidths=[1.75 * inch] * 4, hAlign="LEFT")
    tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FA")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8DEE8")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return tbl


def paragraph_list(items, styles):
    return [p(f"- {item}", styles, "Body") for item in items]


def build_pdf():
    product = products[0]
    engine = SupplyPlanningEngine(product)
    inv = engine.inventory_health()
    shortage = engine.po_shortage()
    backlog = engine.backlog_risk()
    supplier = engine.supplier_health()
    allocation = engine.allocation_engine()
    balance = engine.stock_balance()
    pull = engine.pull_logic()
    push = engine.push_logic()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    story = []

    story.append(p("Supply Planning Decision Report", styles, "TitleCenter"))
    story.append(
        p(
            "Prepared by Manikandan Sankaran<br/>Business Case Demonstration | Nabu Casa | Supply Planning Decision Framework<br/>"
            f"Generated {date.today().isoformat()}",
            styles,
            "SubtitleCenter",
        )
    )

    story.extend(section("Executive Summary", styles))
    story.append(
        kpi_table(
            [
                ("Current WOS", inv["Current WOS"], "On-hand weeks of supply"),
                ("Planning Deficit", moneyless(inv["Planning Deficit"]), "Units below target"),
                ("Recommended New Buy", moneyless(shortage["Recommended PO"]), "MOQ adjusted"),
                ("Backlog Risk", backlog["Risk"], backlog["Recommendation"]),
            ]
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        p(
            f"The flagship product is currently classified as <b>{inv['Status']}</b>. "
            f"Inventory position is {moneyless(inv['Inventory Position'])} units against a target of "
            f"{moneyless(inv['Target Inventory'])} units. The planning engine recommends a new buy of "
            f"{moneyless(shortage['Recommended PO'])} units where the remaining deficit cannot be recovered through balancing, pull, or push actions.",
            styles,
        )
    )

    story.extend(section("Product And Supplier Position", styles))
    story.append(
        table(
            [
                ["Part Number", "Description", "Supplier", "Supplier Status", "Lead Time", "Shipping"],
                [
                    product["part_number"],
                    product["description"],
                    supplier["Supplier"],
                    supplier["Status"],
                    f"{supplier['Lead Time']} weeks",
                    f"{supplier['Shipping']} weeks",
                ],
            ],
            [1.15 * inch, 1.45 * inch, 0.9 * inch, 1.2 * inch, 1.05 * inch, 1.05 * inch],
        )
    )

    story.extend(section("Inventory Health", styles))
    story.append(
        kpi_table(
            [
                ("Target WOS", inv["Target WOS"], "Planning policy"),
                ("Current WOS", inv["Current WOS"], "On hand only"),
                ("Pipeline WOS", inv["Pipeline WOS"], "On hand plus open PO"),
                ("Disruption WOS", inv["Disruption WOS"], "On hand plus in transit"),
                ("Target Inventory", moneyless(inv["Target Inventory"]), "Units"),
                ("Inventory Position", moneyless(inv["Inventory Position"]), "Units"),
                ("Open PO", moneyless(engine.total_open_po()), "Committed pipeline"),
                ("In Transit", moneyless(engine.total_in_transit()), "Already shipped"),
            ]
        )
    )

    story.extend(section("Purchase Order Health", styles))
    story.append(
        table(
            [["PO", "Quantity", "Status", "Ship Date", "Delivery Date"]]
            + [
                [row["PO"], moneyless(row["Quantity"]), row["Status"], row["Ship Date"], row["Delivery Date"]]
                for row in engine.purchase_order_health()
            ],
            [1.3 * inch, 1.1 * inch, 1.25 * inch, 1.45 * inch, 1.45 * inch],
        )
    )

    allocation_rows = [["Region", "On Hand", "Weekly Demand", "Open Demand", "Allocated", "Backlog", "Fill Rate"]]
    for region, data in product["regions"].items():
        allocated = allocation["Regions"][region]
        allocation_rows.append(
            [
                region,
                moneyless(data["on_hand"]),
                moneyless(data["weekly_demand"]),
                moneyless(data["open_demand"]),
                moneyless(allocated["Allocated"]),
                moneyless(allocated["Backlog"]),
                f"{allocated['Fill Rate']}%",
            ]
        )
    story.append(
        KeepTogether(
            section("Regional Demand And Allocation", styles)
            + [
                table(
                    allocation_rows,
                    [0.85 * inch, 0.9 * inch, 1.0 * inch, 1.0 * inch, 0.95 * inch, 0.9 * inch, 0.9 * inch],
                )
            ]
        )
    )

    story.extend(section("Optimization Sequence", styles))
    story.append(
        table(
            [
                ["Step", "Planning Rule", "Status", "Recommendation"],
                ["1", "Stock Balance", balance["Status"], balance["Recommendation"]],
                ["2", pull["Priority"], pull["Status"], pull["Recommendation"]],
                ["3", push["Priority"], push["Status"], push["Recommendation"]],
                ["4", "PO Shortage", "REQUIRED" if shortage["Required"] else "NOT REQUIRED", shortage["Reason"]],
                ["5", "Backlog Risk", backlog["Risk"], backlog["Recommendation"]],
            ],
            [0.45 * inch, 1.55 * inch, 1.2 * inch, 3.3 * inch],
        )
    )

    if balance["Transfers"]:
        story.append(Spacer(1, 8))
        story.append(p("Recommended Transfers", styles, "CardTitle"))
        story.append(
            table(
                [["Receiving Region", "Donor Region", "Transfer Qty", "Receiving WOS", "Donor WOS"]]
                + [
                    [
                        row["Receiving Region"],
                        row["Donor Region"],
                        moneyless(row["Transfer Qty"]),
                        row["Receiving WOS"],
                        row["Donor WOS"],
                    ]
                    for row in balance["Transfers"]
                ],
                [1.45 * inch, 1.25 * inch, 1.15 * inch, 1.15 * inch, 1.15 * inch],
            )
        )

    story.append(PageBreak())
    story.extend(section("Planning Assumptions And Scope", styles))
    assumptions = [
        (
            "Purchase Order Timeline",
            "The 10,000-unit purchase order is assumed to have been created approximately 10 weeks before expected delivery: 8 weeks manufacturing lead time plus 2 weeks shipping and logistics.",
        ),
        (
            "Lead Time Definition",
            "The stated 8-week lead time is treated as manufacturing lead time. Inventory planning uses total replenishment lead time because decisions depend on when stock becomes available for sale.",
        ),
        (
            "Regional Open Demand",
            "Regional demand is treated as confirmed distributor and customer purchase orders awaiting fulfilment, not forecast demand.",
        ),
        (
            "Inventory Position",
            "Open purchase orders already include in-transit inventory. Inventory position is calculated as on hand plus open purchase orders to avoid double-counting.",
        ),
        (
            "Distribution Network",
            "A single central distribution centre is assumed where inventory is received before allocation to regional distributors.",
        ),
        (
            "Finished Goods Scope",
            "The product is treated as a finished good supplied by a contract manufacturer. Service parts, repair inventory, reverse logistics, and RMAs are excluded.",
        ),
        (
            "Reusable Framework",
            "The prototype is designed as a reusable supply planning decision framework supporting multiple products, suppliers, regions, and rule-based planning decisions.",
        ),
    ]
    for title, body in assumptions:
        story.append(KeepTogether([p(title, styles, "CardTitle"), p(body, styles, "Body"), Spacer(1, 4)]))

    story.extend(section("Immediate Response Checklist", styles))
    story.extend(
        paragraph_list(
            [
                "Validate supplier root cause",
                "Confirm revised production schedule",
                "Review inventory health and weeks of supply",
                "Review customer backlog and open purchase orders",
                "Evaluate stock balance, pull, and push opportunities",
                "Calculate planning deficit and determine new buy requirement",
                "Communicate recovery plan",
            ],
            styles,
        )
    )

    story.extend(section("Planning Formula Reference", styles))
    story.append(
        table(
            [
                ["Formula", "Definition"],
                ["Target Inventory", "Target WOS x Weekly Demand"],
                ["Inventory Position", "On Hand + Open Purchase Orders"],
                ["Planning Deficit", "Target Inventory - Inventory Position"],
                ["Recommended New Buy", "MAX(Planning Deficit, MOQ)"],
            ],
            [2.0 * inch, 4.5 * inch],
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.55 * inch,
        title="Supply Planning Decision Report",
        author="Manikandan Sankaran",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return OUTPUT_PATH


if __name__ == "__main__":
    print(build_pdf())
