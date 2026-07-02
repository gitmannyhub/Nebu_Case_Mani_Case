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

st.subheader("Prepared by Manikandan Sankaran")

st.caption(
    "Business Case Demonstration | Nabu Casa | Supply Planning Decision Framework"
)

st.divider()

# ======================================================
# PRODUCT SELECTION
# ======================================================

with st.container(border=True):

    st.subheader("Select Product")

    selected = st.selectbox(

        "Product",

        [p["part_number"] for p in products],

        label_visibility="collapsed"

    )

product = next(

    p

    for p in products

    if p["part_number"] == selected

)

# ======================================================
# INITIALISE ENGINE
# ======================================================

engine = SupplyPlanningEngine(product)

report = ReportEngine(engine)

inventory = engine.inventory_health()

shortage = engine.po_shortage()

allocation = engine.allocation_engine()

backlog = engine.backlog_risk()

supplier = engine.supplier_health()

# ======================================================
# APPLICATION TABS
# ======================================================

tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📝 Planning Assumptions & Scope",
        "📊 Executive Decision Report",
        "🅰 Part A",
        "🅱 Part B",
        "🅲 Part C",
        "🅳 Part D"
    ]
)

# ======================================================
# EXECUTIVE DECISION REPORT
# ======================================================

with tab1:

    report.render()
# ======================================================
# PLANNING ASSUMPTIONS & SCOPE
# ======================================================

with tab0:

    st.header("📝 Planning Assumptions & Scope")

    with st.container(border=True):

        st.markdown("""
This business case intentionally leaves several areas open to interpretation.
The following assumptions were made to create a consistent, realistic and
repeatable Supply Planning Decision Framework.

These assumptions establish the planning context for every decision made
throughout this prototype.
""")

    # ======================================================
    # PURCHASE ORDER TIMELINE
    # ======================================================

    with st.container(border=True):

        st.subheader("📅 Purchase Order Timeline")

        st.markdown("""

**Assumption**

The existing **10,000-unit Purchase Order** is assumed to have been
created approximately **10 weeks** before the expected delivery.

The replenishment timeline is interpreted as:

• Manufacturing Lead Time = **8 Weeks**

• Shipping & Logistics = **2 Weeks**

• Total Replenishment Lead Time = **10 Weeks**

Two days before the planned shipment, the supplier confirms that
only **4,000 units** can ship due to a component shortage, with the
remaining **6,000 units** arriving approximately three weeks later.

**Reason**

The case does not specify the Purchase Order creation date or
shipping duration, therefore a realistic replenishment timeline
has been assumed.

""")

    # ======================================================
    # LEAD TIME
    # ======================================================

    with st.container(border=True):

        st.subheader("🚢 Lead Time Definition")

        st.markdown("""

**Assumption**

The stated **8-week Lead Time** is interpreted as the supplier's
manufacturing lead time.

Inventory planning uses the **total replenishment lead time**:

Manufacturing

8 Weeks

+

Shipping

2 Weeks

=

10 Weeks

**Reason**

Planning decisions should be based on the time until inventory
becomes available for sale rather than production completion.

""")

    # ======================================================
    # DEMAND
    # ======================================================

    with st.container(border=True):

        st.subheader("📦 Regional Open Demand")

        st.markdown("""

**Assumption**

Regional demand represents confirmed distributor and customer
purchase orders awaiting fulfilment rather than forecast demand.

""")

        demand = pd.DataFrame({

            "Region":[

                "🇺🇸 United States",

                "🇪🇺 Europe",

                "🌏 APAC"

            ],

            "Open Demand":[

                "4,500",

                "3,000",

                "2,000"

            ]

        })

        st.dataframe(

            demand,

            use_container_width=True,

            hide_index=True

        )

        st.markdown("""

**Reason**

This ensures allocation decisions prioritise confirmed customer
commitments during constrained supply.

""")

    # ======================================================
    # INVENTORY POSITION
    # ======================================================

    with st.container(border=True):

        st.subheader("📊 Inventory Position")

        st.markdown("""

**Assumption**

Open Purchase Orders already include In Transit inventory.

Therefore In Transit is **not** added again.

Inventory Position

=

On Hand

+

Open Purchase Orders

=

8,000

+

10,000

=

18,000 Units

**Reason**

This avoids double-counting inventory already contained within
the Purchase Order quantity.

""")

    # ======================================================
    # DISTRIBUTION CENTRE
    # ======================================================

    with st.container(border=True):

        st.subheader("🏢 Distribution Network")

        st.markdown("""

**Assumption**

The business case does not define the distribution network.

A single central distribution centre is assumed where inventory
is received before allocation to regional distributors.

**Reason**

This keeps the exercise focused on inventory planning,
allocation and replenishment rather than transport optimisation.

""")

    # ======================================================
    # FINISHED GOODS
    # ======================================================

    with st.container(border=True):

        st.subheader("📦 Finished Goods Scope")

        st.markdown("""

**Assumption**

The flagship product is treated as a Finished Good supplied
by a Contract Manufacturer to regional distributors.

The scope excludes:

• Service Parts

• Repair Inventory

• Reverse Logistics

• RMAs

**Reason**

The exercise focuses exclusively on Finished Goods planning.

""")

    # ======================================================
    # APPLICATION DESIGN
    # ======================================================

    with st.container(border=True):

        st.subheader("💻 Application Design Decisions")

        st.markdown("""

Although the business case contains only one product,
the planning engine has been designed to support:

• Multiple Products

• Multiple Suppliers

• Multiple Manufacturing Sites

• Multiple Regions

without changing the business logic.

This demonstrates scalability and future reuse.

""")

    # ======================================================
    # EXECUTIVE REPORT
    # ======================================================

    with st.container(border=True):

        st.subheader("📊 Executive Decision Report")

        st.markdown("""

Rather than presenting calculations independently,
this prototype generates a structured Executive Decision Report.

The design was inspired by a reporting solution I developed at Apple,
where automated business rules and reporting gave planners and buyers
early visibility of supply risks before they became customer issues.

The same principles have been adapted here to monitor:

• Inventory Health

• Purchase Order Health

• Stock Balance

• Pull Logic

• Push Logic

• Planning Deficit

• New Buy Proposal

• Allocation

• Supplier Health

• Backlog Risk

• Decision Log

• AI Executive Summary

""")

    with st.container(border=True):

        st.success(
"""
These planning assumptions provide a transparent foundation
for every recommendation generated throughout this Supply
Planning Decision Framework.
"""
        )
