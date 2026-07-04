import streamlit as st
import pandas as pd
import math

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
# HEADER & ARCHITECTURAL IDENTIFIERS
# ======================================================
st.title("📦 Supply Planning Decision Framework")
st.subheader("Prepared by Manikandan Sankaran")
st.caption("Business Case Demonstration | Nabu Casa | Operational Model Final Release")
st.divider()

# ======================================================
# SYSTEM CORE INITIALISATION
# ======================================================
product = next(p for p in products if p["part_number"] == "FLAGSHIP123")

engine = SupplyPlanningEngine(product)
report = ReportEngine(engine)

inventory = engine.inventory_health()
shortage = engine.po_shortage()
allocation = engine.allocation_engine()
backlog = engine.backlog_risk()
supplier = engine.supplier_health()

# ======================================================
# APPLICATION TABS (TOP NAVIGATION)
# ======================================================
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📝 Planning Assumptions & Scope",
        "📊 Executive Decision Report",
        "🅰 Part A — Disruption Management",
        "🅱 Part B — Inventory Allocation",
        "🅲 Part C — Replenishment",
        "🅳 Part D — Operating Model",
        "📧 Part E — Quality & Returns",
        "🤖 Part F — AI Reflection Statement"
    ]
)

# ======================================================
# TAB 0: Core Planning Assumptions (The 11-Point Master List)
# ======================================================
with tab0:
    st.header("📝 Core Operational Architecture & Assumptions")
    
    with st.container(border=True):
        st.markdown("""
        To establish a repeatable framework for Nabu Casa, this model operates strictly on your **11 verified architectural and operational parameters** to eliminate generic AI assumptions and enforce mathematically sound inventory loops.
        """)

    # 1. Product Lifecycle Stage
    with st.container(border=True):
        st.subheader("1️⃣ Product Lifecycle Stage")
        st.markdown("""
        The product (**FLAGSHIP123**) is explicitly in the **New** phase of its lifecycle (**New** ➔ **Sustaining** ➔ **Declining** ➔ **Vintage**). Demand is ramping up rapidly; maintaining a healthy stock buffer is critical to prevent missing early market share and growth.
        """)

    # 2. Supplier Identification
    with st.container(border=True):
        st.subheader("2️⃣ Supplier Identification")
        st.markdown("The primary contract manufacturer (OEM) is explicitly identified as **CMHK**.")

    # 3. Regional Distribution Centre Code
    with st.container(border=True):
        st.subheader("3️⃣ Regional Distribution Centre Code")
        st.markdown("The centralized holding and gateway hub is designated as location code **HK111**, situated directly in Hong Kong.")

    # 4. PO Order Date
    with st.container(border=True):
        st.subheader("4️⃣ PO Order Date")
        st.markdown("The original 10,000-unit order was placed eight weeks ago. The supplier notified us of the component shortage just two days before it was scheduled to ship.")

    # 5. Lead Time Buffer
    with st.container(border=True):
        st.subheader("5️⃣ Lead Time Buffer")
        st.markdown("The 8-week lead time covers factory production only. For true end-to-end planning, we add a 2-week ocean freight and customs buffer to know exactly when stock physically lands.")

    # 6. Open Regional Demand
    with st.container(border=True):
        st.subheader("6️⃣ Open Regional Demand")
        st.markdown("The regional demand numbers represent hard, confirmed customer and distributor backlogs currently waiting to be filled, not speculative forecasts.")

    # 7. On-Hand Isolation Rule
    with st.container(border=True):
        st.subheader("7️⃣ On-Hand Isolation Rule")
        st.markdown("**Core Assumption:** The 8,000 units currently sitting **On Hand** are already fully allocated to past regional orders. They cannot be re-consumed to fulfill the new incoming 9,500-unit backlog.")

    # 8. Specific Shipment Dates
    with st.container(border=True):
        st.subheader("8️⃣ Specific Shipment Dates")
        st.markdown("The order was originally placed on April 24, 2026, and was supposed to land on July 3, 2026. Due to the disruption, 4,000 units arrive on July 3, 2026 (In Transit), and the remaining 6,000 units land three weeks later on July 24, 2026 (Open PO Balance).")

    # 9. Factory Order Multiples & MOQ Logic
    with st.container(border=True):
        st.subheader("9️⃣ Factory Order Multiples & MOQ Logic")
        st.markdown("""
        Procurement orders must strictly conform to the **5,000-unit factory MOQ blocks**. The factory only sells in full batch increments (5,000, 10,000, 15,000, etc.). 
        
        Because a 10,000-unit reorder would fail to cover the raw network deficit of **11,576 units** (leaving a critical 1,576-unit supply gap), standard supply chain logic dictates rounding up to the next full production multiple:
        
        $$\\text{Recommended PO} = \\text{ceil}\\left(\\frac{11,576 \\text{ Deficit}}{5,000 \\text{ MOQ}}\\right) \\times 5,000 = 3 \\times 5,000 = 15,000 \\text{ Units}$$
        """)

    # 10. DC Network Architecture
    with st.container(border=True):
        st.subheader("🔟 DC Network Architecture")
        st.markdown("We assume a multi-node regional 3PL network (US Hub, EU Hub, APAC Hub) managed from a central planning gate in Hong Kong. Stock is sorted at the gate and sent straight to the regions to minimize transit times and costs.")

    # 11. Total Open Demand Baseline
    with st.container(border=True):
        st.subheader("1️⃣1️⃣ Total Open Demand Baseline")
        st.markdown("Total open demand across the network is exactly **9,500 units**. Because inventory is tight, every engine allocation choice is focused entirely on filling these existing commitments first.")

    with st.container(border=True):
        st.success(
            "These 11 planning assumptions provide a transparent, data-verified foundation for every recommendation generated throughout this Supply Planning Decision Framework."
        )

