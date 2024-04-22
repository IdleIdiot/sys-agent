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
        ],
        "template": message_template["resource"],
    },
}
