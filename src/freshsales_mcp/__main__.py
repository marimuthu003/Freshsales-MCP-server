import os
import sys
import asyncio
import argparse
import uvicorn
from dotenv import load_dotenv, find_dotenv
from .server import create_sse_app, create_streamable_http_app, run_stdio_server

load_dotenv(find_dotenv())

def main():
    parser = argparse.ArgumentParser(description="Freshsales MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport mode: stdio (default, for AI clients), sse (legacy web), streamable-http (modern web)",
    )
    args, _ = parser.parse_known_args()

    api_key = os.environ.get("FRESHSALES_API_KEY")
    domain = os.environ.get("FRESHSALES_DOMAIN")

    if not api_key or not domain:
        print("Missing FRESHSALES_API_KEY or FRESHSALES_DOMAIN", file=sys.stderr)
        sys.exit(1)

    transport = args.transport
    # Also check env var for backward compatibility
    if os.environ.get("TRANSPORT"):
        transport = os.environ["TRANSPORT"]

    if transport == "stdio":
        asyncio.run(run_stdio_server(api_key=api_key, domain=domain))
    elif transport == "sse":
        app = create_sse_app(api_key=api_key, domain=domain)
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
            log_level="info",
        )
    elif transport == "streamable-http":
        app = create_streamable_http_app(api_key=api_key, domain=domain)
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
            log_level="info",
        )

if __name__ == "__main__":
    main()
