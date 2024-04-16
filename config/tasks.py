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
        "items": ["1001", "1002", "1003"],
        "template": message_template["resource"],
    },
}
