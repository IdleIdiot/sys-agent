message_template = {
    "log": {
        "host_id": "",
        "item_id": "",
        "agent_time": "",
        "value1": "",
        "log_info": "",
        "alias": "",
    },
    "process": {
        "host_id": "",
        "item_id": "",
        "agent_time": "",
        "pid": "",
        "cpu": "",
        "mem": "",
        "alias": "",
    },
    "resource": {
        "host_id": "",
        "item_id": "",
        "agent_time": "",
        "value1": "",
        "alias": "",
    },
}

message_mapping = {
    "resource": {
        "mappings": {
            "properties": {
                "agent_time": {
                    "type": "date",
                    "format": " yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis",
                },
                "host_id": {
                    "type": "text",
                },
                "item_id": {
                    "type": "keyword",
                },
                "value1": {
                    "type": "long",
                },
                "alias": {
                    "type": "text",
                },
            },
        }
    },
    "log": {
        "mappings": {
            "properties": {
                "agent_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis",
                },
                "host_id": {
                    "type": "text",
                },
                "item_id": {
                    "type": "keyword",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256,
                        },
                    },
                },
                "value1": {
                    "type": "long",
                },
                "log_info": {
                    "type": "text",
                },
                "alias": {
                    "type": "text",
                },
            }
        }
    },
    "process": {
        "mappings": {
            "properties": {
                "agent_time": {
                    "type": "date",
                    "format": " yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis",
                },
                "host_id": {
                    "type": "text",
                },
                "item_id": {
                    "type": "keyword",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256,
                        },
                    },
                },
                "pid": {
                    "type": "long",
                },
                "cpu": {
                    "type": "long",
                },
                "mem": {
                    "type": "long",
                },
                "alias": {
                    "type": "text",
                },
            }
        }
    },
}
