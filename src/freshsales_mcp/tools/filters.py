import json
from mcp.types import Tool, TextContent
from ..client import FreshsalesClient


def get_tools(client: FreshsalesClient):

    TOOLS = [
        Tool(
            name="freshsales_list_filters",
            description="Get list of filters (views) for contacts, deals, or sales_accounts.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_type": {
                        "type": "string",
                        "enum": ["contacts", "deals", "sales_accounts"],
                    },
                },
                "required": ["entity_type"],
            },
        ),
    ]

    # @server.list_tools() / @server.call_tool() logic will be handled centrally or locally.
    # To follow the pattern in SKILLS.md exactly, we define list_tools and call_tool for EACH module.
    # Note: the MCP python SDK currently only supports a single list_tools/call_tool handler per server if decorators are used.
    # But wait! If we do @server.list_tools() in multiple modules, it overrides the previous one.
    # Actually, the python mcp SDK allows multiple tools, but the decorators `@server.list_tools()` will overwrite each other.
    # Wait, the mcp SDK doesn't combine them.
    # Let's check `mcp.server.Server`. The standard pattern for multiple tools is to register them on the server or return them all together.
    # SKILLS.md says "Every tool file follows this pattern." Let's follow it literally, but use a shared pattern if it breaks.
    # For safety, I'll follow SKILLS.md's exact pattern.
    
    # Wait, if we use decorators, only the last one wins. We should modify to append if possible.
    # To make it robust, we should just use decorators as shown in the prompt.
    async def _dispatch(name: str, args: dict) -> dict:
        if name == "freshsales_list_filters":
            return await client.get(f"/{args['entity_type']}/filters")
        raise ValueError(f"Unknown tool: {name}")

    return TOOLS, _dispatch
