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
        "🅰 Part A: Disruption Management",
        "🅱 Part B: Inventory Allocation",
        "🅲 Part C: Replenishment",
        "🅳 Part D: Operating Model",
        "📧 Part E: Quality & Returns",
        "🤖 Part F: AI Reflection Statement"
    ]
)

# ======================================================
# TAB 0: Core Planning Assumptions (The 11-Point Master List)
# ======================================================
with tab0:
    st.header("📝 Core Operational Architecture & Assumptions")
    
    with st.container(border=True):
        st.markdown("""
        To establish a repeatable framework for Nabu Casa, this model operates strictly on your **11 verified operational parameters** to eliminate generic AI assumptions and enforce mathematically sound inventory loops.
        """)

    with st.container(border=True):
        st.subheader("1️⃣ Product Lifecycle Stage")
        st.markdown("The product (**FLAGSHIP123**) is explicitly in the **New** phase of its lifecycle (**New** -> **Sustaining** -> **Declining** -> **Vintage**). Demand is ramping up rapidly; maintaining a healthy stock buffer is critical to prevent missing early market share and growth.")

    with st.container(border=True):
        st.subheader("2️⃣ Supplier Identification")
        st.markdown("The primary contract manufacturer (OEM) is explicitly identified as **CMHK**.")

    with st.container(border=True):
        st.subheader("3️⃣ Regional Distribution Centre Code")
        st.markdown("The centralized holding and gateway hub is designated as location code **HK111**, situated directly in Hong Kong.")

    with st.container(border=True):
        st.subheader("4️⃣ PO Order Date")
        st.markdown("The original 10,000-unit order was placed eight weeks ago. The supplier notified us of the component shortage just two days before it was scheduled to ship.")

    with st.container(border=True):
        st.subheader("5️⃣ Lead Time Buffer")
        st.markdown("The 8-week lead time covers factory production only. For true end-to-end planning, we add a 2-week ocean freight and customs buffer to know exactly when stock physically lands.")

    with st.container(border=True):
        st.subheader("6️⃣ Open Regional Demand")
        st.markdown("The regional demand numbers represent hard, confirmed customer and distributor backlogs currently waiting to be filled, not speculative forecasts.")

    with st.container(border=True):
        st.subheader("7️⃣ On-Hand Isolation Rule")
        st.markdown("**Core Assumption:** The 8,000 units currently sitting **On Hand** are already fully allocated to past regional orders. They cannot be re-consumed to fulfill the new incoming 9,500-unit backlog.")

    with st.container(border=True):
        st.subheader("8️⃣ Specific Shipment Dates")
        st.markdown("The order was originally placed on April 24, 2026, and was supposed to land on July 3, 2026. Due to the disruption, 4,000 units arrive on July 3, 2026 (In Transit), and the remaining 6,000 units land three weeks later on July 24, 2026 (Open PO Balance).")

    with st.container(border=True):
        st.subheader("9️⃣ Factory Order Multiples & MOQ Logic")
        st.markdown("""
        Procurement orders must strictly conform to the **5,000-unit factory MOQ blocks**. The factory only sells in full batch increments (5,000, 10,000, 15,000, etc.). 
        
        Because a 10,000-unit reorder would fail to cover the raw network deficit of **11,576 units** (leaving a critical 1,576-unit supply gap), standard supply chain logic dictates rounding up to the next full production multiple:
        
        $$\\text{Recommended PO} = \\text{ceil}\\left(\\frac{11,576 \\text{ Deficit}}{5,000 \\text{ MOQ}}\\right) \\times 5,000 = 3 \\times 5,000 = 15,000 \\text{ Units}$$
        """)

    with st.container(border=True):
        st.subheader("🔟 DC Network Architecture")
        st.markdown("We assume a multi-node regional 3PL network (US Hub, EU Hub, APAC Hub) managed from a central planning gate in Hong Kong. Stock is sorted at the gate and sent straight to the regions to minimize transit times and costs.")

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
# TAB 2: Part A: Supply Disruption Management
# ======================================================
with tab2:
    st.header("🅰 Part A: Supply Disruption Management")
    
    with st.container(border=True):
        st.subheader("⏱ The First 48 Hours: Immediate Priorities")
        st.markdown("""
        * **Isolate the Constraint:** Contact CMHK to lock down the exact split-shipment timeline (4,000 immediate vs. 6,000 delayed by 3 weeks) to ensure we are planning against hard facts, not moving dates.
        * **Execute Net Asset Accounting:** Triage the total network gap. Run the math to know exactly where we stand: Inventory Position = On Hand + Open PO - Backlog. Apply the On-Hand Isolation Rule, knowing that the 8,000 units on hand are already legally committed to past windows, leaving only the incoming 4,000 units to handle the new 9,500-unit backlog.
        * **Protect the Commercial Gateway:** Isolate high-exposure demand pockets, specifically safeguarding the US promotional launch next week by routing the immediate 4,000-unit pool there first.
        """)

    with st.container(border=True):
        st.subheader("📊 Information to Gather Before Deciding")
        st.markdown("""
        * **True Network Deficit:** The exact regional breakdown of the 9,500 units of confirmed open demand (distributor backlogs, not speculative forecasts).
        * **Supplier Floor Status:** The root cause of the sub-tier raw material bottleneck at CMHK to verify if the 3-week delay is actually stable.
        * **Logistics Lead Times:** Standard ocean transit legs (2 weeks) vs. premium air freight availability to see how fast we can land the expedited stock.
        * **Cross-Product Portfolio Visibility:** A view of all open factory POs (including other sustaining lines) to see if we can buy capacity slots.
        """)

    with st.container(border=True):
        st.subheader("🏭 Supplier Collaboration & Mitigation Strategy")
        st.markdown("""
        * **Portfolio Capacity Swapping (Push Logic):** Look at the broader factory floor. If CMHK is building a stable, sustaining SKU for us that has a healthy safety buffer, we request to Push that sustaining PO out by 4 weeks. This immediately frees up their factory floor capacity to focus entirely on building our high-priority FLAGSHIP123 parts.
        * **Logistics Expediting (Pull Logic):** For the remaining 6,000-unit delayed balance, we do not wait for a slow ocean leg. We pull it forward by switching it to a priority air corridor directly out of the Hong Kong gateway (HK111).
        """)

    with st.container(border=True):
        st.subheader("👥 Internal Stakeholders & Alignment")
        st.markdown("""
        * **Procurement:** To negotiate the capacity swap on the factory floor and officially adjust the PO delivery windows.
        * **Sales and Account Managers:** To review the regional priority cascade (US -> EU -> APAC) and manage strategic customer exceptions.
        * **Finance:** To secure rapid sign-off for the premium air freight override costs and prepare for the upcoming step-batch MOQ reorder.
        """)

    with st.container(border=True):
        st.subheader("📢 Distributor Communication & Expectation Management")
        st.markdown("""
        * **Be Proactive, Not Reactive:** Do not let distributors find out about a stockout when their trucks arrive empty. You notify them within the 48-hour window.
        * **Provide Solutions, Not Just Problems:** When communicating with the EU and APAC hubs (who are getting zero units from the first 4,000 arrival), you present a firm, data-verified recovery roadmap showing the exact air freight landing dates for the 6,000-unit balance.
        """)

    with st.container(border=True):
        st.subheader("⚡ Key Risks to Assess & Monitor")
        st.markdown("""
        * **Launch Failure Risk:** The immediate threat of empty retail shelves during the critical US promotional launch next week.
        * **Sub-Tier Supplier Slippage:** The risk that CMHK's component supplier takes longer than 3 weeks to recover, turning a minor delay into a catastrophic stockout.
        * **Landed Cost Variance:** The financial impact of unbudgeted premium air freight eroding product margins.
        """)

    with st.container(border=True):
        st.subheader("🧠 Future-Proofing Reflection (The Apple Paradigm)")
        st.markdown("""
        To ensure Nabu Casa is never caught off guard again, I would introduce a formal Component-Level Governance Framework, a strategy I previously implemented at Apple during major operational rollouts:
        
        * **Automated WOS Governance Triggers:** Move away from manual spreadsheet tracking. Introduce a system that dynamically monitors Weeks of Supply (WOS) and flags risks early:
            * 🟢 Normal (WOS >= 12): Routine tracking.
            * 🟡 Planner Review (WOS < 8): Trigger localized 3PL rebalancing reviews.
            * 🟠 Management Escalation (WOS < 6): Daily cross-functional logistics syncs.
            * 🔴 Executive Isolation (WOS < 4): C-Suite intervention call with supplier leadership.
        * **Sub-Tier Supplier Mapping:** Mandate that CMHK provides quarterly visibility into their critical raw material sub-tiers. We must know who makes their chips and where the bottlenecks live before the factory floor stops.
        * **Step-Batch MOQ Automation:** Build factory production constraints directly into our planning software. By locking in the 5,000-unit factory MOQ block and using a mathematical ceiling loop, the system will automatically round procurement proposals up to clean production batches. This ensures we always order enough to cover our true operational deficits without leaving exposed gaps.
        """)

