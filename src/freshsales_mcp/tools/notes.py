import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_create_note",
            description="Create a note for a contact, account, or deal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "targetable_type": {
                        "type": "string",
                        "enum": ["Contact", "Account", "Deal"]
                    },
                    "targetable_id": {"type": "integer"},
                },
                "required": ["description", "targetable_type", "targetable_id"],
            },
        ),
        Tool(
            name="freshsales_update_note",
            description="Update an existing note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {"type": "integer"},
                    "description": {"type": "string"},
                },
                "required": ["note_id", "description"],
            },
        ),
        Tool(
            name="freshsales_delete_note",
            description="Delete a note.",
            inputSchema={
                "type": "object",
                "properties": {
                    "note_id": {"type": "integer"},
                },
                "required": ["note_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_create_note":
            return await client.post("/notes", body={"note": args})

        elif name == "freshsales_update_note":
            return await client.put(f"/notes/{args['note_id']}", body={"note": {"description": args["description"]}})

        elif name == "freshsales_delete_note":
            return await client.delete(f"/notes/{args['note_id']}")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
