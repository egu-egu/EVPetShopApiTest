ORDER_SCHEMA = {
"type": "object",
"properties": {
"id": {
"type": "integer"
},
"petId": {
"type": "integer"
},
"quantity": {
"type": "integer"
},
"shipDate": {
"type": "string"
},
"status": {
"type": "string",
"enum": ["placed", "approved", "delivered"]
},
"complete": {
"type": "boolean"
}
},
"required": ["id", "petId", "quantity", "status", "complete"],
"additionalProperties": False
}

INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        }
    },
    "additionalProperties": False,
    "anyOf": [
        {"required": ["approved"]},
        {"required": ["delivered"]}
    ]
}