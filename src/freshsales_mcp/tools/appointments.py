import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_appointment",
            description="Get a single appointment by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer"},
                },
                "required": ["appointment_id"],
            },
        ),
        Tool(
            name="freshsales_list_appointments",
            description="List appointments by filter.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "enum": ["upcoming", "past", "overdue"]
                    },
                },
                "required": ["filter"],
            },
        ),
        Tool(
            name="freshsales_create_appointment",
            description="Create an appointment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "from_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "attendees": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string"},
                                "name": {"type": "string"}
                            }
                        }
                    },
                    "targetable_type": {"type": "string"},
                    "targetable_id": {"type": "integer"},
                },
                "required": ["title", "from_date", "end_date"],
            },
        ),
        Tool(
            name="freshsales_update_appointment",
            description="Update an appointment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer"},
                    "updates": {"type": "object"},
                },
                "required": ["appointment_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_delete_appointment",
            description="Delete an appointment.",
            inputSchema={
                "type": "object",
                "properties": {
                    "appointment_id": {"type": "integer"},
                },
                "required": ["appointment_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_appointment":
            return await client.get(f"/appointments/{args['appointment_id']}")

        elif name == "freshsales_list_appointments":
            return await client.get(f"/appointments", params={"filter": args["filter"]})

        elif name == "freshsales_create_appointment":
            return await client.post("/appointments", body={"appointment": args})

        elif name == "freshsales_update_appointment":
            return await client.put(f"/appointments/{args['appointment_id']}", body={"appointment": args["updates"]})

        elif name == "freshsales_delete_appointment":
            return await client.delete(f"/appointments/{args['appointment_id']}")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
