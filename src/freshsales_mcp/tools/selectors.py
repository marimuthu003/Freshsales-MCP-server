import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_get_selectors",
            description="Get predefined selectors like owners, deal_stages, territories, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "selector_type": {
                        "type": "string",
                        "enum": ["owners", "deal_stages", "lead_sources", "territories", "currencies", "lifecycle_stages", "contact_statuses", "deal_reasons", "industry_types", "business_types", "deal_pipelines", "campaigns", "deal_payment_statuses", "activity_types", "activity_outcomes", "activity_entity_types", "designations"],
                    },
                },
                "required": ["selector_type"],
            },
        ),
        Tool(
            name="freshsales_list_outcomes_for_activity_type",
            description="Lists all outcomes for a specific sales activity type in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sales_activity_type_id": {"type": "integer"}
                },
                "required": ["sales_activity_type_id"],
            },
        ),
        Tool(
            name="freshsales_list_deal_stages_for_pipeline",
            description="Lists all deal stages for a specific pipeline in Freshsales.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pipeline_id": {"type": "integer"}
                },
                "required": ["pipeline_id"],
            },
        ),
    ]

    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_get_selectors":
            return await client.get(f"/selector/{args['selector_type']}")
            
        elif name == "freshsales_list_outcomes_for_activity_type":
            return await client.get(f"/sales_activities/types/{args['sales_activity_type_id']}/outcomes")

        elif name == "freshsales_list_deal_stages_for_pipeline":
            return await client.get(f"/deal_pipelines/{args['pipeline_id']}/deal_stages")
        
        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
