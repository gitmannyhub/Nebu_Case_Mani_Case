import streamlit as st
import pandas as pd


class ReportEngine:

    def __init__(self, engine):

        self.engine = engine

    # =========================================================
    # MAIN REPORT
    # =========================================================

    def render(self):

        self.executive_summary()

        self.inventory_health()

        self.purchase_order_health()

        self.stock_balance()

    # =========================================================
    # EXECUTIVE SUMMARY
    # =========================================================

    def executive_summary(self):

        inv = self.engine.inventory_health()

        shortage = self.engine.po_shortage()

        supplier = self.engine.supplier_health()

        backlog = self.engine.backlog_risk()

        st.header("📊 Executive Decision Report")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "Current WOS",

            f"{inv['Current WOS']} Weeks"

        )

        c2.metric(

            "Planning Deficit",

            f"{inv['Planning Deficit']:,} Units"

        )

        c3.metric(

            "Recommended New Buy",

            f"{shortage['Recommended PO']:,} Units"

        )

        c4.metric(

            "Backlog Risk",

            backlog["Risk"]

        )

        st.divider()

        # =====================================================
        # OVERALL STATUS
        # =====================================================

        with st.container(border=True):

            st.error("### 🔴 Critical Planning Status")

            left, right = st.columns(2)

            with left:

                st.write(
                    f"**Inventory Health:** {inv['Status']}"
                )

                st.write(
                    f"**Current WOS:** {inv['Current WOS']}"
                )

            with right:

                st.write(
                    f"**Pipeline WOS:** {inv['Pipeline WOS']}"
                )

                st.write(
                    f"**Disruption WOS:** {inv['Disruption WOS']}"
                )

        # =====================================================
        # DASHBOARD
        # =====================================================

        left, right = st.columns(2)

        with left:

            with st.container(border=True):

                st.info("### 🔵 Planning Position")

                st.metric(

                    "Target Inventory",

                    f'{inv["Target Inventory"]:,}'

                )

                st.metric(

                    "Inventory Position",

                    f'{inv["Inventory Position"]:,}'

                )

                st.metric(

                    "Planning Deficit",

                    f'{inv["Planning Deficit"]:,}'

                )

        with right:

            with st.container(border=True):

                st.warning("### 🟠 Procurement")

                st.metric(

                    "Supplier MOQ",

                    f'{shortage["MOQ"]:,}'

                )

                st.metric(

                    "Recommended New Buy",

                    f'{shortage["Recommended PO"]:,}'

                )

                if shortage["Required"]:

                    st.error(

                        shortage["Reason"]

                    )

                else:

                    st.success(

                        shortage["Reason"]

                    )

        left, right = st.columns(2)

        with left:

            with st.container(border=True):

                st.info("### 🟣 Supplier")

                st.metric(

                    "Supplier",

                    supplier["Supplier"]

                )

                st.metric(

                    "Status",

                    supplier["Status"]

                )

                st.metric(

                    "Lead Time",

                    f'{supplier["Lead Time"]} Weeks'

                )

        with right:

            with st.container(border=True):

                st.error("### 🔴 Backlog")

                st.metric(

                    "Current Backlog",

                    f'{backlog["Current Backlog"]:,}'

                )

                st.metric(

                    "Risk",

                    backlog["Risk"]

                )

                if backlog["Risk"] == "Critical":

                    st.error(backlog["Recommendation"])

                elif backlog["Risk"] == "High":

                    st.warning(backlog["Recommendation"])

                else:

                    st.success(backlog["Recommendation"])

        st.divider()

    # =========================================================
    # INVENTORY HEALTH
    # =========================================================

    def inventory_health(self):

        st.header("📦 Inventory Health")

        inv = self.engine.inventory_health()

        # =====================================================
        # KPI DASHBOARD
        # =====================================================

        with st.container(border=True):

            st.info("### 🔵 Inventory Dashboard")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(

                "Current WOS",

                inv["Current WOS"]

            )

            c2.metric(

                "Pipeline WOS",

                inv["Pipeline WOS"]

            )

            c3.metric(

                "Disruption WOS",

                inv["Disruption WOS"]

            )

            c4.metric(

                "Target WOS",

                inv["Target WOS"]

            )

        # =====================================================
        # INVENTORY POSITION
        # =====================================================

        with st.container(border=True):

            st.subheader("Inventory Position")

            c1, c2, c3 = st.columns(3)

            c1.metric(

                "Target Inventory",

                f'{inv["Target Inventory"]:,} Units'

            )

            c2.metric(

                "Inventory Position",

                f'{inv["Inventory Position"]:,} Units'

            )

            c3.metric(

                "Planning Deficit",

                f'{inv["Planning Deficit"]:,} Units'

            )

        # =====================================================
        # PLANNING STATUS
        # =====================================================

        with st.container(border=True):

            if inv["Status"] == "Healthy":

                st.success(
                    "Inventory is currently operating within the target planning policy."
                )

            elif inv["Status"] == "Warning":

                st.warning(
                    "Inventory is below the planning target. Recovery actions should be reviewed."
                )

            else:

                st.error(
                    "Inventory is significantly below the planning target. Immediate recovery actions are recommended."
                )

    # =========================================================
    # PURCHASE ORDER HEALTH
    # =========================================================

    def purchase_order_health(self):

        st.header("📄 Purchase Order Health")

        po = self.engine.purchase_order_health()

        with st.container(border=True):

            st.success("### 🟢 Purchase Order Dashboard")

            st.write(
                """
Review of all open Purchase Orders used within the planning
decision process.
"""
            )

            st.dataframe(

                pd.DataFrame(po),

                use_container_width=True,

                hide_index=True

            )

        with st.container(border=True):

            st.subheader("Planning Insight")

            st.info(
                """
Purchase Orders represent future inventory already committed
within the supply plan. During supply constraints they are
reviewed before any additional procurement is recommended.

Priority is always given to:

• Pulling older Purchase Orders forward

• Delaying lower-priority Purchase Orders where appropriate

• Raising a New Buy only if optimisation cannot recover
the remaining Planning Deficit.
"""
            )

    # =========================================================
    # STOCK BALANCE
    # =========================================================

    def stock_balance(self):

        st.header("🔄 Stock Balance")

        balance = self.engine.stock_balance()

        with st.container(border=True):

            st.subheader("Regional Stock Balancing")

            if balance["Status"] == "SUCCESS":

                st.success(

                    balance["Recommendation"]

                )

            else:

                st.warning(

                    balance["Recommendation"]

                )

        if balance["Status"] == "SUCCESS":

            with st.container(border=True):

                st.subheader("Recommended Transfers")

                transfers = pd.DataFrame(

                    balance["Transfers"]

                )

                st.dataframe(

                    transfers,

                    use_container_width=True,

                    hide_index=True

                )

        with st.container(border=True):

            st.subheader("Business Logic")

            st.write(
                """
Stock Balance is always the first optimisation step.

Before changing supplier schedules or creating a New Buy,
the planning engine evaluates whether inventory can be
rebalanced from regions operating above the Target Weeks
of Supply.

This reduces unnecessary procurement while improving
overall inventory utilisation.
"""
            )