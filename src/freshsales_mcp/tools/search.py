import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_search",
            description="Fuzzy text match across name, email, phone, address, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "include": {"type": "string", "default": "contacts,accounts,deals"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="freshsales_lookup",
            description="Exact match lookup for a specific field and entity type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {"type": "string"},
                    "field": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["entity_type", "field", "value"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_search":
            return await client.get("/search", params={"q": args["query"], "include": args.get("include", "contacts,accounts,deals")})

        elif name == "freshsales_lookup":
            return await client.get("/lookup", params={"q": args["value"], "f": args["field"], "entities": args["entity_type"]})

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
