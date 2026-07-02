import streamlit as st
import pandas as pd

from sample_data import products
from planning_engine import SupplyPlanningEngine
from report_engine import ReportEngine


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Supply Planning Decision Report",
    page_icon="📦",
    layout="wide"
)

# ======================================================
# HEADER
# ======================================================

st.title("📦 Supply Planning Decision Report")

st.caption(
    "Business Case Demonstration | Nabu Casa | OEM Priority Decision Engine"
)

st.info(
"""
This application demonstrates how supply planning decisions can be supported
through rule-based reporting.

The report addresses:

• Part A – Supply Disruption Management

• Part B – Inventory Allocation

• Part C – Inventory Planning & Replenishment

• Part D – Reporting & Risk Management

using a structured decision engine similar to an OEM Supply Planning Report.
"""
)

st.divider()

# ======================================================
# PRODUCT SELECTION
# ======================================================

selected = st.selectbox(

    "Select Product",

    [p["part_number"] for p in products]

)

product = next(

    p

    for p in products

    if p["part_number"] == selected

)

engine = SupplyPlanningEngine(product)

report = ReportEngine(engine)

# ======================================================
# BUSINESS CASE INPUT
# ======================================================

st.header("📄 Business Case Scenario")

left, right = st.columns(2)

with left:

    st.subheader("Current Position")

    current = pd.DataFrame({

        "Metric":[

            "Lead Time",

            "Shipping Time",

            "Total Lead Time",

            "MOQ",

            "On Hand",

            "Open Purchase Order",

            "In Transit",

            "PO Balance"

        ],

        "Value":[

            "8 Weeks",

            "2 Weeks",

            "10 Weeks",

            "5,000",

            "8,000",

            "10,000",

            "4,000",

            "6,000"

        ]

    })

    st.table(current)

with right:

    st.subheader("Regional Open Demand")

    demand = pd.DataFrame({

        "Region":[

            "🇪🇺 EU",

            "🇺🇸 US",

            "🌏 APAC"

        ],

        "Open Demand":[

            "3,000",

            "4,500",

            "2,000"

        ]

    })

    st.table(demand)

st.divider()

# ======================================================
# FORECAST
# ======================================================

st.header("📈 Forecast")

forecast = pd.DataFrame({

    "Month":[

        "Month 1",

        "Month 2",

        "Month 3",

        "Month 4"

    ],

    "Forecast":[

        "6,000",

        "7,500",

        "9,000",

        "6,500"

    ]

})

st.table(forecast)
st.divider()

# ======================================================
# PLANNING METRICS
# ======================================================

st.header("📊 Planning Metrics")

avg_monthly = round(sum(product["monthly_forecast"]) / 4)

avg_weekly = product["weekly_demand"]

planning = pd.DataFrame({

    "Metric":[

        "Average Monthly Forecast",

        "Average Weekly Run Rate",

        "Current Weeks of Supply",

        "Pipeline Weeks of Supply",

        "Pipeline Disruption WOS",

        "Target Weeks of Supply"

    ],

    "Value":[

        f"{avg_monthly:,} Units",

        f"{avg_weekly:,} Units",

        "4.8 Weeks",

        "10.8 Weeks",

        "7.2 Weeks",

        "12 Weeks"

    ]

})

st.table(planning)

st.divider()

# ======================================================
# DECISION SUMMARY
# ======================================================

st.header("🚦Decision Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Current WOS",

        "4.8",

        "-7.2 vs Target"

    )

with col2:

    st.metric(

        "Inventory Gap",

        "7,328",

        "Units"

    )

with col3:

    st.metric(

        "Backlog",

        "9,500",

        "Critical"

    )

with col4:

    st.metric(

        "Supplier",

        "CMHK",

        "High Risk"

    )

st.divider()

# ======================================================
# INTERVIEW ASSUMPTIONS
# ======================================================

st.header("📌 Planning Assumptions")

st.markdown("""

### Business Assumptions

- Regional demand represents current open customer orders awaiting fulfilment.

- Target inventory policy is **12 Weeks of Supply**
(8 weeks manufacturing + 2 weeks shipping + 2 weeks safety buffer).

- Purchase Orders are prioritised using **Oldest PO First**.

- OEM Capacity is balanced by **pushing the newest Purchase Orders**.

- New Buy Purchase Orders are only recommended after:

    • Stock Balance

    • Pull Logic

    • Push Logic

have all been exhausted.

- Current backlog represents customer orders already waiting for supply.

- Backlog Risk is determined using current backlog together with supplier lead time.

""")

st.divider()
# ======================================================
# BUSINESS CASE TABS
# ======================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🅰 Part A - Supply Disruption",
        "🅱 Part B - Allocation",
        "🅲 Part C - Inventory Planning",
        "📊 Executive Report"
    ]
)

# ======================================================
# PART A
# ======================================================

