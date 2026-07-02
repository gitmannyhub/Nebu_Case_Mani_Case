products = [
    {
        "part_number": "FLAGSHIP123",

        "description": "Smart Home Hub",

        "supplier": "CMHK",

        "target_wos": 12,

        "moq": 5000,

        "lead_time": 8,

        "shipping_time": 2,

        "backlog": 9500,

        # ======================================================
        # BUSINESS CASE DATA
        # ======================================================

        "weekly_demand": 1673,

        "monthly_forecast": [

            6000,

            7500,

            9000,

            6500

        ],

        # ======================================================
        # REGIONAL INVENTORY
        #
        # Total On Hand = 8,000
        #
        # EU = 6,000
        # US = 1,500
        # APAC = 500
        # ======================================================

        "regions": {

            "EU": {

                "on_hand": 6000,

                "weekly_demand": 693,

                "open_demand": 3000

            },

            "US": {

                "on_hand": 1500,

                "weekly_demand": 518,

                "open_demand": 4500

            },

            "APAC": {

                "on_hand": 500,

                "weekly_demand": 462,

                "open_demand": 2000

            }

        },

        # ======================================================
        # PURCHASE ORDERS
        #
        # IMPORTANT
        #
        # Open PO = 10,000
        #
        # = 4,000 In Transit
        #
        # + 6,000 Still Open
        #
        # DO NOT ADD ANY MORE POs
        #
        # Otherwise Inventory Position
        # becomes incorrect.
        # ======================================================

        "purchase_orders": [

            {

                "po": "PO10001",

                "qty": 4000,

                "supplier": "CMHK",

                "status": "In Transit",

                "ship_date": "2026-06-19",

                "delivery_date": "2026-07-03"

            },

            {

                "po": "PO10002",

                "qty": 6000,

                "supplier": "CMHK",

                "status": "Open",

                "ship_date": "2026-08-15",

                "delivery_date": "2026-08-29"

            }

        ]

    }

]