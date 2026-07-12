import contextlib
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
import mcp.server.stdio
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

from .client import FreshsalesClient
from .tools.registry import register_all_tools


def _create_base_server(api_key: str, domain: str) -> Server:
    server = Server("freshsales-mcp")
    client = FreshsalesClient(api_key=api_key, domain=domain)
    register_all_tools(server, client)
    return server


# ── SSE Transport (legacy) ────────────────────────────────────────────
def create_sse_app(api_key: str, domain: str) -> Starlette:
    server = _create_base_server(api_key, domain)
    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await server.run(
                streams[0], streams[1],
                server.create_initialization_options()
            )

    async def health(request):
        return JSONResponse({"status": "ok", "server": "freshsales-mcp", "transport": "sse"})

    return Starlette(routes=[
        Route("/mcp", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
        Route("/health", endpoint=health),
    ])


# ── Streamable HTTP Transport (modern, recommended) ───────────────────
def create_streamable_http_app(api_key: str, domain: str) -> Starlette:
    server = _create_base_server(api_key, domain)
    session_manager = StreamableHTTPSessionManager(
        app=server,
        json_response=False,
        stateless=False,
    )

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette):
        async with session_manager.run():
            yield

    async def health(request):
        return JSONResponse({"status": "ok", "server": "freshsales-mcp", "transport": "streamable-http"})

    return Starlette(
        routes=[
            Mount("/mcp", app=session_manager.handle_request),
            Route("/health", endpoint=health),
        ],
        lifespan=lifespan,
    )


# ── Backward compatibility alias ──────────────────────────────────────
create_app = create_streamable_http_app


# ── stdio Transport ──────────────────────────────────────────────────
async def run_stdio_server(api_key: str, domain: str):
    server = _create_base_server(api_key, domain)
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream,
            server.create_initialization_options()
        )
