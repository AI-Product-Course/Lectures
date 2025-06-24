from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Orders MCP-Server")


ORDER_STATUSES = {
  "b42": "lost"
}

@mcp.tool()
def get_order_status(order_id: str) -> str:
    return ORDER_STATUSES.get(order_id, "unknown")


@mcp.resource("orders://delivery/{company}")
def delivery_process_resource(company: str) -> str:
    return f"This information is about delivery process in {company}"


@mcp.prompt()
def assistant_prompt() -> str:
    return "You are a smart order assistant."


if __name__ == "__main__":
    mcp.run()