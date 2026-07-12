import json
from mcp.types import Tool
from ..client import FreshsalesClient

def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_create_list",
            description="Creates a new marketing list in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The name of the list"}
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="freshsales_list_lists",
            description="Lists all marketing lists in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "default": 1}
                },
            },
        ),
        Tool(
            name="freshsales_update_list",
            description="Updates the name of a marketing list in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_id": {"type": "integer"},
                    "name": {"type": "string"}
                },
                "required": ["list_id", "name"],
            },
        ),
        Tool(
            name="freshsales_add_contacts_to_list",
            description="Adds contacts to a marketing list in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_id": {"type": "integer"},
                    "contact_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["list_id", "contact_ids"],
            },
        ),
        Tool(
            name="freshsales_list_contacts_in_list",
            description="Lists all contacts belonging to a specific marketing list.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_id": {"type": "integer"},
                    "page": {"type": "integer", "default": 1}
                },
                "required": ["list_id"],
            },
        ),
        Tool(
            name="freshsales_move_contacts_between_lists",
            description="Moves contacts from one marketing list to another.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_list_id": {"type": "integer"},
                    "destination_list_id": {"type": "integer"},
                    "contact_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["source_list_id", "destination_list_id", "contact_ids"],
            },
        ),
        Tool(
            name="freshsales_remove_contacts_from_list",
            description="Removes contacts from a marketing list.",
            inputSchema={
                "type": "object",
                "properties": {
                    "list_id": {"type": "integer"},
                    "contact_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["list_id", "contact_ids"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_create_list":
            return await client.post("/lists", body={"list": {"name": args["name"]}})
        
        elif name == "freshsales_list_lists":
            return await client.get("/lists", params={"page": args.get("page", 1)})
        
        elif name == "freshsales_update_list":
            return await client.put(f"/lists/{args['list_id']}", body={"list": {"name": args["name"]}})
        
        elif name == "freshsales_add_contacts_to_list":
            return await client.post(f"/lists/{args['list_id']}/contacts", body={"contact_ids": args["contact_ids"]})

        elif name == "freshsales_list_contacts_in_list":
            return await client.get(f"/lists/{args['list_id']}/contacts", params={"page": args.get("page", 1)})

        elif name == "freshsales_move_contacts_between_lists":
            return await client.post(f"/lists/{args['source_list_id']}/move", body={
                "destination_list_id": args["destination_list_id"],
                "contact_ids": args["contact_ids"]
            })

        elif name == "freshsales_remove_contacts_from_list":
            return await client.delete(f"/lists/{args['list_id']}/contacts", params={"contact_ids": ",".join(map(str, args["contact_ids"]))})

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
