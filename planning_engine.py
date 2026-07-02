from datetime import datetime


class SupplyPlanningEngine:

    def __init__(self, product):

        self.product = product

        self.part_number = product["part_number"]
        self.description = product["description"]

        self.supplier = product["supplier"]

        self.target_wos = product["target_wos"]

        self.moq = product["moq"]

        self.backlog = product["backlog"]

        self.lead_time = product["lead_time"]

        self.shipping_time = product["shipping_time"]

        self.weekly_demand = product["weekly_demand"]

        self.monthly_forecast = product["monthly_forecast"]

        self.regions = product["regions"]

        self.purchase_orders = product["purchase_orders"]

    # ==========================================================
    # INVENTORY
    # ==========================================================

    def total_on_hand(self):

        return sum(

            region["on_hand"]

            for region in self.regions.values()

        )

    def total_weekly_demand(self):

        return self.weekly_demand

    def total_open_demand(self):

        return sum(

            region["open_demand"]

            for region in self.regions.values()

        )

    def total_open_po(self):

        """
        Open PO already includes
        In Transit quantities.
        """

        return sum(

            po["qty"]

            for po in self.purchase_orders

        )

    def total_in_transit(self):

        return sum(

            po["qty"]

            for po in self.purchase_orders

            if po["status"] == "In Transit"

        )

    def inventory_position(self):

        """
        Inventory Position

        On Hand

        +

        Open PO

        (Do NOT add In Transit again.)
        """

        return (

            self.total_on_hand()

            +

            self.total_open_po()

        )
        # ==========================================================
    # WEEKS OF SUPPLY
    # ==========================================================

    def current_wos(self):

        return round(

            self.total_on_hand()

            /

            self.total_weekly_demand(),

            1

        )

    def pipeline_wos(self):

        return round(

            self.inventory_position()

            /

            self.total_weekly_demand(),

            1

        )

    def disruption_wos(self):

        """
        Assumes only inventory already
        shipped is available.

        On Hand

        +

        In Transit
        """

        return round(

            (

                self.total_on_hand()

                +

                self.total_in_transit()

            )

            /

            self.total_weekly_demand(),

            1

        )

    # ==========================================================
    # TARGET INVENTORY
    # ==========================================================

    def target_inventory(self):

        """
        Target Inventory

        =

        Target WOS

        x

        Weekly Demand
        """

        return round(

            self.target_wos

            *

            self.total_weekly_demand()

        )

    def planning_deficit(self):

        """
        Planning Deficit

        =

        Target Inventory

        -

        Inventory Position
        """

        return max(

            0,

            self.target_inventory()

            -

            self.inventory_position()

        )

    # ==========================================================
    # INVENTORY HEALTH
    # ==========================================================

    def inventory_health(self):

        current = self.current_wos()

        if current >= self.target_wos:

            status = "Healthy"

        elif current >= 8:

            status = "Monitor"

        else:

            status = "Critical"

        return {

            "Status": status,

            "Current WOS": current,

            "Pipeline WOS": self.pipeline_wos(),

            "Disruption WOS": self.disruption_wos(),

            "Target WOS": self.target_wos,

            "Target Inventory": self.target_inventory(),

            "Inventory Position": self.inventory_position(),

            "Planning Deficit": self.planning_deficit()

        }

    # ==========================================================
    # PURCHASE ORDER HEALTH
    # ==========================================================

    def purchase_order_health(self):

        rows = []

        for po in self.purchase_orders:

            rows.append({

                "PO": po["po"],

                "Quantity": po["qty"],

                "Status": po["status"],

                "Ship Date": po["ship_date"],

                "Delivery Date": po["delivery_date"]

            })

        return rows
        # ==========================================================
    # STOCK BALANCE
    # ==========================================================

    def stock_balance(self):

        transfers = []

        for receiving_name, receiving in self.regions.items():

            receiving_wos = round(

                receiving["on_hand"]

                /

                receiving["weekly_demand"],

                1

            )

            if receiving_wos >= self.target_wos:

                continue

            shortage = round(

                (

                    self.target_wos

                    -

                    receiving_wos

                )

                *

                receiving["weekly_demand"]

            )

            for donor_name, donor in self.regions.items():

                if donor_name == receiving_name:

                    continue

                donor_wos = round(

                    donor["on_hand"]

                    /

                    donor["weekly_demand"],

                    1

                )

                if donor_wos <= self.target_wos:

                    continue

                surplus = round(

                    (

                        donor_wos

                        -

                        self.target_wos

                    )

                    *

                    donor["weekly_demand"]

                )

                if surplus <= 0:

                    continue

                transfer_qty = min(

                    shortage,

                    surplus

                )

                transfers.append({

                    "Receiving Region": receiving_name,

                    "Donor Region": donor_name,

                    "Transfer Qty": transfer_qty,

                    "Receiving WOS": receiving_wos,

                    "Donor WOS": donor_wos

                })

                shortage -= transfer_qty

                if shortage <= 0:

                    break

        if len(transfers) == 0:

            return {

                "Status": "FAILED",

                "Transfers": [],

                "Recommendation": "No Stock Balance Available"

            }

        return {

            "Status": "SUCCESS",

            "Transfers": transfers,

            "Recommendation": "Execute Stock Balance"

        }
        # ==========================================================
    # PULL LOGIC
    # ==========================================================

    def pull_logic(self):

        balance = self.stock_balance()

        if balance["Status"] == "SUCCESS":

            return {

                "Status": "NOT REQUIRED",

                "Priority": "Oldest PO First",

                "Pulled Qty": 0,

                "Remaining Deficit": 0,

                "POs": [],

                "Recommendation": "Recovered through Stock Balance"

            }

        remaining = self.planning_deficit()

        candidates = [

            po

            for po in self.purchase_orders

            if po["status"] == "Open"

        ]

        candidates.sort(

            key=lambda po: datetime.strptime(

                po["delivery_date"],

                "%Y-%m-%d"

            )

        )

        pulled = []

        pulled_qty = 0

        for po in candidates:

            if remaining <= 0:

                break

            qty = min(

                po["qty"],

                remaining

            )

            pulled.append({

                "PO": po["po"],

                "Qty": qty,

                "Original Delivery": po["delivery_date"]

            })

            pulled_qty += qty

            remaining -= qty

        if pulled_qty == 0:

            return {

                "Status": "FAILED",

                "Priority": "Oldest PO First",

                "Pulled Qty": 0,

                "Remaining Deficit": self.planning_deficit(),

                "POs": [],

                "Recommendation": "No Open Purchase Orders Available"

            }

        return {

            "Status": "SUCCESS",

            "Priority": "Oldest PO First",

            "Pulled Qty": pulled_qty,

            "Remaining Deficit": remaining,

            "POs": pulled,

            "Recommendation": f"Prioritise {len(pulled)} Purchase Orders"

        }
        # ==========================================================
    # PUSH LOGIC
    # ==========================================================

    def push_logic(self):

        pull = self.pull_logic()

        if pull["Status"] != "SUCCESS":

            return {

                "Status": "NOT REQUIRED",

                "Priority": "Newest PO First",

                "Pushed Qty": 0,

                "Required Capacity": 0,

                "POs": [],

                "Recommendation": "No Push Required"

            }

        required_capacity = pull["Pulled Qty"]

        candidates = [

            po

            for po in self.purchase_orders

            if po["status"] == "Open"

        ]

        candidates.sort(

            key=lambda po: datetime.strptime(

                po["delivery_date"],

                "%Y-%m-%d"

            ),

            reverse=True

        )

        pushed = []

        pushed_qty = 0

        for po in candidates:

            if pushed_qty >= required_capacity:

                break

            qty = min(

                po["qty"],

                required_capacity - pushed_qty

            )

            pushed.append({

                "PO": po["po"],

                "Qty": qty,

                "Original Delivery": po["delivery_date"]

            })

            pushed_qty += qty

        return {

            "Status": "SUCCESS",

            "Priority": "Newest PO First",

            "Pushed Qty": pushed_qty,

            "Required Capacity": required_capacity,

            "POs": pushed,

            "Recommendation": f"Push {pushed_qty:,} units to free OEM capacity"

        }

    # ==========================================================
    # PO SHORTAGE
    # ==========================================================

    def po_shortage(self):

        deficit = self.planning_deficit()

        if deficit <= 0:

            return {

                "Required": False,

                "Reason": "Target Inventory Achieved",

                "Planning Deficit": 0,

                "MOQ": self.moq,

                "Recommended PO": 0

            }

        return {

            "Required": True,

            "Reason": "Planning Deficit Identified",

            "Planning Deficit": deficit,

            "MOQ": self.moq,

            "Recommended PO": max(deficit, self.moq)

        }
        # ==========================================================
    # ALLOCATION ENGINE
    # ==========================================================

    def allocation_engine(self):

        available = self.total_on_hand()

        remaining = available

        allocation = {}

        priority = [

            "US",

            "EU",

            "APAC"

        ]

        for region in priority:

            demand = self.regions[region]["open_demand"]

            allocated = min(

                demand,

                remaining

            )

            backlog = demand - allocated

            fill_rate = round(

                (allocated / demand) * 100,

                1

            ) if demand > 0 else 0

            allocation[region] = {

                "Demand": demand,

                "Allocated": allocated,

                "Backlog": backlog,

                "Fill Rate": fill_rate

            }

            remaining -= allocated

        return {

            "Available Inventory": available,

            "Remaining Inventory": remaining,

            "Regions": allocation

        }

    # ==========================================================
    # BACKLOG RISK
    # ==========================================================

    def backlog_risk(self):

        if self.backlog > 0:

            if self.lead_time >= 8:

                risk = "Critical"

            elif self.lead_time >= 6:

                risk = "High"

            elif self.lead_time >= 3:

                risk = "Moderate"

            else:

                risk = "Low"

        else:

            risk = "Low"

        recommendations = {

            "Critical":

                "Immediate escalation with supplier and executive review.",

            "High":

                "Daily monitoring and supplier recovery plan.",

            "Moderate":

                "Weekly review of supply position.",

            "Low":

                "Continue monitoring."

        }

        return {

            "Current Backlog": self.backlog,

            "Risk": risk,

            "Recommendation": recommendations[risk]

        }

    # ==========================================================
    # SUPPLIER HEALTH
    # ==========================================================

    def supplier_health(self):

        status = "Healthy"

        if self.backlog > 0:

            status = "High Risk"

        elif self.total_open_po() > 0:

            status = "Monitor"

        return {

            "Supplier": self.supplier,

            "Status": status,

            "Lead Time": self.lead_time,

            "Shipping": self.shipping_time,

            "Open PO": self.total_open_po(),

            "In Transit": self.total_in_transit(),

            "PO Balance": self.total_open_po() - self.total_in_transit()

        }
        # ==========================================================
    # DECISION LOG
    # ==========================================================

    def decision_log(self):

        return [

            {

                "Step": 1,

                "Decision":

                    self.stock_balance()["Recommendation"]

            },

            {

                "Step": 2,

                "Decision":

                    self.pull_logic()["Recommendation"]

            },

            {

                "Step": 3,

                "Decision":

                    self.push_logic()["Recommendation"]

            },

            {

                "Step": 4,

                "Decision":

                    self.po_shortage()["Reason"]

            },

            {

                "Step": 5,

                "Decision":

                    self.backlog_risk()["Recommendation"]

            }

        ]

    # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    def executive_summary(self):

        return {

            "Inventory":

                self.inventory_health(),

            "Stock Balance":

                self.stock_balance(),

            "Pull":

                self.pull_logic(),

            "Push":

                self.push_logic(),

            "PO Shortage":

                self.po_shortage(),

            "Allocation":

                self.allocation_engine(),

            "Backlog":

                self.backlog_risk(),

            "Supplier":

                self.supplier_health()

        }

    # ==========================================================
    # AI EXECUTIVE SUMMARY
    # ==========================================================

    def ai_summary(self):

        inventory = self.inventory_health()

        shortage = self.po_shortage()

        return f"""
SUPPLY PLANNING DECISION REPORT

Current WOS: {inventory['Current WOS']} weeks
Pipeline WOS: {inventory['Pipeline WOS']} weeks
Disruption WOS: {inventory['Disruption WOS']} weeks

Target WOS: {self.target_wos} weeks

Target Inventory: {inventory['Target Inventory']:,} units

Inventory Position: {inventory['Inventory Position']:,} units

Planning Deficit: {inventory['Planning Deficit']:,} units

Recommended New Buy: {shortage['Recommended PO']:,} units

Supplier MOQ: {self.moq:,} units

Backlog Risk: {self.backlog_risk()['Risk']}

Supplier Status: {self.supplier_health()['Status']}

Planning Sequence

1. Review Inventory Health
2. Execute Stock Balance
3. Pull Oldest Purchase Orders
4. Push Newest Purchase Orders
5. Review Planning Deficit
6. Raise New Buy only if a deficit remains

Planning Formula

Target Inventory
=
Target WOS × Weekly Demand

Inventory Position
=
On Hand + Open Purchase Orders

Planning Deficit
=
Target Inventory − Inventory Position

Recommended New Buy
=
MAX(Planning Deficit, MOQ)
"""
    