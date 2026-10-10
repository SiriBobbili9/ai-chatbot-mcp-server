
from fastmcp import FastMCP

from app.services.tools import (
    calculate_total,
    get_server_status,
)

mcp = FastMCP("AI Chatbot Tool Server")


@mcp.tool()
def calculate_total_tool(
    price: float,
    quantity: int,
) -> dict:
    """Calculate the total price for a given quantity."""
    return calculate_total(price, quantity)


@mcp.tool()
def get_server_status_tool(
    service_name: str,
) -> dict:
    """Get the current status of a service."""
    return get_server_status(service_name)


if __name__ == "__main__":
    mcp.run()