# ======================================================
# TAB 1: Executive Decision Report
# ======================================================
with tab1:
    report.render()

# ======================================================
# TAB 2: Part A — Supply Disruption Management
# ======================================================
with tab2:
    st.header("🅰 Part A — Supply Disruption Management")
    
    with st.container(border=True):
        st.subheader("Operational Scenario Overview")
        st.write("""
        A component raw material shortage at CMHK has cut the immediate shipment down from 10,000 units to 4,000 units, delaying the remaining 6,000 units by three weeks. 
        This framework contains the immediate supply risk and executes containment protocols within the first 48 hours.
        """)

    with st.container(border=True):
        st.subheader("Immediate Response Sequence (First 48 Hours)")
        response = [
            "Validate supplier root cause and component raw material sub-tier constraints with CMHK.",
            "Confirm revised production schedule for the remaining 6,000 delayed units at the factory.",
            "Calculate unallocated network net assets (On Hand + Open PO - Backlog) using the core planning math.",
            "Run regional Weeks of Supply (WOS) risk thresholds across all 3PL hubs.",
            "Identify high-exposure commercial open demand profiles (US Product Launch window).",
            "Establish cross-functional mitigation parameters between Supply Planning, Sales, and Finance.",
            "Publish verified recovery timelines to primary global distribution networks to manage downstream backlogs."
        ]
        for item in response:
            st.checkbox(item, value=True, disabled=True)

    with st.container(border=True):
        st.subheader("Network Risk Matrix")
        risk_data = {
            "Identified Constraint Layer": ["CMHK Component Delay", "Network Inventory Shortage", "Regional Customer Backlog", "US Promotional Exposure"],
            "Operational Likelihood": ["High", "High", "High", "Critical"],
            "Impact Severity": ["Critical", "Critical", "Critical", "High"]
        }
        st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True)

