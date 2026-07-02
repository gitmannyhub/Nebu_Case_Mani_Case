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

        "weekly_demand": 1673,

        "monthly_forecast": [
            6000,
            7500,
            9000,
            6500
        ],

        "regions": {

            "EU": {

                "on_hand": 6000,

                "weekly_demand": 693,

                "open_demand": 3000

            },

            "US": {

                "on_hand": 1500,

                "weekly_demand": 1039,

                "open_demand": 4500

            },

            "APAC": {

                "on_hand": 500,

                "weekly_demand": 462,

                "open_demand": 2000

            }

        },

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

            },

            {

                "po": "PO10003",

                "qty": 5000,

                "supplier": "CMHK",

                "status": "Open",

                "ship_date": "2026-09-20",

                "delivery_date": "2026-10-04"

            }

        ]
    }
]