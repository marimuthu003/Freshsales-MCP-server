import json
from mcp.types import Tool
from ..client import FreshsalesClient

def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_create_document",
            description="Creates a new CPQ document in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document": {"type": "object", "description": "The document payload"}
                },
                "required": ["document"],
            },
        ),
        Tool(
            name="freshsales_get_document",
            description="Retrieves a CPQ document by ID from Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "integer"},
                    "include": {"type": "string", "description": "Embed related entities"}
                },
                "required": ["document_id"],
            },
        ),
        Tool(
            name="freshsales_update_document",
            description="Updates an existing CPQ document in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "integer"},
                    "updates": {"type": "object"}
                },
                "required": ["document_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_delete_document",
            description="Deletes a CPQ document by ID from Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "integer"}
                },
                "required": ["document_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_create_document":
            return await client.post("/cpq/documents", body={"document": args["document"]})
        
        elif name == "freshsales_get_document":
            params = {}
            if "include" in args:
                params["include"] = args["include"]
            return await client.get(f"/cpq/documents/{args['document_id']}", params=params)
        
        elif name == "freshsales_update_document":
            return await client.put(f"/cpq/documents/{args['document_id']}", body={"document": args["updates"]})
        
        elif name == "freshsales_delete_document":
            return await client.delete(f"/cpq/documents/{args['document_id']}")

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
