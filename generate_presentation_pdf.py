from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from planning_engine import SupplyPlanningEngine
from sample_data import products


OUT = Path("output/pdf/nabu_casa_supply_planning_presentation.pdf")
PAGE_W, PAGE_H = landscape((13.333 * inch, 7.5 * inch))

BG = colors.HexColor("#0B1020")
PANEL = colors.HexColor("#111A2E")
PANEL_2 = colors.HexColor("#162238")
TEXT = colors.HexColor("#F7FAFF")
MUTED = colors.HexColor("#AAB7CF")
BLUE = colors.HexColor("#38BDF8")
TEAL = colors.HexColor("#2DD4BF")
AMBER = colors.HexColor("#FBBF24")
RED = colors.HexColor("#FB7185")
GREEN = colors.HexColor("#34D399")
PURPLE = colors.HexColor("#A78BFA")
LINE = colors.HexColor("#253552")


def fmt(value):
    return f"{value:,}"


def text_width(text, font="Helvetica", size=12):
    return stringWidth(str(text), font, size)


class Deck:
    def __init__(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
        self.c.setTitle("Nabu Casa Supply Planning Decision Framework")
        self.c.setAuthor("Manikandan Sankaran")
        self.slide_no = 0

    def new_slide(self, kicker, title, subtitle=None):
        if self.slide_no:
            self.c.showPage()
        self.slide_no += 1
        self.c.setFillColor(BG)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(1)
        self.c.line(0.55 * inch, PAGE_H - 0.55 * inch, PAGE_W - 0.55 * inch, PAGE_H - 0.55 * inch)
        self.c.setFillColor(BLUE)
        self.c.setFont("Helvetica-Bold", 10)
        self.c.drawString(0.65 * inch, PAGE_H - 0.39 * inch, kicker.upper())
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica", 8)
        self.c.drawRightString(PAGE_W - 0.65 * inch, 0.35 * inch, f"{self.slide_no:02d}")
        self.c.setFillColor(TEXT)
        self.c.setFont("Helvetica-Bold", 30)
        self.c.drawString(0.75 * inch, PAGE_H - 1.12 * inch, title)
        if subtitle:
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica", 12)
            self.draw_wrapped(subtitle, 0.78 * inch, PAGE_H - 1.42 * inch, 11.4 * inch, 15, MUTED, "Helvetica", 12)

    def title_slide(self):
        self.slide_no += 1
        self.c.setFillColor(BG)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        self.c.setFillColor(BLUE)
        self.c.rect(0, PAGE_H - 0.16 * inch, PAGE_W * 0.42, 0.16 * inch, fill=1, stroke=0)
        self.c.setFillColor(TEAL)
        self.c.rect(PAGE_W * 0.42, PAGE_H - 0.16 * inch, PAGE_W * 0.24, 0.16 * inch, fill=1, stroke=0)
        self.c.setFillColor(AMBER)
        self.c.rect(PAGE_W * 0.66, PAGE_H - 0.16 * inch, PAGE_W * 0.18, 0.16 * inch, fill=1, stroke=0)
        self.c.setFillColor(RED)
        self.c.rect(PAGE_W * 0.84, PAGE_H - 0.16 * inch, PAGE_W * 0.16, 0.16 * inch, fill=1, stroke=0)
        self.c.setFillColor(TEXT)
        self.c.setFont("Helvetica-Bold", 40)
        self.c.drawString(0.85 * inch, 4.75 * inch, "Supply Planning")
        self.c.drawString(0.85 * inch, 4.24 * inch, "Decision Framework")
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica", 15)
        self.c.drawString(0.9 * inch, 3.62 * inch, "Nabu Casa business case presentation")
        self.c.drawString(0.9 * inch, 3.32 * inch, "Prepared by Manikandan Sankaran")
        self.kpi_card(8.1 * inch, 4.25 * inch, 1.55 * inch, 0.9 * inch, "Current WOS", "4.8", BLUE)
        self.kpi_card(9.9 * inch, 4.25 * inch, 1.55 * inch, 0.9 * inch, "Backlog Risk", "Critical", RED)
        self.kpi_card(8.1 * inch, 3.05 * inch, 1.55 * inch, 0.9 * inch, "New Buy", "5,000", TEAL)
        self.kpi_card(9.9 * inch, 3.05 * inch, 1.55 * inch, 0.9 * inch, "MOQ", "5,000", AMBER)
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica", 10)
        self.c.drawString(0.9 * inch, 0.55 * inch, "A concise, discussion-led presentation based on my Streamlit decision-support prototype.")

    def draw_wrapped(self, text, x, y, width, leading=14, color=TEXT, font="Helvetica", size=11):
        self.c.setFillColor(color)
        self.c.setFont(font, size)
        words = str(text).split()
        line = ""
        for word in words:
            test = f"{line} {word}".strip()
            if text_width(test, font, size) <= width:
                line = test
            else:
                self.c.drawString(x, y, line)
                y -= leading
                line = word
        if line:
            self.c.drawString(x, y, line)
            y -= leading
        return y

    def bullet_list(self, items, x, y, width, color=TEXT, bullet_color=BLUE, size=12, leading=20):
        for item in items:
            self.c.setFillColor(bullet_color)
            self.c.circle(x, y + 3, 2.5, fill=1, stroke=0)
            y = self.draw_wrapped(item, x + 0.16 * inch, y, width - 0.2 * inch, leading, color, "Helvetica", size)
            y -= 5
        return y

    def panel(self, x, y, w, h, fill=PANEL, stroke=LINE):
        self.c.setFillColor(fill)
        self.c.roundRect(x, y, w, h, 8, fill=1, stroke=0)
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(0.7)
        self.c.roundRect(x, y, w, h, 8, fill=0, stroke=1)

    def kpi_card(self, x, y, w, h, label, value, accent):
        self.panel(x, y, w, h, PANEL)
        self.c.setFillColor(accent)
        self.c.rect(x, y + h - 0.07 * inch, w, 0.07 * inch, fill=1, stroke=0)
        self.c.setFillColor(MUTED)
        self.c.setFont("Helvetica", 8.8)
        self.c.drawString(x + 0.13 * inch, y + h - 0.28 * inch, label)
        self.c.setFillColor(TEXT)
        self.c.setFont("Helvetica-Bold", 21)
        self.c.drawString(x + 0.13 * inch, y + 0.19 * inch, value)

    def table(self, rows, x, y, col_widths, row_h=0.34 * inch, header_color=BLUE):
        total_w = sum(col_widths)
        for r, row in enumerate(rows):
            yy = y - r * row_h
            fill = PANEL_2 if r == 0 else PANEL
            self.c.setFillColor(fill)
            self.c.rect(x, yy - row_h, total_w, row_h, fill=1, stroke=0)
            self.c.setStrokeColor(LINE)
            self.c.rect(x, yy - row_h, total_w, row_h, fill=0, stroke=1)
            cx = x
            for i, cell in enumerate(row):
                self.c.setStrokeColor(LINE)
                self.c.line(cx, yy - row_h, cx, yy)
                self.c.setFillColor(TEXT if r == 0 else MUTED)
                self.c.setFont("Helvetica-Bold" if r == 0 else "Helvetica", 9)
                self.c.drawString(cx + 0.09 * inch, yy - 0.22 * inch, str(cell))
                cx += col_widths[i]
            self.c.line(x + total_w, yy - row_h, x + total_w, yy)
        self.c.setFillColor(header_color)
        self.c.rect(x, y - 0.04 * inch, total_w, 0.04 * inch, fill=1, stroke=0)

    def flow(self, labels, x, y, w, colors_):
        gap = 0.11 * inch
        box_w = (w - gap * (len(labels) - 1)) / len(labels)
        for i, label in enumerate(labels):
            xx = x + i * (box_w + gap)
            self.panel(xx, y, box_w, 0.72 * inch, PANEL)
            self.c.setFillColor(colors_[i % len(colors_)])
            self.c.rect(xx, y + 0.65 * inch, box_w, 0.07 * inch, fill=1, stroke=0)
            self.c.setFillColor(TEXT)
            self.c.setFont("Helvetica-Bold", 8.4)
            self.draw_wrapped(label, xx + 0.08 * inch, y + 0.42 * inch, box_w - 0.16 * inch, 10, TEXT, "Helvetica-Bold", 8.4)

    def bar_chart(self, data, x, y, w, h, max_value, palette):
        bar_gap = 0.22 * inch
        bar_w = (w - bar_gap * (len(data) - 1)) / len(data)
        for i, (label, value) in enumerate(data):
            xx = x + i * (bar_w + bar_gap)
            bh = h * value / max_value
            self.c.setFillColor(colors.HexColor("#1E2B45"))
            self.c.rect(xx, y, bar_w, h, fill=1, stroke=0)
            self.c.setFillColor(palette[i % len(palette)])
            self.c.rect(xx, y, bar_w, bh, fill=1, stroke=0)
            self.c.setFillColor(TEXT)
            self.c.setFont("Helvetica-Bold", 11)
            self.c.drawCentredString(xx + bar_w / 2, y + bh + 0.12 * inch, fmt(value))
            self.c.setFillColor(MUTED)
            self.c.setFont("Helvetica", 9)
            self.c.drawCentredString(xx + bar_w / 2, y - 0.18 * inch, label)

    def save(self):
        self.c.save()


def build():
    product = products[0]
    engine = SupplyPlanningEngine(product)
    inv = engine.inventory_health()
    shortage = engine.po_shortage()
    supplier = engine.supplier_health()
    backlog = engine.backlog_risk()
    pull = engine.pull_logic()
    push = engine.push_logic()

    deck = Deck(OUT)
    deck.title_slide()

    deck.new_slide("Executive view", "What I would do first")
    deck.kpi_card(0.8 * inch, 4.75 * inch, 1.75 * inch, 0.95 * inch, "On Hand", fmt(engine.total_on_hand()), BLUE)
    deck.kpi_card(2.8 * inch, 4.75 * inch, 1.75 * inch, 0.95 * inch, "Immediate Ship", "4,000", TEAL)
    deck.kpi_card(4.8 * inch, 4.75 * inch, 1.75 * inch, 0.95 * inch, "Delayed PO", "6,000", AMBER)
    deck.kpi_card(6.8 * inch, 4.75 * inch, 1.75 * inch, 0.95 * inch, "Backlog", fmt(product["backlog"]), RED)
    deck.kpi_card(8.8 * inch, 4.75 * inch, 1.75 * inch, 0.95 * inch, "New Buy", fmt(shortage["Recommended PO"]), GREEN)
    deck.panel(0.8 * inch, 1.0 * inch, 11.5 * inch, 2.85 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 18)
    deck.c.drawString(1.05 * inch, 3.42 * inch, "Recommendation")
    deck.bullet_list(
        [
            "Treat this as a controlled supply disruption, not just a late shipment.",
            "Validate recovery with the contract manufacturer before changing customer commitments.",
            "Use a repeatable decision sequence: optimise existing supply first, then buy only for the remaining gap.",
            "Publish a daily Executive Decision Report until backlog risk and supplier recovery are stable.",
        ],
        1.08 * inch,
        3.02 * inch,
        10.6 * inch,
        size=12.4,
        leading=18,
    )

    deck.new_slide("Framework", "My planning decision engine")
    deck.c.setFillColor(MUTED)
    deck.c.setFont("Helvetica", 13)
    deck.draw_wrapped(
        "The framework is adapted from a planning and reporting concept I previously implemented at Apple. "
        "I used the same operating logic here because the case asks for judgement under constrained supply.",
        0.85 * inch,
        5.65 * inch,
        10.8 * inch,
        17,
        MUTED,
        "Helvetica",
        13,
    )
    deck.flow(
        [
            "Inventory Health",
            "Stock Balance",
            "Pull Logic",
            "Push Logic",
            "PO Shortage",
            "Allocation",
            "Backlog Risk",
        ],
        0.8 * inch,
        3.85 * inch,
        11.75 * inch,
        [BLUE, TEAL, PURPLE, AMBER, RED],
    )
    deck.panel(0.8 * inch, 1.2 * inch, 5.55 * inch, 1.85 * inch)
    deck.panel(6.75 * inch, 1.2 * inch, 5.55 * inch, 1.85 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(1.05 * inch, 2.62 * inch, "Why this sequence")
    deck.bullet_list(["Avoid unnecessary buying", "Make trade-offs visible", "Create repeatable decision ownership"], 1.08 * inch, 2.25 * inch, 4.8 * inch, size=11)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(7.0 * inch, 2.62 * inch, "What the tool adds")
    deck.bullet_list(["Fast scenario view", "Consistent KPI logic", "A single place to explain recommendations"], 7.03 * inch, 2.25 * inch, 4.8 * inch, bullet_color=TEAL, size=11)

    deck.new_slide("Assumptions", "How I interpreted the case")
    deck.table(
        [
            ["Area", "Assumption", "Why it matters"],
            ["Lead time", "8 weeks manufacturing + 2 weeks shipping", "Planning must use availability date, not production finish."],
            ["Open PO", "10,000 includes 4,000 in transit + 6,000 delayed", "Avoids double-counting supply."],
            ["Demand", "Regional demand is confirmed open demand", "Allocation should protect commitments."],
            ["Network", "Central receipt before regional allocation", "Keeps focus on planning and prioritisation."],
            ["Scope", "Finished goods only", "Excludes service parts, RMA and reverse logistics."],
        ],
        0.85 * inch,
        5.35 * inch,
        [1.25 * inch, 4.0 * inch, 5.7 * inch],
        row_h=0.5 * inch,
    )

    deck.new_slide("Part A", "First 48 hours: control the disruption")
    deck.panel(0.8 * inch, 1.0 * inch, 3.55 * inch, 4.55 * inch)
    deck.panel(4.65 * inch, 1.0 * inch, 3.55 * inch, 4.55 * inch)
    deck.panel(8.5 * inch, 1.0 * inch, 3.55 * inch, 4.55 * inch)
    for x, title, items, accent in [
        (0.8, "Stabilise", ["Validate shortage root cause", "Confirm 4,000 ship date", "Lock recovery date for 6,000", "Check expedite options"], BLUE),
        (4.65, "Decide", ["Review WOS and backlog", "Assess customer commitments", "Run stock balance / pull / push", "Calculate planning deficit"], TEAL),
        (8.5, "Communicate", ["Align Sales, Finance, Logistics", "Brief distributor-facing teams", "Share dates and caveats", "Move to daily recovery cadence"], AMBER),
    ]:
        deck.c.setFillColor(accent)
        deck.c.rect(x * inch, 5.48 * inch, 3.55 * inch, 0.07 * inch, fill=1, stroke=0)
        deck.c.setFillColor(TEXT)
        deck.c.setFont("Helvetica-Bold", 16)
        deck.c.drawString((x + 0.22) * inch, 5.05 * inch, title)
        deck.bullet_list(items, (x + 0.25) * inch, 4.55 * inch, 2.85 * inch, bullet_color=accent, size=11.2, leading=16)

    deck.new_slide("Part A", "Supplier management and risk monitoring")
    deck.table(
        [
            ["Question", "What I would confirm"],
            ["Root cause", "Component constraint, affected build quantity, fix owner, and recurrence risk."],
            ["Recovery plan", "Committed ship dates, capacity plan, expedite options, and supplier constraints."],
            ["Customer impact", "Open demand, backlog, launch risk, and order priority by region."],
            ["Controls", "Daily supplier update, PO health dashboard, exception alerts, and escalation path."],
        ],
        0.85 * inch,
        5.3 * inch,
        [2.0 * inch, 9.0 * inch],
        row_h=0.58 * inch,
    )
    deck.panel(0.85 * inch, 0.4 * inch, 11.0 * inch, 2.0 * inch)
    deck.c.setFillColor(RED)
    deck.c.setFont("Helvetica-Bold", 14)
    deck.c.drawString(1.1 * inch, 1.95 * inch, "Risks to monitor")
    deck.bullet_list(
        ["Recovery date slippage", "Backlog growth", "Distributor confidence", "Working capital pressure", "Expedite cost and logistics capacity"],
        1.1 * inch,
        1.58 * inch,
        10.2 * inch,
        bullet_color=RED,
        size=10.5,
        leading=13,
    )

    deck.new_slide("Part B", "Allocation method for the first 4,000 units")
    deck.kpi_card(0.85 * inch, 4.85 * inch, 1.85 * inch, 0.9 * inch, "Available", "4,000", BLUE)
    deck.kpi_card(2.95 * inch, 4.85 * inch, 1.85 * inch, 0.9 * inch, "Open Demand", "9,500", RED)
    deck.kpi_card(5.05 * inch, 4.85 * inch, 1.85 * inch, 0.9 * inch, "Gap", "5,500", AMBER)
    deck.kpi_card(7.15 * inch, 4.85 * inch, 1.85 * inch, 0.9 * inch, "Priority", "US launch", TEAL)
    deck.panel(0.85 * inch, 1.0 * inch, 5.2 * inch, 3.1 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(1.1 * inch, 3.65 * inch, "Allocation principles")
    deck.bullet_list(
        [
            "Start with confirmed customer commitments, not forecast alone.",
            "Protect the US launch because it has immediate commercial exposure.",
            "Preserve EU baseline service where possible.",
            "Keep APAC visible as a strategic market, even if supply is constrained.",
        ],
        1.1 * inch,
        3.25 * inch,
        4.45 * inch,
        size=10.8,
        leading=15,
    )
    deck.panel(6.45 * inch, 1.0 * inch, 5.35 * inch, 3.1 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(6.7 * inch, 3.65 * inch, "Trade-off")
    deck.bullet_list(
        [
            "A strict allocation engine gives a transparent answer, but business judgement still matters.",
            "I would agree the final split with Sales and leadership before distributor communication.",
            "Any region receiving less than requested gets a date, rationale, and recovery cadence.",
        ],
        6.7 * inch,
        3.25 * inch,
        4.55 * inch,
        bullet_color=AMBER,
        size=10.8,
        leading=15,
    )

    deck.new_slide("Part B", "Allocation recommendation and monitoring")
    deck.table(
        [
            ["Region", "Demand", "Priority rationale", "Communication message"],
            ["US", "4,500", "Promotional launch next week", "Prioritise launch coverage; confirm remaining recovery timing."],
            ["EU", "3,000", "Stable baseline demand", "Protect key commitments; explain temporary constraint."],
            ["APAC", "2,000", "Strategic growth market", "Keep allocation visible; avoid silent deprioritisation."],
        ],
        0.85 * inch,
        5.25 * inch,
        [1.0 * inch, 1.0 * inch, 3.2 * inch, 5.65 * inch],
        row_h=0.58 * inch,
    )
    deck.panel(0.85 * inch, 0.8 * inch, 11 * inch, 2.0 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(1.1 * inch, 2.32 * inch, "Success measures")
    deck.bullet_list(["Fill rate by region", "Backlog aging", "Launch fulfilment", "Distributor escalations", "Recovery date adherence"], 1.1 * inch, 1.9 * inch, 10.2 * inch, bullet_color=GREEN, size=10.6, leading=13)

    deck.new_slide("Part C", "Replenishment decision")
    for i, (label, value, accent) in enumerate(
        [
            ("Current WOS", f"{inv['Current WOS']}", BLUE),
            ("Pipeline WOS", f"{inv['Pipeline WOS']}", TEAL),
            ("Target WOS", f"{inv['Target WOS']}", PURPLE),
            ("Planning Deficit", fmt(inv["Planning Deficit"]), AMBER),
            ("Recommended PO", fmt(shortage["Recommended PO"]), GREEN),
        ]
    ):
        deck.kpi_card((0.85 + i * 2.08) * inch, 4.8 * inch, 1.78 * inch, 0.9 * inch, label, value, accent)
    deck.panel(0.85 * inch, 1.0 * inch, 5.35 * inch, 2.95 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(1.1 * inch, 3.5 * inch, "Decision")
    deck.bullet_list(
        [
            "Place a new PO only after stock balance, pull and push options are reviewed.",
            "The remaining planning deficit is 2,076 units.",
            "Because MOQ is 5,000 units, recommended new buy is 5,000 units.",
            "Position this as risk protection, not speculative over-buying.",
        ],
        1.1 * inch,
        3.1 * inch,
        4.55 * inch,
        size=10.8,
        leading=15,
    )
    deck.panel(6.55 * inch, 1.0 * inch, 5.35 * inch, 2.95 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(6.8 * inch, 3.5 * inch, "Finance justification")
    deck.bullet_list(
        [
            "Show WOS, open PO and backlog in one view.",
            "Explain MOQ constraint and recovery timing.",
            "Separate confirmed demand risk from optional buffer.",
            "Review weekly as forecast and supplier recovery change.",
        ],
        6.8 * inch,
        3.1 * inch,
        4.55 * inch,
        bullet_color=TEAL,
        size=10.8,
        leading=15,
    )

    deck.new_slide("Part C", "Reporting and systems I would build")
    deck.table(
        [
            ["Dashboard / Workflow", "Purpose", "Frequency"],
            ["Inventory Health", "WOS, inventory position, stock-out risk", "Daily"],
            ["Purchase Order Health", "Open PO, in transit, delayed supply, revised dates", "Daily"],
            ["Supplier Health", "Lead time, OTD, recovery commitments", "Daily"],
            ["Forecast Accuracy", "Demand signal quality and bias", "Weekly"],
            ["Executive Decision Report", "Single view of risk, action and owner", "Daily during disruption"],
        ],
        0.85 * inch,
        5.35 * inch,
        [2.5 * inch, 6.2 * inch, 2.0 * inch],
        row_h=0.48 * inch,
    )
    deck.c.setFillColor(MUTED)
    deck.c.setFont("Helvetica", 11)
    deck.c.drawString(0.9 * inch, 1.0 * inch, "ERP note: the same control logic can sit in NetSuite workflows or another ERP/reporting layer.")

    deck.new_slide("Part D", "SOP and escalation model")
    deck.flow(
        ["Supplier issue", "Validate", "Inventory health", "Optimise supply", "New buy / allocation", "Daily report"],
        0.85 * inch,
        4.8 * inch,
        11.4 * inch,
        [RED, AMBER, BLUE, TEAL, PURPLE, GREEN],
    )
    deck.table(
        [
            ["Trigger", "Action"],
            ["Current WOS >= target", "Routine monitoring"],
            ["Current WOS < 8 weeks", "Planner review"],
            ["Current WOS < 6 weeks", "Management review with Procurement"],
            ["Current WOS < 4 weeks", "Executive recovery meeting with supplier"],
        ],
        0.85 * inch,
        3.65 * inch,
        [3.2 * inch, 7.5 * inch],
        row_h=0.45 * inch,
    )
    deck.c.setFillColor(MUTED)
    deck.c.setFont("Helvetica", 11)
    deck.c.drawString(0.9 * inch, 0.95 * inch, "Purpose: make escalation based on measurable risk, not late-stage surprise.")

    deck.new_slide("Part D", "Governance, stakeholders and success metrics")
    deck.table(
        [
            ["Decision", "Owner"],
            ["Inventory health / stock balance", "Supply Planner"],
            ["Pull / push logic", "Supply Planner + Procurement"],
            ["New buy approval", "Procurement + Finance"],
            ["Allocation decision", "Supply Planning Manager + Sales"],
            ["Executive escalation", "Operations leadership"],
        ],
        0.85 * inch,
        5.35 * inch,
        [4.1 * inch, 3.3 * inch],
        row_h=0.42 * inch,
    )
    deck.panel(8.65 * inch, 2.35 * inch, 3.25 * inch, 3.0 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 15)
    deck.c.drawString(8.9 * inch, 4.9 * inch, "KPIs")
    deck.bullet_list(["Fill rate >98%", "Target WOS 12 weeks", "Supplier OTD >95%", "Backlog <1,000", "PO expedites <5%"], 8.9 * inch, 4.48 * inch, 2.55 * inch, bullet_color=GREEN, size=10.8, leading=15)

    deck.new_slide("Part D", "Broader supply chain risk reduction")
    risk_items = [
        ("Supplier diversification", "Qualify backup manufacturing options."),
        ("Safety stock strategy", "Differentiate by demand variability and criticality."),
        ("Lead-time management", "Track trends and trigger early warnings."),
        ("Concentration risk", "Reduce dependency on one site where practical."),
        ("Tariffs and duties", "Include landed cost in sourcing decisions."),
        ("Inventory positioning", "Place stock closer to demand where justified."),
    ]
    for i, (title, body) in enumerate(risk_items):
        x = (0.85 + (i % 3) * 3.85) * inch
        y = (4.5 - (i // 3) * 1.75) * inch
        deck.panel(x, y, 3.35 * inch, 1.25 * inch)
        deck.c.setFillColor([BLUE, TEAL, AMBER, PURPLE, RED, GREEN][i])
        deck.c.rect(x, y + 1.18 * inch, 3.35 * inch, 0.07 * inch, fill=1, stroke=0)
        deck.c.setFillColor(TEXT)
        deck.c.setFont("Helvetica-Bold", 12)
        deck.c.drawString(x + 0.16 * inch, y + 0.85 * inch, title)
        deck.draw_wrapped(body, x + 0.16 * inch, y + 0.55 * inch, 2.95 * inch, 12, MUTED, "Helvetica", 9.5)

    deck.new_slide("Final recommendation", "What I would leave behind")
    deck.panel(0.85 * inch, 1.0 * inch, 11.3 * inch, 4.55 * inch)
    deck.c.setFillColor(TEXT)
    deck.c.setFont("Helvetica-Bold", 17)
    deck.c.drawString(1.12 * inch, 5.08 * inch, "A scalable decision-support rhythm")
    deck.bullet_list(
        [
            "Resolve the immediate disruption through a daily supplier recovery and allocation cadence.",
            "Use the decision hierarchy to justify buying decisions and avoid reactive procurement.",
            "Turn the Streamlit prototype logic into an operating dashboard for planners, procurement and leadership.",
            "Keep the discussion centred on assumptions, trade-offs and clear ownership.",
        ],
        1.15 * inch,
        4.55 * inch,
        10.4 * inch,
        bullet_color=BLUE,
        size=13,
        leading=20,
    )

    deck.new_slide("Part F", "How I used AI")
    deck.panel(0.9 * inch, 1.2 * inch, 11.15 * inch, 4.2 * inch)
    deck.bullet_list(
        [
            "I had the planning framework and concept before using AI.",
            "The core logic was my own and based on a concept I had implemented previously at Apple.",
            "I used AI to help build the Streamlit prototype and improve the presentation quality.",
            "I reviewed and adjusted the output so the final submission reflected my own planning judgement.",
        ],
        1.25 * inch,
        4.75 * inch,
        10.1 * inch,
        bullet_color=TEAL,
        size=14,
        leading=24,
    )

    deck.save()
    return OUT


if __name__ == "__main__":
    print(build())
