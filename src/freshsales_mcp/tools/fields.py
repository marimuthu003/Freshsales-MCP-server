import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_list_fields",
            description="Get field definitions including custom fields for an entity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {
                        "type": "string",
                        "enum": ["contacts", "deals", "sales_accounts", "tasks", "appointments"],
                    },
                },
                "required": ["entity_type"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_list_fields":
            return await client.get(f"/settings/{args['entity_type']}/fields")
        
        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
