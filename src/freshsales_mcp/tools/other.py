import json
from mcp.types import Tool
from ..client import FreshsalesClient

def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_job_status",
            description="Retrieves the status and details of a background job in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string"}
                },
                "required": ["job_id"],
            },
        ),
        Tool(
            name="freshsales_filtered_search_contact",
            description="Searches for contacts matching exact filter criteria in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter_rule": {"type": "object", "description": "The exact filter criteria"}
                },
                "required": ["filter_rule"],
            },
        ),
        Tool(
            name="freshsales_manage_contact_team_members",
            description="Adds or removes team members associated with a contact in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"},
                    "team_member_ids": {"type": "array", "items": {"type": "integer"}},
                    "action": {"type": "string", "enum": ["add", "remove"]}
                },
                "required": ["contact_id", "team_member_ids", "action"],
            },
        ),
        Tool(
            name="freshsales_manage_account_team_members",
            description="Adds or removes team members associated with a sales account in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"},
                    "team_member_ids": {"type": "array", "items": {"type": "integer"}},
                    "action": {"type": "string", "enum": ["add", "remove"]}
                },
                "required": ["account_id", "team_member_ids", "action"],
            },
        ),
        Tool(
            name="freshsales_manage_deal_team_members",
            description="Adds or removes team members associated with a deal in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"},
                    "team_member_ids": {"type": "array", "items": {"type": "integer"}},
                    "action": {"type": "string", "enum": ["add", "remove"]}
                },
                "required": ["deal_id", "team_member_ids", "action"],
            },
        ),
        Tool(
            name="freshsales_forget_contact",
            description="Permanently and irreversibly deletes all data for a contact (Hard Delete).",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"}
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="freshsales_forget_account",
            description="Permanently and irreversibly deletes all data for a sales account (Hard Delete).",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"}
                },
                "required": ["account_id"],
            },
        ),
        Tool(
            name="freshsales_forget_deal",
            description="Permanently and irreversibly deletes all data for a deal (Hard Delete).",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"}
                },
                "required": ["deal_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_job_status":
            return await client.get(f"/jobs/{args['job_id']}")
        
        elif name == "freshsales_filtered_search_contact":
            return await client.post("/contacts/filters", body={"filter_rule": args["filter_rule"]})
            
        elif name == "freshsales_manage_contact_team_members":
            method = client.post if args["action"] == "add" else client.delete
            return await method(f"/contacts/{args['contact_id']}/team_members", body={"team_member_ids": args["team_member_ids"]} if args["action"] == "add" else None)

        elif name == "freshsales_manage_account_team_members":
            method = client.post if args["action"] == "add" else client.delete
            return await method(f"/sales_accounts/{args['account_id']}/team_members", body={"team_member_ids": args["team_member_ids"]} if args["action"] == "add" else None)

        elif name == "freshsales_manage_deal_team_members":
            method = client.post if args["action"] == "add" else client.delete
            return await method(f"/deals/{args['deal_id']}/team_members", body={"team_member_ids": args["team_member_ids"]} if args["action"] == "add" else None)

        elif name == "freshsales_forget_contact":
            return await client.delete(f"/contacts/{args['contact_id']}/forget")

        elif name == "freshsales_forget_account":
            return await client.delete(f"/sales_accounts/{args['account_id']}/forget")

        elif name == "freshsales_forget_deal":
            return await client.delete(f"/deals/{args['deal_id']}/forget")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
