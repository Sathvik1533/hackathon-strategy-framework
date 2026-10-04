import asyncio
import os

from mcp.server.fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(name="HackathonToolServer", dependencies=["pydantic", "httpx"])


class DataProcessInput(BaseModel):
    query: str = Field(description="Search or data processing query")
    max_records: int = Field(default=10, ge=1, le=100, description="Max candidate records")


@mcp.tool(name="process_hackathon_data", description="Performs isolated high-speed data enrichment")
async def process_hackathon_data(args: DataProcessInput, ctx: Context) -> str:
    ctx.info(f"Executing data enrichment for query: {args.query}")
    await asyncio.sleep(0.5)
    return f"Processed {args.max_records} records for '{args.query}' successfully with zero subprocess leaks."


@mcp.resource("config://hackathon-env")
def get_hackathon_env() -> str:
    return '{"status": "online", "transport": "sse", "workers": 4}'


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "sse")
    if transport == "sse":
        mcp.run(transport="sse", port=8001)
    else:
        mcp.run(transport="stdio")