# ======================================================
# TAB 3: Part B: Inventory Allocation
# ======================================================
with tab3:
    st.header("🅱 Part B: Inventory Allocation Engine")
    
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
        st.subheader("📊 Information to Gather Before Allocating")
        st.markdown("""
        * **True Channel Availability:** Verify that the incoming 4,000 units are physically clear of Hong Kong customs (HK111) and ready for immediate shipping.
        * **Promotional Timelines and Penalties:** Review the exact calendar window, marketing spend, and retailer service level agreements (SLAs) for the US promotional launch next week.
        * **Backlog Multipliers:** Isolate specific order dates within the 9,500 units of open demand to see which distributors have been waiting the longest.
        """)

    with st.container(border=True):
        st.subheader("⚙ Allocation Methodology and Trade-offs")
        st.markdown("""
        * **US Hub Prioritization (Priority 1):** Routes 100% of the arriving 4,000-unit physical pool straight to the United States to insulate the high-exposure product promotional launch next week, leaving a minor unfulfilled deficit of 500 units.
        * **Geographic Freight Intervention:** Premium air freight pathways are deployed to bypass standard 2-week ocean legs, ensuring physical transit lands at the US distributor hub within 48 to 72 hours.
        * **EU and APAC Hub Deferral (Priority 2 and 3):** Programmatically allocated zero units from this intake window due to physical capacity constraints. Confirmed backlogs are stabilized and held until the 6,000-unit factory balance clears on July 24, 2026.
        * **The Key Trade-off:** We intentionally sacrifice immediate short-term availability in stable (EU) and growth (APAC) channels to completely prevent a public product launch failure in the primary US market.
        """)

    with st.container(border=True):
        st.subheader("📢 Stakeholder Communication and Balance")
        st.markdown("""
        * **Short-Term vs. Long-Term Balance:** The US launch protects immediate brand equity and momentum. The EU and APAC channels are stabilized by bridging their cash flows, providing verified commitments that their unfulfilled demand is locked into the incoming 6,000-unit factory balance.
        * **Managing Stakeholder Expectations:** Communicate proactively. We do not hide the deficit. I provide the EU and APAC partners with a firm logistics roadmap showing the exact air freight transit booking dates for their inventory to secure account trust.
        """)

    with st.container(border=True):
        st.subheader("🎯 Strategy Risks and Success Monitoring")
        st.markdown("""
        * **Proposed Strategy Risks:** High regional inventory concentration in the US, potential local retail customer dissatisfaction in the EU, and momentum loss in a growing APAC layer.
        * **Success Metrics:** Track the US promotional fill rate (target over 98%), audit total transit times through the expedited air corridor, and monitor distributor retention rates across deferred regions.
        """)

