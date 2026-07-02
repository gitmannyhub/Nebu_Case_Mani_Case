import streamlit as st
import pandas as pd


class ReportEngine:

    def __init__(self, engine):
        self.engine = engine

    def render(self):

        self.executive_summary()
        self.inventory_health()
        self.purchase_order_health()
        self.stock_balance()
        self.pull_logic()
        self.push_logic()
        self.po_shortage()
        self.allocation_engine()
        self.backlog_risk()
        self.supplier_health()
        self.decision_log()
        self.ai_summary()

    # =========================================================

    def executive_summary(self):

        st.header("📋 Executive Summary")

        inv = self.engine.inventory_health()
        backlog = self.engine.backlog_risk()
        supplier = self.engine.supplier_health()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Current WOS", inv["Current WOS"])
        c2.metric("Target WOS", inv["Target WOS"])
        c3.metric("Inventory Gap", f'{inv["Inventory Gap"]:,}')
        c4.metric("Backlog", f'{backlog["Current Backlog"]:,}')

        st.info(
            f"""
**Overall Status**

• Inventory Health : **{inv["Status"]}**

• Backlog Risk : **{backlog["Risk"]}**

• Supplier Status : **{supplier["Status"]}**
"""
        )

    # =========================================================

    def inventory_health(self):

        st.header("📦 Inventory Health")

        inv = self.engine.inventory_health()

        df = pd.DataFrame(
            {
                "Metric": inv.keys(),
                "Value": inv.values()
            }
        )

        st.dataframe(df, use_container_width=True)

    # =========================================================

    def purchase_order_health(self):

        st.header("📄 Purchase Order Health")

        df = pd.DataFrame(
            self.engine.purchase_order_health()
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # =========================================================

    def stock_balance(self):

        st.header("🔄 Stock Balance")

        balance = self.engine.stock_balance()

        st.success(balance["Recommendation"])

        if len(balance["Transfers"]) > 0:

            df = pd.DataFrame(balance["Transfers"])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    # =========================================================

    def pull_logic(self):

        st.header("⬆️ Pull Logic")

        pull = self.engine.pull_logic()

        st.info(pull["Recommendation"])

        if len(pull["POs"]) > 0:

            df = pd.DataFrame(pull["POs"])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    # =========================================================

    def push_logic(self):

        st.header("⬇️ Push Logic")

        push = self.engine.push_logic()

        st.info(push["Recommendation"])

        if len(push["POs"]) > 0:

            df = pd.DataFrame(push["POs"])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

    # =========================================================

    def po_shortage(self):

        st.header("🚨 PO Shortage")

        shortage = self.engine.po_shortage()

        col1, col2 = st.columns(2)

        col1.metric(
            "OEM Capacity Shortage",
            shortage["OEM Capacity Shortage"]
        )

        col2.metric(
            "Recommended New Buy",
            shortage["Recommended PO"]
        )

        st.warning(shortage["Reason"])

    # =========================================================

    def allocation_engine(self):

        st.header("🌍 Allocation Engine")

        allocation = self.engine.allocation_engine()

        st.metric(
            "Available Inventory",
            allocation["Available Inventory"]
        )

        rows = []

        for region, values in allocation["Regions"].items():

            rows.append({

                "Region": region,

                "Demand": values["Demand"],

                "Allocated": values["Allocated"],

                "Backlog": values["Backlog"],

                "Fill Rate %": values["Fill Rate"]

            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # =========================================================

    def backlog_risk(self):

        st.header("⚠️ Backlog Risk")

        risk = self.engine.backlog_risk()

        c1, c2 = st.columns(2)

        c1.metric(
            "Current Backlog",
            risk["Current Backlog"]
        )

        c2.metric(
            "Risk",
            risk["Risk"]
        )

        st.error(risk["Recommendation"])

    # =========================================================

    def supplier_health(self):

        st.header("🏭 Supplier Health")

        supplier = self.engine.supplier_health()

        df = pd.DataFrame(
            {
                "Metric": supplier.keys(),
                "Value": supplier.values()
            }
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    # =========================================================

    def decision_log(self):

        st.header("📝 Decision Log")

        df = pd.DataFrame(
            self.engine.decision_log()
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # =========================================================

    def ai_summary(self):

        st.header("🤖 AI Executive Summary")

        st.success(
            self.engine.ai_summary()
        )