with tab1:

    st.header("Part A - Supply Disruption Management")

    st.subheader("Scenario")

    st.warning("""
Two days before shipment, the manufacturer confirms that only 4,000 units
can ship immediately.

The remaining 6,000 units will be delayed by approximately three weeks.
""")

    st.subheader("First 48 Hours Priorities")

    priorities = [
        "Contact Contract Manufacturer",
        "Confirm Root Cause",
        "Validate Revised Shipment Schedule",
        "Assess Inventory Position",
        "Review Customer Backlog",
        "Review Open Purchase Orders",
        "Evaluate Stock Balance Opportunities",
        "Prepare Internal Stakeholder Update"
    ]

    for p in priorities:
        st.checkbox(p, value=True)

    st.subheader("Stakeholders")

    stakeholders = {
        "Stakeholder": [
            "Supply Planning",
            "Finance",
            "Sales",
            "Customer Support",
            "Warehouse",
            "Contract Manufacturer"
        ],
        "Reason": [
            "Inventory Planning",
            "Working Capital",
            "Customer Commitments",
            "Distributor Communication",
            "Receiving Schedule",
            "Recovery Plan"
        ]
    }

    st.table(pd.DataFrame(stakeholders))

    st.subheader("Key Risks")

    risks = pd.DataFrame({

        "Risk":[

            "Customer Backlog",

            "Lost Revenue",

            "Promotion Risk",

            "Supplier Delay",

            "Inventory Shortage"

        ],

        "Impact":[

            "High",

            "High",

            "High",

            "Critical",

            "Critical"

        ]

    })

    st.dataframe(
        risks,
        use_container_width=True,
        hide_index=True
    )

# ======================================================
# PART B
# ======================================================

with tab2:

    st.header("Part B - Inventory Allocation")

    allocation = engine.allocation_engine()

    st.metric(
        "Available Inventory",
        "4,000 Units"
    )

    st.subheader("Allocation Priority")

    st.markdown("""

1. 🇺🇸 US

Major promotional launch

2. 🇪🇺 EU

Stable baseline demand

3. 🌏 APAC

Strategic growth market

""")

    rows = []

    for region, values in allocation["Regions"].items():

        rows.append({

            "Region": region,

            "Demand": values["Demand"],

            "Allocated": values["Allocated"],

            "Backlog": values["Backlog"],

            "Fill Rate %": values["Fill Rate"]

        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Trade-offs")

    st.info("""
US receives priority due to promotional commitments.

EU receives baseline supply to protect existing revenue.

APAC receives remaining inventory to maintain long-term strategic growth.
""")
    # ======================================================
# PART C
# ======================================================

with tab3:

    st.header("Part C - Inventory Planning & Replenishment")

    shortage = engine.po_shortage()

    st.subheader("Planning Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Current WOS",
            "4.8 Weeks"
        )

    with c2:

        st.metric(
            "Target WOS",
            "12 Weeks"
        )

    with c3:

        st.metric(
            "Inventory Gap",
            "7,328 Units"
        )

    st.divider()

    st.subheader("Decision Hierarchy")

    st.markdown("""

### Step 1 — Stock Balance

Transfer inventory from regions above **12 Weeks of Supply**.

↓

### Step 2 — Pull Logic

Prioritise the **Oldest Purchase Orders**.

↓

### Step 3 — Push Logic

Push the **Newest Purchase Orders** to free OEM build capacity.

↓

### Step 4 — PO Shortage

If Pull + Push cannot recover supply,

recommend a **New Buy Purchase Order**.

""")

    st.divider()

    st.subheader("Purchase Order Recommendation")

    recommendation = pd.DataFrame({

        "Decision":[

            "Current WOS",

            "Pipeline WOS",

            "Disruption WOS",

            "Target WOS",

            "Recommended New Buy"

        ],

        "Value":[

            "4.8",

            "10.8",

            "7.2",

            "12",

            f'{shortage["Recommended PO"]:,} Units'

        ]

    })

    st.table(recommendation)

    st.divider()

    st.subheader("Finance Justification")

    st.success("""

A new Purchase Order is recommended only after

• Stock Balance

• Pull Logic

• Push Logic

have been exhausted.

This minimises excess inventory while maintaining the target
12 Weeks of Supply.

""")

# ======================================================
# EXECUTIVE REPORT
# ======================================================

with tab4:

    st.header("Executive Decision Report")

    report.render()

# ======================================================
# FOOTER
# ======================================================

st.divider()

st.markdown("## Reporting & Systems")

st.markdown("""

This prototype demonstrates the reporting that would support ongoing supply planning.

### Dashboards

- Inventory Health
- Purchase Order Health
- Supplier Lead Time
- Weeks of Supply
- Stock Balance Opportunities
- Pull Recommendations
- Push Recommendations
- PO Shortage
- Allocation Decisions
- Backlog Risk
- Decision Log

### ERP Integration

This solution could integrate with:

- NetSuite
- SAP
- Oracle
- Microsoft Dynamics

### Future Enhancements

- Live ERP Integration
- Automated Supplier Alerts
- Email Notifications
- Historical Trend Analysis
- AI Decision Recommendations
- Multi-Supplier Planning
- Multi-Site Inventory Optimisation

""")

st.caption(
    "Supply Planning Decision Report | Business Case Demonstration | Version 1.0"
)
    