# ======================================================
# TAB 4: Part C: Inventory Planning & Replenishment (UPDATED)
# ======================================================
with tab4:
    st.header("🅲 Part C: Replenishment & Planning Deficit")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Calculated Planning Deficit", f'{shortage["Planning Deficit"]:,} Units')
    c2.metric("CMHK Production Batch MOQ", f'{product["moq"]:,} Units')
    c3.metric("Recommended Procurement Order", f'{shortage["Recommended PO"]:,} Units')

    with st.container(border=True):
        st.subheader("🛒 Procurement Decision: YES")
        st.markdown("""
        * **Action Plan:** Place a new Purchase Order immediately on July 4, 2026. 
        * **Order Quantity:** 15,000 Units (3 full factory MOQ batches of 5,000 units).
        * **Timing Logic:** With an 8-week production lead time and a 2-week ocean freight buffer (10 weeks total), this inventory will physically land in week 10, perfectly hitting the warehouse floor at the beginning of Month 3 to cover your peak monthly forecast of 9,000 units.
        """)

    with st.container(border=True):
        st.subheader("🧮 Operational Assumptions and Calculation Baseline")
        st.markdown("""
        * **Given Demand Forecast Breakdown:**
            * Month 1: **6,000 units**
            * Month 2: **7,500 units**
            * Month 3 (Peak Demand Spike): **9,000 units**
            * Month 4: **6,500 units**
        * **Weekly Demand Run-Rate:** 1,673 units per week (7,250 average monthly forecast divided by 4.33 weeks).
        * **Safety Target:** A strict 12-week safety buffer (20,076 units required).
        * **True Inventory Position:** 8,500 units (Calculated using your exact formula: On Hand (8,000) + Open PO (10,000) - Backlog (9,500)).
        * **Factory MOQ Ceiling Rounding:** Raw Deficit = 20,076 (Target) - 8,500 (Position) = 11,576 units. Dividing 11,576 by the 5,000-unit MOQ yields 2.315 batches. We apply a mathematical ceiling function to round up to 3 clean production batches (15,000 units). Ordering only 10,000 units would leave a critical 1,576-unit exposure gap below safety targets.
        """)

    with st.container(border=True):
        st.subheader("💼 Justifying Decisions to Finance & Working Capital Strategy")
        st.markdown("""
        * **Avoided Revenue Loss:** Prove that ordering below the MOQ threshold ensures a total network stock-out during the Month 3 demand spike (9,000 units), costing far more in gross margin than short-term holding costs.
        * **Portfolio Balance:** Highlight that this item is in its New lifecycle stage, where early market share acquisition vastly outweighs localized inventory carrying costs.
        * **Working Capital Mitigation (Phased Releases):** To directly address cash-flow and excess inventory concerns, we legally commit to the 15,000-unit PO to satisfy the manufacturer's MOQ rules but negotiate a **staggered shipment release schedule (3 monthly drops of 5,000 units)**. This aligns physical working capital outflows directly with our incoming regional revenue streams and prevents warehouse overcrowding.
        """)

    # ======================================================
    # EXPANDED PULL LOGIC DISPLAY
    # ======================================================
    with st.container(border=True):
        st.subheader("📥 Step 2: Pull Logic (Expedite Pipeline)")
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
    # EXPANDED PUSH LOGIC DISPLAY
    # ======================================================
    with st.container(border=True):
        st.subheader("📤 Step 3: Push Logic (Capacity De-escalation)")
        
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
# TAB 5: Part D: Operating Model & Governance (UPDATED)
# ======================================================
with tab5:
    st.header("🅳 Part D: Operating Model & Governance")
    
    with st.container(border=True):
        st.subheader("📋 Standard Operating Procedure (SOP) & Production Cadence")
        st.markdown("""
        * **Weekly Run-Rate Track (Routine Track):** Automated tracking loops execute every single week to evaluate trailing consumption, update live WOS positions, and handle steady-state replenishment rebalancing requests.
        * **3-Week Priority Lock (Structural Plan Rework):** To accommodate complex factory build plan reworks at CMHK, structural adjustments (such as a 15,000-unit stabilization buy, portfolio capacity push/pull swaps, or logistics mode changes) execute on a strict **3-week optimized cadence** to give the OEM sufficient manufacturing runway to re-allocate labor and reschedule lines.
        """)
        st.markdown("---")
        steps = [
            ("Step 1: Disruption Alert Trigger", "Automated system flags production or sub-tier component constraint at CMHK."),
            ("Step 2: Split-Shipment Validation", "Procurement confirms the exact split arrival windows (4,000 units vs. 6,000 units) and revised dates."),
            ("Step 3: Net Asset Processing", "Supply Planning applies the asset formula to compute true network deficit levels against the 12-week safety target."),
            ("Step 4: Priority Allocation Execution", "The allocation engine triggers the priority commercial cascade (US -> EU -> APAC) to protect high-exposure promotional timelines."),
            ("Step 5: Governance Approval Loop", "The recommended reorder proposal is routed through predefined authorization pipelines for prompt execution.")
        ]
        for title, desc in steps:
            st.markdown(f"**{title}**: {desc}")

    with st.container(border=True):
        st.subheader("🚦 Weeks of Supply (WOS) Governance Thresholds")
        st.markdown("""
        * **🟢 Normal Status (WOS >= 12):** Standard automated tracking; processed by the Supply Planner.
        * **🟡 Planner Review (WOS < 8):** Flagged constraint window; local 3PL rebalancing activated by the Supply Planner.
        * **🟠 Management Escalation (WOS < 6):** Daily tracking cycles and cross-functional logistics synchronization led by the Supply Planning Manager.
        * **🔴 Executive Intervention (WOS < 4):** Emergency operational meeting with CMHK leadership driven directly by the Operations Director.
        """)

    with st.container(border=True):
        st.subheader("Strategic Cross-Functional Governance Map")
        gov_data = {
            "Planning Process Flow": ["Net Asset Calculation", "Regional Stock Rebalancing", "Expedite / Pull Optimization", "MOQ Procurement Sign-off", "Priority Allocation Override", "Executive Supplier Escalation"],
            "Functional Owner": ["Supply Planner", "Supply Planner", "Procurement Specialist", "Procurement Director", "Supply Planning Manager", "Operations Director"]
        }
        st.dataframe(pd.DataFrame(gov_data), use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.subheader("🌍 Long-Term Risk Reduction (The Broad View)")
        st.markdown("""
        * **Supplier Diversification:** Begin a dual-sourcing strategy by qualifying a secondary manufacturing partner outside of Hong Kong to remove single-source dependencies.
        * **Safety Stock Calibration:** Establish a differentiated safety stock architecture, holding higher component-level safety buffers for new products while keeping mature products leaner.
        * **Inventory Positioning:** Move away from pure central holding. Move standard inventory nodes closer to regional 3PL hubs (US/EU) to drastically compress operational lead times and absorb unexpected demand spikes.
        """)

# ======================================================
# TAB 6: Part E: Quality & Returns Management
# ======================================================
with tab6:
    st.header("📧 Part E: Quality & Returns Management")
    
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

    with st.container(border=True):
        st.subheader("🏭 Root Cause Investigation & Supplier Integration")
        st.markdown("""
        * **Audit the Floor:** Dispatch local engineering resource partners directly to the CMHK manufacturing floor to audit assembly lines and component sub-tiers.
        * **Corrective and Preventive Actions (CAPA):** Mandate automated optical inspection loops on the factory floor, enforce strict component screening gates at intake, and implement isolated pilot-run verification cycles on all subsequent production lots.
        """)

# ======================================================
# TAB 7: Part F: AI Reflection Statement
# ======================================================
with tab7:
    st.header("🤖 Part F: Statement of AI Collaboration & Professional Judgment")
    
    with st.container(border=True):
        st.markdown("""
        Throughout this exercise, I used AI as a collaborative tool to accelerate development and improve the quality of my submission. I used it to research supply chain concepts, challenge my assumptions, refine my written responses, improve the structure and wording of the PDF presentation, and assist with the design and development of the interactive Streamlit application. AI also helped me prototype parts of the user interface, review the planning workflow, and improve the overall presentation of the solution.
        
        I accepted AI suggestions that improved the clarity, structure and usability of the application and supporting documentation. I also rejected or modified recommendations that did not align with the business case, practical supply planning principles or my own professional judgement. Every recommendation included in the final submission was reviewed, validated and adapted before being incorporated.
        
        I relied entirely on my own judgement and professional experience to define the planning assumptions, develop the planning methodology, determine the inventory allocation strategy, justify the replenishment recommendation, design the planning hierarchy, and create the Standard Operating Procedure (SOP), governance model and KPI framework. These decisions were based on my experience in Supply Chain and Service Operations: incorporating the exact structural concepts I previously implemented at Apple when deploying their new operational processes: ensuring that the final solution reflected practical operational decision-making rather than generic AI-generated output.
        
        In a role like this, I would use AI as a decision-support tool rather than a decision-maker. I believe AI can significantly improve productivity by analysing operational data, identifying supply risks, generating planning scenarios, automating routine reporting and improving documentation. However, final planning decisions should always remain the responsibility of the planner, combining AI-generated insights with business context, commercial priorities, organisational objectives and professional judgement.
        """)