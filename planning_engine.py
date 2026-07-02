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

        self.regions = product["regions"]

        self.purchase_orders = product["purchase_orders"]

        self.monthly_forecast = product["monthly_forecast"]

    # ==========================================================
    # INVENTORY
    # ==========================================================

    def total_on_hand(self):

        total = 0

        for region in self.regions.values():

            total += region["on_hand"]

        return total

    def total_weekly_demand(self):

        total = 0

        for region in self.regions.values():

            total += region["weekly_demand"]

        return total

    def total_open_demand(self):

        total = 0

        for region in self.regions.values():

            total += region["open_demand"]

        return total

    def total_open_po(self):

        total = 0

        for po in self.purchase_orders:

            if po["status"] == "Open":

                total += po["qty"]

        return total

    def total_in_transit(self):

        total = 0

        for po in self.purchase_orders:

            if po["status"] == "In Transit":

                total += po["qty"]

        return total

    def inventory_position(self):

        return self.total_on_hand() + self.total_open_po()

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

    def target_inventory(self):

        return round(

            self.target_wos

            *

            self.total_weekly_demand()

        )

    def inventory_gap(self):

        gap = self.target_inventory() - self.inventory_position()

        return max(0, round(gap))

    # ==========================================================
    # REGIONAL WOS
    # ==========================================================

    def regional_wos(self):

        results = {}

        for region_name, region in self.regions.items():

            wos = round(

                region["on_hand"]

                /

                region["weekly_demand"],

                1

            )

            results[region_name] = {

                "On Hand": region["on_hand"],

                "Weekly Demand": region["weekly_demand"],

                "Open Demand": region["open_demand"],

                "Current WOS": wos,

                "Target WOS": self.target_wos

            }

        return results

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

            "Inventory Position": self.inventory_position(),

            "Inventory Gap": self.inventory_gap()

        }

    # ==========================================================
    # PURCHASE ORDER HEALTH
    # ==========================================================

    def purchase_order_health(self):

        results = []

        for po in self.purchase_orders:

            results.append({

                "PO": po["po"],

                "Quantity": po["qty"],

                "Status": po["status"],

                "Ship Date": po["ship_date"],

                "Delivery Date": po["delivery_date"]

            })

        return results
        # ==========================================================
    # STOCK BALANCE
    # ==========================================================

    def stock_balance(self):

        transfers = []

        for receiving_name, receiving in self.regions.items():

            receiving_wos = round(

                receiving["on_hand"] /

                receiving["weekly_demand"],

                1

            )

            if receiving_wos >= self.target_wos:

                continue

            shortage = round(

                (self.target_wos - receiving_wos)

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

                    (donor_wos - self.target_wos)

                    *

                    donor["weekly_demand"]

                )

                if surplus <= 0:
                    continue

                transfer = min(shortage, surplus)

                transfers.append({

                    "Receiving Region": receiving_name,

                    "Donor Region": donor_name,

                    "Transfer Qty": transfer,

                    "Receiving WOS": receiving_wos,

                    "Donor WOS": donor_wos

                })

                shortage -= transfer

                donor["on_hand"] -= transfer
                receiving["on_hand"] += transfer

                if shortage <= 0:
                    break

        if len(transfers) == 0:

            return {

                "Status": "FAILED",

                "Transfers": [],

                "Recommendation":

                    "No Stock Balance Available"

            }

        return {

            "Status": "SUCCESS",

            "Transfers": transfers,

            "Recommendation":

                "Execute Stock Transfer"

        }

    # ==========================================================
    # PULL LOGIC
    # ==========================================================

    def pull_logic(self):

        balance = self.stock_balance()

        if balance["Status"] == "SUCCESS":

            return {

                "Status": "NOT REQUIRED",

                "Pulled Qty": 0,

                "POs": [],

                "Recommendation":

                    "Stock Balance resolved shortage"

            }

        remaining_gap = self.inventory_gap()

        candidates = [

            po

            for po in self.purchase_orders

            if po["status"] == "Open"

        ]

        candidates.sort(

            key=lambda x: datetime.strptime(

                x["delivery_date"],

                "%Y-%m-%d"

            )

        )

        pulled = []

        total = 0

        for po in candidates:

            if remaining_gap <= 0:
                break

            qty = min(

                po["qty"],

                remaining_gap

            )

            pulled.append({

                "PO": po["po"],

                "Qty": qty,

                "Original Delivery":

                    po["delivery_date"]

            })

            total += qty

            remaining_gap -= qty

        if total == 0:

            return {

                "Status": "FAILED",

                "Pulled Qty": 0,

                "POs": [],

                "Recommendation":

                    "No Pull Candidates"

            }

        return {

            "Status": "SUCCESS",

            "Priority":

                "Oldest PO First",

            "Pulled Qty": total,

            "Remaining Gap": remaining_gap,

            "POs": pulled,

            "Recommendation":

                f"Prioritise {len(pulled)} Purchase Orders"

        }

    # ==========================================================
    # PUSH LOGIC
    # ==========================================================

    def push_logic(self):

        pull = self.pull_logic()

        if pull["Status"] != "SUCCESS":

            return {

                "Status": "NOT REQUIRED",

                "Pushed Qty": 0,

                "POs": [],

                "Recommendation":

                    "No Push Required"

            }

        required_capacity = pull["Pulled Qty"]

        candidates = [

            po

            for po in self.purchase_orders

            if po["status"] == "Open"

        ]

        candidates.sort(

            key=lambda x: datetime.strptime(

                x["delivery_date"],

                "%Y-%m-%d"

            ),

            reverse=True

        )

        pushed = []

        capacity = 0

        for po in candidates:

            if capacity >= required_capacity:
                break

            qty = min(

                po["qty"],

                required_capacity - capacity

            )

            pushed.append({

                "PO": po["po"],

                "Qty": qty,

                "Original Delivery":

                    po["delivery_date"]

            })

            capacity += qty

        return {

            "Status": "SUCCESS",

            "Priority":

                "Newest PO First",

            "Pushed Qty": capacity,

            "Required Capacity": required_capacity,

            "POs": pushed,

            "Recommendation":

                f"Push {capacity:,} units to free OEM capacity"

        }
        # ==========================================================
    # PO SHORTAGE
    # ==========================================================

    def po_shortage(self):

        balance = self.stock_balance()

        if balance["Status"] == "SUCCESS":

            return {

                "Required": False,

                "Reason": "Resolved through Stock Balance",

                "OEM Capacity Shortage": 0,

                "Recommended PO": 0

            }

        pull = self.pull_logic()

        if pull["Status"] != "SUCCESS":

            return {

                "Required": False,

                "Reason": "No Pull Candidates",

                "OEM Capacity Shortage": 0,

                "Recommended PO": 0

            }

        push = self.push_logic()

        shortage = max(

            0,

            pull["Pulled Qty"]

            -

            push["Pushed Qty"]

        )

        if shortage == 0:

            return {

                "Required": False,

                "Reason": "OEM Capacity Available",

                "OEM Capacity Shortage": 0,

                "Recommended PO": 0

            }

        recommendation = max(

            shortage,

            self.moq

        )

        return {

            "Required": True,

            "Reason":

                "Pull exceeded Push capacity",

            "OEM Capacity Shortage":

                shortage,

            "Recommended PO":

                recommendation

        }

    # ==========================================================
    # ALLOCATION ENGINE
    # ==========================================================

    def allocation_engine(self):

        available = self.total_on_hand()

        allocation = {}

        priority = [

            "US",

            "EU",

            "APAC"

        ]

        remaining = available

        for region in priority:

            demand = self.regions[region]["open_demand"]

            allocated = min(

                demand,

                remaining

            )

            backlog = demand - allocated

            fill_rate = round(

                allocated / demand * 100,

                1

            )

            allocation[region] = {

                "Demand": demand,

                "Allocated": allocated,

                "Backlog": backlog,

                "Fill Rate": fill_rate

            }

            remaining -= allocated

        return {

            "Available Inventory":

                available,

            "Remaining Inventory":

                remaining,

            "Regions":

                allocation

        }

    # ==========================================================
    # BACKLOG RISK
    # ==========================================================

    def backlog_risk(self):

        if self.backlog > 0:

            if self.lead_time >= 8:

                level = "Critical"

            elif self.lead_time >= 6:

                level = "High"

            elif self.lead_time >= 3:

                level = "Moderate"

            else:

                level = "Low"

        else:

            weeks_left = self.current_wos()

            if weeks_left <= 3:

                level = "High"

            elif weeks_left <= 6:

                level = "Moderate"

            else:

                level = "Low"

        return {

            "Current Backlog":

                self.backlog,

            "Risk":

                level,

            "Recommendation": {

                "Critical":

                    "Immediate escalation",

                "High":

                    "Daily monitoring",

                "Moderate":

                    "Weekly review",

                "Low":

                    "Monitor"

            }[level]

        }

    # ==========================================================
    # SUPPLIER HEALTH
    # ==========================================================

    def supplier_health(self):

        delayed = self.total_open_po()

        status = "Healthy"

        if delayed > 0:

            status = "Monitor"

        if self.backlog > 0:

            status = "High Risk"

        return {

            "Supplier":

                self.supplier,

            "Status":

                status,

            "Lead Time":

                self.lead_time,

            "Shipping":

                self.shipping_time,

            "Open PO":

                self.total_open_po(),

            "In Transit":

                self.total_in_transit()

        }

    # ==========================================================
    # DECISION LOG
    # ==========================================================

    def decision_log(self):

        decisions = []

        decisions.append({

            "Step":1,

            "Decision":

                self.stock_balance()["Recommendation"]

        })

        decisions.append({

            "Step":2,

            "Decision":

                self.pull_logic()["Recommendation"]

        })

        decisions.append({

            "Step":3,

            "Decision":

                self.push_logic()["Recommendation"]

        })

        decisions.append({

            "Step":4,

            "Decision":

                self.po_shortage()["Reason"]

        })

        decisions.append({

            "Step":5,

            "Decision":

                self.backlog_risk()["Recommendation"]

        })

        return decisions

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

            "Backlog":

                self.backlog_risk(),

            "Supplier":

                self.supplier_health()

        }

    # ==========================================================
    # AI EXECUTIVE SUMMARY
    # ==========================================================

    def ai_summary(self):

        shortage = self.po_shortage()

        return f"""
SUPPLY PLANNING DECISION REPORT

Current WOS:
{self.current_wos()} weeks

Target WOS:
{self.target_wos} weeks

Inventory Position:
{self.inventory_position():,} units

Stock Balance:
{self.stock_balance()['Recommendation']}

Pull Logic:
{self.pull_logic()['Recommendation']}

Push Logic:
{self.push_logic()['Recommendation']}

PO Shortage:
{shortage['Reason']}

Recommended New Buy:
{shortage['Recommended PO']:,} units

Backlog Risk:
{self.backlog_risk()['Risk']}

Supplier Status:
{self.supplier_health()['Status']}

Recommended Action:

1. Execute Stock Balance if available.
2. Pull oldest purchase orders.
3. Push newest purchase orders to free OEM capacity.
4. Raise a New Buy Purchase Order only if Pull/Push cannot resolve the shortage.
5. Monitor backlog until supplier recovery is confirmed.
"""