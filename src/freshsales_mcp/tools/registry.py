import json
from mcp.server import Server
from mcp.types import TextContent
from ..client import FreshsalesClient

from .contacts import get_tools as get_contact_tools
from .accounts import get_tools as get_account_tools
from .deals import get_tools as get_deal_tools
from .tasks import get_tools as get_task_tools
from .notes import get_tools as get_note_tools
from .appointments import get_tools as get_appointment_tools
from .activities import get_tools as get_activity_tools
from .search import get_tools as get_search_tools
from .filters import get_tools as get_filter_tools
from .selectors import get_tools as get_selector_tools
from .fields import get_tools as get_field_tools
from .documents import get_tools as get_document_tools
from .products import get_tools as get_product_tools
from .lists import get_tools as get_list_tools
from .files import get_tools as get_file_tools
from .bulk import get_tools as get_bulk_tools
from .other import get_tools as get_other_tools


def register_all_tools(server: Server, client: FreshsalesClient):
    all_tools = []
    dispatchers = []

    # Must register filter tools first due to view_id dependencies (conceptual ordering)
    modules = [
        get_filter_tools,
        get_selector_tools,
        get_field_tools,
        get_contact_tools,
        get_account_tools,
        get_deal_tools,
        get_task_tools,
        get_note_tools,
        get_appointment_tools,
        get_activity_tools,
        get_search_tools,
        get_document_tools,
        get_product_tools,
        get_list_tools,
        get_file_tools,
        get_bulk_tools,
        get_other_tools,
    ]

    for get_module_tools in modules:
        tools, dispatcher = get_module_tools(client)
        all_tools.extend(tools)
        dispatchers.append(dispatcher)

    @server.list_tools()
    async def list_tools():
        return all_tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        try:
            for dispatch in dispatchers:
                try:
                    result = await dispatch(name, arguments)
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                except ValueError as e:
                    if str(e).startswith("Unknown tool:"):
                        continue
                    raise
            
            # If we went through all dispatchers and didn't find the tool
            return [TextContent(type="text", text=f"Error: Unknown tool {name}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
