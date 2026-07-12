import json
import base64
from mcp.types import Tool
from ..client import FreshsalesClient

def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_create_file",
            description="Uploads and attaches a file to an entity (contact, account, deal). Note: due to MCP limits, passing binary data might be tricky, use create_file_link if possible.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {"type": "string", "enum": ["contacts", "sales_accounts", "deals"]},
                    "entity_id": {"type": "integer"},
                    "file_content_b64": {"type": "string", "description": "Base64 encoded file content"},
                    "filename": {"type": "string"}
                },
                "required": ["entity_type", "entity_id", "file_content_b64", "filename"],
            },
        ),
        Tool(
            name="freshsales_create_file_link",
            description="Attaches a file link (URL) to a contact, sales account, or deal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {"type": "string", "enum": ["contacts", "sales_accounts", "deals"]},
                    "entity_id": {"type": "integer"},
                    "link": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ["entity_type", "entity_id", "link", "name"],
            },
        ),
        Tool(
            name="freshsales_list_contact_files",
            description="Lists all files and links attached to a contact.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_id": {"type": "integer"}
                },
                "required": ["contact_id"],
            },
        ),
        Tool(
            name="freshsales_list_deal_files",
            description="Lists all files and links attached to a deal.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_id": {"type": "integer"}
                },
                "required": ["deal_id"],
            },
        ),
        Tool(
            name="freshsales_list_account_files",
            description="Lists all files and links attached to a sales account.",
            inputSchema={
                "type": "object",
                "properties": {
                    "account_id": {"type": "integer"}
                },
                "required": ["account_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_create_file":
            try:
                file_bytes = base64.b64decode(args["file_content_b64"])
            except Exception as e:
                raise ValueError(f"Failed to decode base64 file content: {e}")

            files = {
                "file": (args["filename"], file_bytes)
            }
            return await client.post_multipart(f"/{args['entity_type']}/{args['entity_id']}/files", files=files)
        
        elif name == "freshsales_create_file_link":
            # Using standard post but it might be a specific endpoint for files
            # Usually POST /api/contacts/{id}/files or something similar.
            return await client.post(f"/{args['entity_type']}/{args['entity_id']}/files", body={
                "file": {
                    "link": args["link"],
                    "name": args["name"]
                }
            })
        
        elif name == "freshsales_list_contact_files":
            return await client.get(f"/contacts/{args['contact_id']}/files")
        
        elif name == "freshsales_list_deal_files":
            return await client.get(f"/deals/{args['deal_id']}/files")

        elif name == "freshsales_list_account_files":
            return await client.get(f"/sales_accounts/{args['account_id']}/files")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
