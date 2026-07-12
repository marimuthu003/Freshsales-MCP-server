import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_activity",
            description="Get a single custom activity by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {"type": "integer"},
                },
                "required": ["activity_id"],
            },
        ),
        Tool(
            name="freshsales_list_activities",
            description="List all activities.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="freshsales_create_activity",
            description="Create an activity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "start_date": {"type": "string"},
                    "end_date": {"type": "string"},
                    "targetable_type": {"type": "string"},
                    "targetable_id": {"type": "integer"},
                },
                "required": ["title", "start_date", "end_date"],
            },
        ),
        Tool(
            name="freshsales_update_activity",
            description="Update an activity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {"type": "integer"},
                    "updates": {"type": "object"},
                },
                "required": ["activity_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_delete_activity",
            description="Delete an activity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "activity_id": {"type": "integer"},
                },
                "required": ["activity_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_activity":
            return await client.get(f"/sales_activities/{args['activity_id']}")

        elif name == "freshsales_list_activities":
            return await client.get(f"/sales_activities")

        elif name == "freshsales_create_activity":
            return await client.post("/sales_activities", body={"sales_activity": args})

        elif name == "freshsales_update_activity":
            return await client.put(f"/sales_activities/{args['activity_id']}", body={"sales_activity": args["updates"]})

        elif name == "freshsales_delete_activity":
            return await client.delete(f"/sales_activities/{args['activity_id']}")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