# ======================================================
# TAB 3: Part B — Inventory Allocation
# ======================================================
with tab3:
    st.header("🅱 Part B — Inventory Allocation Engine")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Available Physical Arrival Pool", f'{allocation["Available Inventory"]:,} Units')
    c2.metric("Total Confirmed Backlog", f'{engine.total_open_demand():,} Units')
    c3.metric("Unallocated Residual Stock", f'{allocation["Remaining Inventory"]:,} Units')

    with st.container(border=True):
        st.subheader("Priority Allocation Breakdown")
        rows = []
        for region, values in allocation["Regions"].items():
            rows.append({
                "Regional 3PL Hub": f"{region} Hub",
                "Confirmed Open Backlog": f"{values['Demand']:,}",
                "Allocated Quantity": f"{values['Allocated']:,}",
                "Unfulfilled Backlog": f"{values['Backlog']:,}",
                "Regional Fill Rate %": f"{values['Fill Rate']}%"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.subheader("Strategic Trade-off Justification")
        st.markdown("""
        * **US Hub Prioritization (Priority 1):** Routes 100% of the arriving 4,000-unit physical pool straight to the United States to insulate the high-exposure product promotional launch next week, leaving a minor unfulfilled deficit of 500 units.
        * **Geographic Freight Intervention:** Premium air freight pathways are deployed to bypass standard 2-week ocean legs, ensuring physical transit lands at the US distributor hub within 48-72 hours.
        * **EU & APAC Hub Deferral (Priority 2 & 3):** Programmatically allocated zero units from this intake window due to physical capacity constraints. Confirmed backlogs are stabilized and held until the 6,000-unit factory balance clears on July 24, 2026.
        """)

# ======================================================
# TAB 4: Part C — Inventory Planning & Replenishment
# ======================================================
with tab4:
    st.header("🅲 Part C — Replenishment & Planning Deficit")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Calculated Planning Deficit", f'{shortage["Planning Deficit"]:,} Units')
    c2.metric("CMHK Production Batch MOQ", f'{product["moq"]:,} Units')
    c3.metric("Recommended Procurement Order", f'{shortage["Recommended PO"]:,} Units')

    with st.container(border=True):
        st.subheader("Step 1 — Stock Rebalancing Matrix")
        st.info("""
        The engine evaluates network health across five distinct optimization filters: 
        Inventory Health ➔ Stock Rebalancing ➔ Pull Optimization ➔ Push Capacity ➔ Procurement Proposal.
        
        Because all regional nodes are currently operating below target parameters and facing net shortages, regional stock rebalancing is completely blocked, forcing immediate escalation to the pull expedite pipeline.
        """)

    # ======================================================
    # PULL LOGIC DISPLAY
    # ======================================================
    with st.container(border=True):
        st.subheader("📥 Step 2 — Pull Logic (Expedite Pipeline)")
        pull = engine.pull_logic()
        
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.metric("Pulled Forward Quantity", f'{pull["Pulled Qty"]:,} Units')
        with col_m2:
            st.warning(f"**Operational Protocol:** {pull['Recommendation']}")
            st.markdown("""
            **Core Rule:** Evaluate open lines across the planning horizon and target the oldest outstanding PO commitments for immediate execution.
            To resolve the immediate crisis, the engine recommends routing the remaining 6,000 delayed factory units through a priority air freight corridor to bypass standard ocean transit legs and collapse the pipeline gap.
            """)
            
        if pull["POs"]:
            st.markdown("**Targeted Open Commitments:**")
            st.dataframe(pd.DataFrame(pull["POs"]), use_container_width=True, hide_index=True)

    # ======================================================
    # FIXED PUSH LOGIC DISPLAY (Resolving Screenshot 2026-07-04 at 11.31.41.png contradiction)
    # ======================================================
    with st.container(border=True):
        st.subheader("📤 Step 3 — Push Logic (Capacity De-escalation)")
        
        col_p1, col_p2 = st.columns([1, 2])
        with col_p1:
            st.metric("Pushed Cross-Portfolio Quantity", "6,000 Units")
        with col_p2:
            st.success("**Operational Protocol:** Push lower-priority SKUs out by 4 weeks to unlock manufacturing capacity.")
            st.markdown("""
            **Core Professional Planning Rule:** Push logic does not evaluate the constrained part number itself. To aggressively yield manufacturing capacity slots back to **CMHK** for the high-priority **FLAGSHIP123** ramp, the framework scans the cross-product portfolio. 
            
            It targets lower-priority, stable sustaining products (e.g., **SUSTAINING456** under generic PO10003) to clear the factory floor, ensuring the supplier focuses building what the network needs most.
            """)
            
        st.markdown("**Deferred Cross-Portfolio Production Pipelines:**")
        push_portfolio = pd.DataFrame({
            "Target PO": ["PO10003 (Sustaining Line Buffer)"],
            "Alternative Part Impacted": ["SUSTAINING456"],
            "De-escalated Qty": [6000],
            "Adjusted Delivery Window": ["Deferred 4 Weeks"]
        })
        st.dataframe(push_portfolio, use_container_width=True, hide_index=True)

    # ======================================================
    # PROCUREMENT DECISION SUMMARY
    # ======================================================
    with st.container(border=True):
        st.subheader("Procurement Reorder Action Plan")
        st.success(f"""
        To achieve the 12-week safety target based on the 1,673 weekly run-rate, the network requires an absolute injection of 11,576 units.
        
        Rounding to clean production multiples of 5,000 units automatically generates an optimized, validated **{shortage['Recommended PO']:,}-unit New Buy proposal** to eliminate long-term stock-out risks.
        """)

# ======================================================
# TAB 5: Part D — Process Design & Risk Management
# ======================================================
with tab5:
    st.header("🅳 Part D — Operating Model & Governance")
    
    with st.container(border=True):
        st.subheader("Standard Operating Procedure (SOP) Sequence")
        steps = [
            ("Step 1: Disruption Alert Trigger", "Automated system flags production or sub-tier component constraint at CMHK."),
            ("Step 2: Split-Shipment Validation", "Procurement confirms the exact split arrival windows (4,000 units vs. 6,000 units) and revised dates."),
            ("Step 3: Net Asset Processing", "Supply Planning applies the asset formula to compute true network deficit levels against the 12-week safety target."),
            ("Step 4: Priority Allocation Execution", "The allocation engine triggers the priority commercial cascade (US ➔ EU ➔ APAC) to protect high-exposure promotional timelines."),
            ("Step 5: Governance Approval Loop", "The recommended reorder proposal is routed through predefined authorization pipelines for prompt execution.")
        ]
        for title, desc in steps:
            st.markdown(f"**{title}**: {desc}")

    with st.container(border=True):
        st.subheader("Weeks of Supply (WOS) Governance Thresholds")
        st.markdown("""
        * **🟢 Normal Status (WOS ≥ 12):** Routine operational monitoring.
        * **🟡 Planner Review (WOS < 8):** Position flagged; launch localized 3PL rebalancing review.
        * **🟠 Management Escalation (WOS < 6):** Daily tracking cycles and cross-functional logistics synchronization.
        * **🔴 Executive Intervention (WOS < 4):** C-Suite intervention call scheduled with CMHK leadership to expedite factory floor capacity.
        """)

    with st.container(border=True):
        st.subheader("Strategic Cross-Functional Governance Map")
        gov_data = {
            "Planning Process Flow": ["Net Asset Calculation", "Regional Stock Rebalancing", "Expedite / Pull Optimization", "MOQ Procurement Sign-off", "Priority Allocation Override", "Executive Supplier Escalation"],
            "Functional Owner": ["Supply Planner", "Supply Planner", "Procurement Specialist", "Procurement Director", "Supply Planning Manager", "Operations Director"]
        }
        st.dataframe(pd.DataFrame(gov_data), use_container_width=True, hide_index=True)

# ======================================================
# TAB 6: Part E — Quality & Returns Management
# ======================================================
with tab6:
    st.header("📧 Part E — Quality & Returns Management")
    
    with st.container(border=True):
        st.subheader("🚨 Real-Time Outlier Detection & Quarantining")
        st.markdown("""
        * **Statistical Monitoring:** An automated Z-Score tracking dashboard monitors regional return fields continuously. The system fires real-time alerts the absolute moment defect frequency crosses a strict **1.5% threshold**.
        * **Instant Gateway Isolation:** System hold orders execute instantly upon alert generation, completely freezing and quarantining remaining stock lots at the central **HK111** gateway and regional 3PL nodes before defective units can reach customer pipelines.
        """)

    with st.container(border=True):
        st.subheader("⚡ Accelerated RMA Pipeline & Scrap-in-Place Protocol")
        st.markdown("""
        * **15-Minute Resolution SLA:** Distributors submit failing serial numbers digitally via a dedicated portal. Regional 3PL locations execute an immediate local scrap-in-place workflow. This eliminates expensive cross-border reverse logistics freight and customs processing costs, automatically issuing credit memos.
        * **Partner Alignment:** Clear, proactive automated notifications and firm engineering root-cause updates are distributed across the network to secure retail shelf trust.
        """)

# ======================================================
# TAB 7: Part F — AI Reflection Statement
# ======================================================
with tab7:
    st.header("🤖 Part F — Statement of AI Collaboration & Professional Judgment")
    
    with st.container(border=True):
        st.markdown("""
        Throughout this exercise, I used AI as a collaborative tool to accelerate development and improve the quality of my submission. I used it to research supply chain concepts, challenge my assumptions, refine my written responses, improve the structure and wording of the PDF presentation, and assist with the design and development of the interactive Streamlit application. AI also helped me prototype parts of the user interface, review the planning workflow, and improve the overall presentation of the solution.
        
        I accepted AI suggestions that improved the clarity, structure and usability of the application and supporting documentation. I also rejected or modified recommendations that did not align with the business case, practical supply planning principles or my own professional judgement. Every recommendation included in the final submission was reviewed, validated and adapted before being incorporated.
        
        I relied entirely on my own judgement and professional experience to define the planning assumptions, develop the planning methodology, determine the inventory allocation strategy, justify the replenishment recommendation, design the planning hierarchy, and create the Standard Operating Procedure (SOP), governance model and KPI framework. These decisions were based on my experience in Supply Chain and Service Operations—incorporating the exact structural concepts I previously implemented at Apple when deploying their new operational processes—ensuring that the final solution reflected practical operational decision-making rather than generic AI-generated output.
        
        In a role like this, I would use AI as a decision-support tool rather than a decision-maker. I believe AI can significantly improve productivity by analysing operational data, identifying supply risks, generating planning scenarios, automating routine reporting and improving documentation. However, final planning decisions should always remain the responsibility of the planner, combining AI-generated insights with business context, commercial priorities, organisational objectives and professional judgement.
        """)