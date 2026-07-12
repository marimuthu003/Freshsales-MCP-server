import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_task",
            description="Get a single Freshsales task by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                },
                "required": ["task_id"],
            },
        ),
        Tool(
            name="freshsales_list_tasks",
            description="List tasks using a predefined filter.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {
                        "type": "string",
                        "enum": ["open", "due_today", "due_tomorrow", "overdue", "completed"]
                    },
                },
                "required": ["filter"],
            },
        ),
        Tool(
            name="freshsales_create_task",
            description="Create a new task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "due_date": {"type": "string"},
                    "targetable_type": {"type": "string"},
                    "targetable_id": {"type": "integer"},
                },
                "required": ["title", "due_date"],
            },
        ),
        Tool(
            name="freshsales_update_task",
            description="Update a task. Use status=1 to mark completed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "updates": {"type": "object"},
                },
                "required": ["task_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_delete_task",
            description="Delete a task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                },
                "required": ["task_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_task":
            return await client.get(f"/tasks/{args['task_id']}")

        elif name == "freshsales_list_tasks":
            return await client.get(f"/tasks", params={"filter": args["filter"]})

        elif name == "freshsales_create_task":
            return await client.post("/tasks", body={"task": args})

        elif name == "freshsales_update_task":
            return await client.put(f"/tasks/{args['task_id']}", body={"task": args["updates"]})

        elif name == "freshsales_delete_task":
            return await client.delete(f"/tasks/{args['task_id']}")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
