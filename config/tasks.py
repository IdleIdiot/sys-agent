from config.message import message_template

test_task = {
    "log": {
        "items": [],
        "template": message_template["log"],
    },
    "process": {
        "items": [],
        "template": message_template["process"],
    },
    "resource": {
        "items": [
            "1001",
            "1002",
            "2001",
            "2002",
            "2003",
            "2004",
            "2005",
            "2006",
            "2007",
            "2008",
            "2021",
            "2022",
            "2023",
            "2024",
            "2025",
            "2026",
            "2027",
            "2028",
        ],
        "template": message_template["resource"],
    },
}
