import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_account",
            description="Get a single Freshsales account by ID with optional embedded related data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"},
                    "include": {"type": "string"},
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="freshsales_list_accounts",
            description="List accounts from a Freshsales view.",
            inputSchema={
                "type": "object",
                "properties": {
                    "view_id": {"type": "integer"},
                    "page": {"type": "integer", "default": 1},
                    "per_page": {"type": "integer", "default": 25},
                },
                "required": ["view_id"],
            },
        ),
        Tool(
            name="freshsales_create_account",
            description="Create a new account in Freshsales. Name is required.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "custom_field": {"type": "object"},
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="freshsales_update_account",
            description="Update an existing Freshsales account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"},
                    "updates": {"type": "object"},
                },
                "required": ["account_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_upsert_account",
            description="Create or update an account by unique identifier (e.g. name).",
            inputSchema={
                "type": "object",
                "properties": {
                    "unique_identifier": {"type": "object"},
                    "sales_account": {"type": "object"},
                },
                "required": ["unique_identifier", "sales_account"],
            },
        ),
        Tool(
            name="freshsales_delete_account",
            description="Permanently delete a Freshsales account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"},
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="freshsales_clone_account",
            description="Clone an existing Freshsales account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"},
                },
                "required": ["account_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_account":
            params = {}
            if "include" in args:
                params["include"] = args["include"]
            return await client.get(f"/sales_accounts/{args['account_id']}", params=params)

        elif name == "freshsales_list_accounts":
            params = {
                "page": args.get("page", 1),
                "per_page": min(args.get("per_page", 25), 100),
            }
            return await client.get(f"/sales_accounts/view/{args['view_id']}", params=params)

        elif name == "freshsales_create_account":
            return await client.post("/sales_accounts", body={"sales_account": args})

        elif name == "freshsales_update_account":
            return await client.put(f"/sales_accounts/{args['account_id']}", body={"sales_account": args["updates"]})

        elif name == "freshsales_upsert_account":
            return await client.post("/sales_accounts/upsert", body={
                "sales_account": args["sales_account"],
                "unique_identifier": args["unique_identifier"],
            })

        elif name == "freshsales_delete_account":
            return await client.delete(f"/sales_accounts/{args['account_id']}")

        elif name == "freshsales_clone_account":
            return await client.post(f"/sales_accounts/{args['account_id']}/clone", body={})

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