# ======================================================
# PART A
# ======================================================

with tab2:

    st.header("🅰 Part A — Supply Disruption Management")

    with st.container(border=True):

        st.subheader("Scenario")

        st.write(
            """
Two days before the scheduled shipment, the Contract Manufacturer
confirmed that only **4,000 units** could be shipped due to a component
shortage.

The remaining **6,000 units** would be delayed by approximately
**three weeks**.

The objective is to minimise customer impact while maintaining supply
continuity through structured planning decisions.
"""
        )

    # ======================================================
    # FIRST 48 HOURS
    # ======================================================

    with st.container(border=True):

        st.subheader("Immediate Response (First 48 Hours)")

        response = [

            "Validate supplier root cause",

            "Confirm revised production schedule",

            "Review Inventory Health",

            "Calculate Weeks of Supply",

            "Review customer backlog",

            "Review open Purchase Orders",

            "Evaluate Stock Balance",

            "Evaluate Pull opportunities",

            "Evaluate Push opportunities",

            "Calculate Planning Deficit",

            "Determine New Buy requirement",

            "Communicate recovery plan"

        ]

        for item in response:

            st.checkbox(

                item,

                value=True,

                disabled=True

            )

    # ======================================================
    # BUSINESS POSITION
    # ======================================================

    with st.container(border=True):

        st.subheader("Current Business Position")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "On Hand",

            f"{engine.total_on_hand():,}"

        )

        c2.metric(

            "Open PO",

            f"{engine.total_open_po():,}"

        )

        c3.metric(

            "In Transit",

            f"{engine.total_in_transit():,}"

        )

        c4.metric(

            "MOQ",

            f"{product['moq']:,}"

        )

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("Supply")

            supply = pd.DataFrame({

                "Metric":[

                    "Manufacturing Lead Time",

                    "Shipping",

                    "Total Lead Time",

                    "Outstanding PO"

                ],

                "Value":[

                    "8 Weeks",

                    "2 Weeks",

                    "10 Weeks",

                    f"{engine.total_open_po()-engine.total_in_transit():,}"

                ]

            })

            st.dataframe(

                supply,

                use_container_width=True,

                hide_index=True

            )

        with right:

            st.subheader("Regional Demand")

            regional = pd.DataFrame({

                "Region":[

                    "🇺🇸 United States",

                    "🇪🇺 Europe",

                    "🌏 APAC"

                ],

                "Open Demand":[

                    f"{product['regions']['US']['open_demand']:,}",

                    f"{product['regions']['EU']['open_demand']:,}",

                    f"{product['regions']['APAC']['open_demand']:,}"

                ]

            })

            st.dataframe(

                regional,

                use_container_width=True,

                hide_index=True

            )

    # ======================================================
    # RISK ASSESSMENT
    # ======================================================

    with st.container(border=True):

        st.subheader("Immediate Risk Assessment")

        risk = pd.DataFrame({

            "Risk":[

                "Supplier Delay",

                "Inventory Shortage",

                "Customer Backlog",

                "Revenue Impact",

                "Customer Experience"

            ],

            "Likelihood":[

                "High",

                "High",

                "High",

                "Medium",

                "High"

            ],

            "Impact":[

                "Critical",

                "Critical",

                "Critical",

                "High",

                "High"

            ]

        })

        st.dataframe(

            risk,

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # RECOMMENDED RESPONSE
    # ======================================================

    with st.container(border=True):

        st.subheader("Recommended Planning Response")

        st.markdown("""

1. Validate supplier recovery plan.

2. Assess Inventory Health.

3. Execute Stock Balance where possible.

4. Evaluate Pull opportunities.

5. Evaluate Push opportunities.

6. Calculate remaining Planning Deficit.

7. Raise a New Buy only if optimisation cannot recover the deficit.

8. Allocate inventory according to business priorities.

9. Communicate the recovery plan to stakeholders.

10. Monitor supplier recovery through the Executive Decision Report.

""")

        st.success(
            """
The response follows a structured planning hierarchy that prioritises
inventory optimisation before recommending additional procurement.
"""
        )
# ======================================================
# PART B
# ======================================================

with tab3:

    st.header("🅱 Part B — Inventory Allocation")

    with st.container(border=True):

        st.subheader("Allocation Objective")

        st.write(
            """
With inventory constrained, the objective is to allocate available
inventory in a transparent and repeatable manner while balancing:

• Customer commitments

• Commercial priorities

• Strategic market objectives

• Available inventory

The allocation engine follows the agreed priority:

🇺🇸 United States

↓

🇪🇺 Europe

↓

🌏 APAC
"""
        )

    # ======================================================
    # INVENTORY SUMMARY
    # ======================================================

    with st.container(border=True):

        st.subheader("Inventory Summary")

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Available Inventory",

            f'{allocation["Available Inventory"]:,} Units'

        )

        c2.metric(

            "Regional Demand",

            f'{engine.total_open_demand():,} Units'

        )

        c3.metric(

            "Remaining Inventory",

            f'{allocation["Remaining Inventory"]:,} Units'

        )

    # ======================================================
    # ALLOCATION RESULTS
    # ======================================================

    with st.container(border=True):

        st.subheader("Allocation Results")

        rows = []

        for region, values in allocation["Regions"].items():

            rows.append({

                "Region": region,

                "Open Demand": values["Demand"],

                "Allocated": values["Allocated"],

                "Backlog": values["Backlog"],

                "Fill Rate %": values["Fill Rate"]

            })

        st.dataframe(

            pd.DataFrame(rows),

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # ALLOCATION PRIORITY
    # ======================================================

    with st.container(border=True):

        st.subheader("Allocation Strategy")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.success(
"""
### 🇺🇸 Priority 1

**United States**

Protect promotional launch commitments and
highest commercial exposure.
"""
            )

        with col2:

            st.info(
"""
### 🇪🇺 Priority 2

**Europe**

Protect confirmed customer commitments and
maintain service levels.
"""
            )

        with col3:

            st.warning(
"""
### 🌏 Priority 3

**APAC**

Support strategic regional growth while
maximising available inventory.
"""
            )

    # ======================================================
    # DECISION FACTORS
    # ======================================================

    with st.container(border=True):

        st.subheader("Decision Factors")

        left, right = st.columns(2)

        with left:

            st.markdown("""
### Planning Considerations

✅ Customer Commitments

✅ Commercial Priorities

✅ Available Inventory

✅ Regional Demand

✅ Fill Rate

✅ Revenue Protection

✅ Strategic Growth

✅ Customer Experience
""")

        with right:

            st.markdown("""
### Potential Business Impacts

• Reduced Fill Rate

• Increased Customer Backlog

• Lost Revenue

• Customer Dissatisfaction

• Delayed Promotional Activity

• Increased Expedite Costs

• Longer Supply Recovery
""")

    # ======================================================
    # RECOMMENDED ACTIONS
    # ======================================================

    with st.container(border=True):

        st.subheader("Recommended Actions")

        st.markdown("""

1. Execute the approved allocation strategy.

2. Notify Sales of constrained inventory.

3. Communicate revised fulfilment dates.

4. Continue supplier recovery monitoring.

5. Review inventory position daily.

6. Re-run allocation after every significant inventory movement.

7. Update stakeholders through the Executive Decision Report.

""")

        st.success(
"""
The allocation engine provides a transparent and repeatable
method for distributing constrained inventory while balancing
customer commitments, commercial priorities and long-term
strategic objectives.
"""
        )
# ======================================================
# PART C
# ======================================================

with tab4:

    st.header("🅲 Part C — Inventory Planning & Replenishment")

    with st.container(border=True):

        st.subheader("Planning Objective")

        st.write(
            """
The objective is to determine whether additional inventory should
be purchased after all optimisation opportunities have been
evaluated.

The planning engine follows a structured hierarchy that prioritises
inventory optimisation before recommending additional procurement.
"""
        )

    # ======================================================
    # PLANNING FORMULA
    # ======================================================

    with st.container(border=True):

        st.subheader("Planning Methodology")

        st.code(
"""
Target Inventory

=

Target Weeks of Supply

×

Average Weekly Demand


Inventory Position

=

On Hand

+

Open Purchase Orders

(Open Purchase Orders already include
In Transit inventory)


Planning Deficit

=

Target Inventory

−

Inventory Position


Recommended New Buy

=

MAX(Planning Deficit, Supplier MOQ)
"""
        )

    # ======================================================
    # INVENTORY DASHBOARD
    # ======================================================

    with st.container(border=True):

        st.subheader("Inventory Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "Current WOS",

            f'{inventory["Current WOS"]} Weeks'

        )

        c2.metric(

            "Pipeline WOS",

            f'{inventory["Pipeline WOS"]} Weeks'

        )

        c3.metric(

            "Disruption WOS",

            f'{inventory["Disruption WOS"]} Weeks'

        )

        c4.metric(

            "Target WOS",

            f'{inventory["Target WOS"]} Weeks'

        )

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Target Inventory",

            f'{inventory["Target Inventory"]:,}'

        )

        c2.metric(

            "Inventory Position",

            f'{inventory["Inventory Position"]:,}'

        )

        c3.metric(

            "Planning Deficit",

            f'{inventory["Planning Deficit"]:,}'

        )

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Supplier MOQ",

            f'{product["moq"]:,}'

        )

        c2.metric(

            "Recommended New Buy",

            f'{shortage["Recommended PO"]:,}'

        )

        c3.metric(

            "Supplier",

            supplier["Supplier"]

        )

    # ======================================================
    # DECISION HIERARCHY
    # ======================================================

    with st.container(border=True):

        st.subheader("Supply Planning Decision Hierarchy")

        steps = [

            (
                "1️⃣ Inventory Health",
                "Review Current WOS, Pipeline WOS and Inventory Position."
            ),

            (
                "2️⃣ Stock Balance",
                "Transfer inventory from regions operating above Target WOS."
            ),

            (
                "3️⃣ Pull Logic",
                "Bring forward the oldest Purchase Orders where possible."
            ),

            (
                "4️⃣ Push Logic",
                "Delay lower-priority Purchase Orders to recover supplier capacity."
            ),

            (
                "5️⃣ Planning Deficit",
                "Calculate the remaining inventory gap after optimisation."
            ),

            (
                "6️⃣ New Buy Proposal",
                "Recommend procurement only when optimisation cannot recover the remaining deficit."
            )

        ]

        for title, description in steps:

            with st.container(border=True):

                st.markdown(f"### {title}")

                st.write(description)

    # ======================================================
    # STOCK BALANCE
    # ======================================================

    with st.container(border=True):

        st.subheader("Step 1 — Stock Balance")

        balance = engine.stock_balance()

        if balance["Status"] == "SUCCESS":

            st.success(balance["Recommendation"])

            st.dataframe(

                pd.DataFrame(balance["Transfers"]),

                use_container_width=True,

                hide_index=True

            )

        else:

            st.warning(balance["Recommendation"])

    # ======================================================
    # PULL & PUSH
    # ======================================================

    left, right = st.columns(2)

    with left:

        with st.container(border=True):

            st.subheader("Step 2 — Pull Logic")

            pull = engine.pull_logic()

            st.metric(

                "Pulled Quantity",

                f'{pull["Pulled Qty"]:,} Units'

            )

            st.info(

                pull["Recommendation"]

            )

            if pull["POs"]:

                st.dataframe(

                    pd.DataFrame(pull["POs"]),

                    use_container_width=True,

                    hide_index=True

                )

    with right:

        with st.container(border=True):

            st.subheader("Step 3 — Push Logic")

            push = engine.push_logic()

            st.metric(

                "Pushed Quantity",

                f'{push["Pushed Qty"]:,} Units'

            )

            st.info(

                push["Recommendation"]

            )

            if push["POs"]:

                st.dataframe(

                    pd.DataFrame(push["POs"]),

                    use_container_width=True,

                    hide_index=True

                )

    # ======================================================
    # FINAL DECISION
    # ======================================================

    with st.container(border=True):

        st.subheader("Final Planning Decision")

        c1, c2, c3 = st.columns(3)

        c1.metric(

            "Planning Deficit",

            f'{shortage["Planning Deficit"]:,}'

        )

        c2.metric(

            "Supplier MOQ",

            f'{shortage["MOQ"]:,}'

        )

        c3.metric(

            "Recommended New Buy",

            f'{shortage["Recommended PO"]:,}'

        )

        st.success(
"""
The planning engine only recommends a New Buy after evaluating:

✅ Inventory Health

✅ Stock Balance

✅ Pull Logic

✅ Push Logic

For this scenario:

• Planning Deficit = 2,076 Units

• Supplier MOQ = 5,000 Units

Therefore the recommended New Buy is **5,000 Units**.

This ensures procurement decisions remain transparent,
consistent and fully aligned with supplier purchasing constraints.
"""
        )
