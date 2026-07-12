import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_deal",
            description="Get a single Freshsales deal by ID with optional embedded related data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"},
                    "include": {"type": "string"},
                },
                "required": ["deal_id"],
            },
        ),
        Tool(
            name="freshsales_list_deals",
            description=(
                "List deals from Freshsales. "
                "IMPORTANT: You MUST call freshsales_list_filters(entity_type='deals') first "
                "to get the available view_ids — then pass one here. NEVER ask the user for a view_id."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "view_id": {"type": "integer", "description": "Get this from freshsales_list_filters first"},
                    "page": {"type": "integer", "default": 1},
                    "per_page": {"type": "integer", "default": 25},
                },
                "required": ["view_id"],
            },
        ),
        Tool(
            name="freshsales_create_deal",
            description="Create a new deal in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "amount": {"type": "number"},
                    "deal_stage_id": {"type": "integer"},
                    "expected_close": {"type": "string"},
                    "custom_field": {"type": "object"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="freshsales_update_deal",
            description="Update an existing Freshsales deal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"},
                    "updates": {"type": "object"},
                },
                "required": ["deal_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_upsert_deal",
            description="Create or update a deal by unique identifier (e.g. name).",
            inputSchema={
                "type": "object",
                "properties": {
                    "unique_identifier": {"type": "object"},
                    "deal": {"type": "object"},
                },
                "required": ["unique_identifier", "deal"],
            },
        ),
        Tool(
            name="freshsales_delete_deal",
            description="Permanently delete a Freshsales deal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"},
                },
                "required": ["deal_id"],
            },
        ),
        Tool(
            name="freshsales_clone_deal",
            description="Clone an existing Freshsales deal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"},
                },
                "required": ["deal_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_deal":
            params = {}
            if "include" in args:
                params["include"] = args["include"]
            return await client.get(f"/deals/{args['deal_id']}", params=params)

        elif name == "freshsales_list_deals":
            params = {
                "page": args.get("page", 1),
                "per_page": min(args.get("per_page", 25), 100),
            }
            return await client.get(f"/deals/view/{args['view_id']}", params=params)

        elif name == "freshsales_create_deal":
            return await client.post("/deals", body={"deal": args})

        elif name == "freshsales_update_deal":
            return await client.put(f"/deals/{args['deal_id']}", body={"deal": args["updates"]})

        elif name == "freshsales_upsert_deal":
            return await client.post("/deals/upsert", body={
                "deal": args["deal"],
                "unique_identifier": args["unique_identifier"],
            })

        elif name == "freshsales_delete_deal":
            return await client.delete(f"/deals/{args['deal_id']}")

        elif name == "freshsales_clone_deal":
            return await client.post(f"/deals/{args['deal_id']}/clone", body={})

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
