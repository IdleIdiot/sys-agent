from config.message import message_template


base_task = {
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
        ],
        "template": message_template["resource"],
    },
}


linux_with_2_gpu_task = {
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
            "1003",
            "1004",
            "1005",
            "1006",
            "2001",
            "2002",
            "2005",
            "2006",
            "2009",
            "2010",
            "2013",
            "2014",
            "2017",
            "2018",
        ],
        "template": message_template["resource"],
    },
}