# ======================================================
# PART D
# ======================================================

with tab5:

    st.header("🅳 Part D — Process Design & Risk Management")

    with st.container(border=True):

        st.subheader("Objective")

        st.write(
            """
Design a repeatable Supply Planning process that standardises
decision making, improves visibility and reduces supply chain risk.

The objective is not only to resolve today's disruption but to
create an operating model capable of supporting future supply
events across multiple products and suppliers.
"""
        )

    # ======================================================
    # STANDARD OPERATING PROCEDURE
    # ======================================================

    with st.container(border=True):

        st.subheader("1. Standard Operating Procedure (SOP)")

        steps = [

            ("1️⃣ Supplier Disruption",
             "Supplier confirms a production or supply constraint."),

            ("2️⃣ Validate Supplier Commitment",
             "Confirm revised production schedule, available quantity and recovery timeline."),

            ("3️⃣ Inventory Health",
             "Review Current WOS, Pipeline WOS and Inventory Position."),

            ("4️⃣ Stock Balance",
             "Evaluate regional inventory balancing opportunities."),

            ("5️⃣ Pull Logic",
             "Bring forward the oldest Purchase Orders where possible."),

            ("6️⃣ Push Logic",
             "Delay lower priority Purchase Orders to recover supplier capacity."),

            ("7️⃣ Planning Deficit",
             "Calculate the remaining inventory shortfall."),

            ("8️⃣ New Buy",
             "Raise a Purchase Order only if optimisation cannot recover the deficit."),

            ("9️⃣ Inventory Allocation",
             "Allocate constrained inventory according to business priorities."),

            ("🔟 Executive Decision Report",
             "Publish recommendations and monitor recovery daily.")

        ]

        for title, description in steps:

            with st.container(border=True):

                st.markdown(f"### {title}")

                st.write(description)

    # ======================================================
    # ESCALATION MATRIX
    # ======================================================

    with st.container(border=True):

        st.subheader("2. Escalation Triggers")

        c1, c2 = st.columns(2)

        with c1:

            st.success("""
### 🟢 Normal

Current WOS ≥ Target WOS

Routine monitoring.
""")

            st.warning("""
### 🟡 Planner Review

Current WOS < 8 Weeks

Review inventory position and recovery options.
""")

        with c2:

            st.warning("""
### 🟠 Management Review

Current WOS < 6 Weeks

Daily planning review with Procurement.
""")

            st.error("""
### 🔴 Executive Escalation

Current WOS < 4 Weeks

Executive recovery meeting with supplier.
""")

    # ======================================================
    # GOVERNANCE
    # ======================================================

    with st.container(border=True):

        st.subheader("3. Governance & Decision Ownership")

        governance = pd.DataFrame({

            "Decision":[

                "Inventory Health",

                "Stock Balance",

                "Pull Logic",

                "Push Logic",

                "New Buy Approval",

                "Inventory Allocation",

                "Executive Escalation"

            ],

            "Owner":[

                "Supply Planner",

                "Supply Planner",

                "Supply Planner",

                "Supply Planner",

                "Procurement",

                "Supply Planning Manager",

                "Operations Director"

            ]

        })

        st.dataframe(

            governance,

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # STAKEHOLDERS
    # ======================================================

    with st.container(border=True):

        st.subheader("4. Stakeholders")

        stakeholders = pd.DataFrame({

            "Stakeholder":[

                "Supply Planning",

                "Procurement",

                "Contract Manufacturer",

                "Logistics",

                "Sales",

                "Finance",

                "Customer Support"

            ],

            "Responsibility":[

                "Planning Decisions",

                "Supplier & PO Management",

                "Production Recovery",

                "Transport Recovery",

                "Customer Prioritisation",

                "Inventory Investment",

                "Customer Communication"

            ]

        })

        st.dataframe(

            stakeholders,

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # REPORTING
    # ======================================================

    with st.container(border=True):

        st.subheader("5. Reporting Requirements")

        reports = pd.DataFrame({

            "Report":[

                "Executive Decision Report",

                "Inventory Health",

                "Purchase Order Health",

                "Supplier Health",

                "Allocation Review",

                "Planning KPI Review"

            ],

            "Frequency":[

                "Daily",

                "Daily",

                "Daily",

                "Daily",

                "Daily",

                "Weekly"

            ]

        })

        st.dataframe(

            reports,

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # KPI
    # ======================================================

    with st.container(border=True):

        st.subheader("6. Success Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric("Fill Rate", ">98%")

        c2.metric("Target WOS", "12 Weeks")

        c3.metric("Supplier OTD", ">95%")

        c4, c5, c6 = st.columns(3)

        c4.metric("Backlog", "<1,000")

        c5.metric("Planning Cycle", "<30 mins")

        c6.metric("PO Expedites", "<5%")

    # ======================================================
    # REFLECTION
    # ======================================================

    with st.container(border=True):

        st.subheader("7. Long-Term Risk Reduction")

        topics = [

            ("Supplier Diversification",
             "Qualify secondary suppliers to reduce dependency on a single manufacturing source."),

            ("Safety Stock Strategy",
             "Define differentiated safety stock policies based on demand variability and product criticality."),

            ("Lead-Time Management",
             "Monitor supplier lead-time trends and introduce early warning alerts."),

            ("Manufacturing Concentration Risk",
             "Reduce dependency on a single production site where practical."),

            ("Tariffs & Duties",
             "Consider landed cost and tariff exposure within sourcing decisions."),

            ("Inventory Positioning",
             "Position inventory strategically across regions to improve responsiveness."),

            ("Business Continuity Planning",
             "Maintain documented recovery playbooks and perform regular disruption simulations.")

        ]

        for title, text in topics:

            with st.expander(title):

                st.write(text)

    with st.container(border=True):

        st.success(
"""
This prototype demonstrates how manual supply planning decisions
can be converted into a structured decision-support framework.

The planning engine evaluates Inventory Health, Stock Balance,
Pull Logic, Push Logic and Planning Deficit before recommending
a New Buy, ensuring planning decisions remain transparent,
consistent and repeatable.

The solution has also been designed to support multiple products,
suppliers and regions, making it scalable beyond the single-product
business case presented in this exercise.
"""
        )
