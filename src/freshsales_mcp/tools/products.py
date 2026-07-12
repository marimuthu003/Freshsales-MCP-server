import json
from mcp.types import Tool
from ..client import FreshsalesClient

def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_create_product",
            description="Creates a new product in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {"type": "object", "description": "The product payload"}
                },
                "required": ["product"],
            },
        ),
        Tool(
            name="freshsales_get_product",
            description="Retrieves a product by ID from Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "include": {"type": "string", "description": "Embed related entities"}
                },
                "required": ["product_id"],
            },
        ),
        Tool(
            name="freshsales_update_product",
            description="Updates an existing product in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "updates": {"type": "object"}
                },
                "required": ["product_id", "updates"],
            },
        ),
        Tool(
            name="freshsales_delete_product",
            description="Deletes a product by ID from Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"}
                },
                "required": ["product_id"],
            },
        ),
        Tool(
            name="freshsales_manage_product_prices",
            description="Adds, updates, or removes prices for a product in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer"},
                    "prices": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["product_id", "prices"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_create_product":
            return await client.post("/products", body={"product": args["product"]})
        
        elif name == "freshsales_get_product":
            params = {}
            if "include" in args:
                params["include"] = args["include"]
            return await client.get(f"/products/{args['product_id']}", params=params)
        
        elif name == "freshsales_update_product":
            return await client.put(f"/products/{args['product_id']}", body={"product": args["updates"]})
        
        elif name == "freshsales_delete_product":
            return await client.delete(f"/products/{args['product_id']}")

        elif name == "freshsales_manage_product_prices":
            return await client.put(f"/products/{args['product_id']}/prices", body={"prices": args["prices"]})

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
