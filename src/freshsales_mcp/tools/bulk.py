import json
from mcp.types import Tool
from ..client import FreshsalesClient

def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_bulk_upsert_contacts",
            description="Creates or updates multiple contacts in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contacts": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["contacts"],
            },
        ),
        Tool(
            name="freshsales_bulk_assign_contact_owner",
            description="Assigns an owner to multiple contacts at once.",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner_id": {"type": "integer"},
                    "contact_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["owner_id", "contact_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_delete_contacts",
            description="Deletes multiple contacts at once.",
            inputSchema={
                "type": "object",
                "properties": {
                    "contact_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["contact_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_upsert_accounts",
            description="Creates or updates multiple sales accounts in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sales_accounts": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["sales_accounts"],
            },
        ),
        Tool(
            name="freshsales_bulk_delete_accounts",
            description="Deletes multiple sales accounts at once.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sales_account_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["sales_account_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_upsert_deals",
            description="Creates or updates multiple deals in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deals": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["deals"],
            },
        ),
        Tool(
            name="freshsales_bulk_delete_deals",
            description="Deletes multiple deals at once.",
            inputSchema={
                "type": "object",
                "properties": {
                    "deal_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["deal_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_update_documents",
            description="Updates multiple CPQ documents in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "documents": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["documents"],
            },
        ),
        Tool(
            name="freshsales_bulk_assign_document_owner",
            description="Assigns an owner to multiple CPQ documents in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner_id": {"type": "integer"},
                    "document_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["owner_id", "document_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_delete_documents",
            description="Deletes multiple CPQ documents in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["document_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_restore_documents",
            description="Restores multiple deleted CPQ documents in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["document_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_update_products",
            description="Updates multiple products in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "products": {"type": "array", "items": {"type": "object"}}
                },
                "required": ["products"],
            },
        ),
        Tool(
            name="freshsales_bulk_assign_product_owner",
            description="Assigns an owner to multiple products in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "owner_id": {"type": "integer"},
                    "product_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["owner_id", "product_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_delete_products",
            description="Deletes multiple products in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["product_ids"],
            },
        ),
        Tool(
            name="freshsales_bulk_restore_products",
            description="Restores multiple deleted products in bulk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_ids": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["product_ids"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        # Standard Freshsales bulk ops often use `/bulk` or similar endpoints.
        # This is a generic implementation.
        
        if name == "freshsales_bulk_upsert_contacts":
            return await client.post("/contacts/bulk/upsert", body={"contacts": args["contacts"]})
        
        elif name == "freshsales_bulk_assign_contact_owner":
            return await client.post("/contacts/bulk/assign", body={"owner_id": args["owner_id"], "contact_ids": args["contact_ids"]})
            
        elif name == "freshsales_bulk_delete_contacts":
            return await client.post("/contacts/bulk/delete", body={"contact_ids": args["contact_ids"]})

        elif name == "freshsales_bulk_upsert_accounts":
            return await client.post("/sales_accounts/bulk/upsert", body={"sales_accounts": args["sales_accounts"]})

        elif name == "freshsales_bulk_delete_accounts":
            return await client.post("/sales_accounts/bulk/delete", body={"sales_account_ids": args["sales_account_ids"]})

        elif name == "freshsales_bulk_upsert_deals":
            return await client.post("/deals/bulk/upsert", body={"deals": args["deals"]})

        elif name == "freshsales_bulk_delete_deals":
            return await client.post("/deals/bulk/delete", body={"deal_ids": args["deal_ids"]})
            
        elif name == "freshsales_bulk_update_documents":
            return await client.post("/cpq/documents/bulk/update", body={"documents": args["documents"]})
            
        elif name == "freshsales_bulk_assign_document_owner":
            return await client.post("/cpq/documents/bulk/assign", body={"owner_id": args["owner_id"], "document_ids": args["document_ids"]})

        elif name == "freshsales_bulk_delete_documents":
            return await client.post("/cpq/documents/bulk/delete", body={"document_ids": args["document_ids"]})

        elif name == "freshsales_bulk_restore_documents":
            return await client.post("/cpq/documents/bulk/restore", body={"document_ids": args["document_ids"]})

        elif name == "freshsales_bulk_update_products":
            return await client.post("/products/bulk/update", body={"products": args["products"]})

        elif name == "freshsales_bulk_assign_product_owner":
            return await client.post("/products/bulk/assign", body={"owner_id": args["owner_id"], "product_ids": args["product_ids"]})

        elif name == "freshsales_bulk_delete_products":
            return await client.post("/products/bulk/delete", body={"product_ids": args["product_ids"]})

        elif name == "freshsales_bulk_restore_products":
            return await client.post("/products/bulk/restore", body={"product_ids": args["product_ids"]})

        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
