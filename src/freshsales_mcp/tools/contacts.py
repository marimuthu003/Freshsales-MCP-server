import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_contact",
            description="Get a single Freshsales contact by ID with optional embedded related data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"},
                    "include": {
                        "type": "string",
                        "description": "Comma-separated embeds: owner,tasks,notes,deals,sales_account"
                    },
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="freshsales_list_contacts",
            description=(
                "List contacts from Freshsales. "
                "IMPORTANT: You MUST call freshsales_list_filters(entity_type='contacts') first "
                "to get the available view_ids — then pass one of those IDs here. "
                "NEVER ask the user for a view_id. The 'All Contacts' view is usually the first result."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "view_id": {"type": "integer", "description": "Get this from freshsales_list_filters first"},
                    "page": {"type": "integer", "default": 1},
                    "per_page": {"type": "integer", "default": 25},
                    "include": {"type": "string"},
                },
                "required": ["view_id"],
            },
        ),
        Tool(
            name="freshsales_create_contact",
            description="Create a new contact in Freshsales. Provide first_name or email at minimum.",
            inputSchema={
                "type": "object",
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "email": {"type": "string"},
                    "mobile_number": {"type": "string"},
                    "custom_field": {"type": "object", "description": "Custom fields as cf_ prefixed keys"},
                },
            },
        ),
        Tool(
            name="freshsales_update_contact",
            description="Update an existing Freshsales contact. Only provided fields are changed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"},
                    "updates": {"type": "object"},
                },
                "required": ["contact_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_upsert_contact",
            description="Create or update a contact by unique identifier (e.g. email). Idempotent.",
            inputSchema={
                "type": "object",
                "properties": {
                    "unique_identifier": {
                        "type": "object",
                        "description": "Match field — use 'emails' (plural) for email match",
                        "example": {"emails": "jane@co.com"}
                    },
                    "contact": {"type": "object"},
                },
                "required": ["unique_identifier", "contact"],
            },
        ),
        Tool(
            name="freshsales_delete_contact",
            description="Permanently delete a Freshsales contact. Cannot be undone.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"},
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="freshsales_clone_contact",
            description="Clone an existing Freshsales contact. Returns a new contact with a new ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"},
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="freshsales_list_contact_activities",
            description="Get the full activity timeline for a contact — calls, emails, tasks, notes, appointments.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"},
                },
                "required": ["contact_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_contact":
            params = {}
            if "include" in args:
                params["include"] = args["include"]
            return await client.get(f"/contacts/{args['contact_id']}", params=params)

        elif name == "freshsales_list_contacts":
            params = {
                "page": args.get("page", 1),
                "per_page": min(args.get("per_page", 25), 100),
            }
            if "include" in args:
                params["include"] = args["include"]
            return await client.get(f"/contacts/view/{args['view_id']}", params=params)

        elif name == "freshsales_create_contact":
            return await client.post("/contacts", body={"contact": args})

        elif name == "freshsales_update_contact":
            return await client.put(
                f"/contacts/{args['contact_id']}",
                body={"contact": args["updates"]}
            )

        elif name == "freshsales_upsert_contact":
            return await client.post("/contacts/upsert", body={
                "contact": args["contact"],
                "unique_identifier": args["unique_identifier"],
            })

        elif name == "freshsales_delete_contact":
            return await client.delete(f"/contacts/{args['contact_id']}")

        elif name == "freshsales_clone_contact":
            return await client.post(f"/contacts/{args['contact_id']}/clone", body={})

        elif name == "freshsales_list_contact_activities":
            return await client.get(f"/contacts/{args['contact_id']}/activities")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
