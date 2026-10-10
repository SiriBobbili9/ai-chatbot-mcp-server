AI Chatbot MCP Tool Server
A beginner-friendly Python project demonstrating FastAPI REST endpoints and FastMCP tools.
1. What this project does
This project exposes example capabilities in two ways:
- FastAPI REST API: HTTP routes that a browser, frontend, or API client such as Bruno can call.
- FastMCP server: tools that a compatible MCP client can discover and invoke through the Model Context Protocol.
Example capabilities:
- calculate_total_tool: calculates price * quantity.
- get_server_status_tool: returns sample status information for a service.
get_server_status_tool returns mock data; it does not actually check a live service.

2. Prerequisites
Install these on Windows:
1. Python 3.12: https://www.python.org/downloads/windows/ — enable Add python.exe to PATH during installation.
2. Visual Studio Code: https://code.visualstudio.com/download
3. uv: https://docs.astral.sh/uv/getting-started/installation/
4. Optional, for API testing: Bruno: https://www.usebruno.com/downloads
After installing, open a new PowerShell window and check:
python --version
pip --version
uv --version
3. Create the project on Windows
Open PowerShell and run these commands one at a time:
mkdir ai-chatbot-mcp-server
cd ai-chatbot-mcp-server

uv init --bare
uv python pin 3.12
uv add fastapi "uvicorn[standard]" fastmcp

mkdir app
mkdir app\services
mkdir tests

New-Item app\__init__.py -ItemType File
New-Item app\main.py -ItemType File
New-Item app\mcp_server.py -ItemType File
New-Item app\services\__init__.py -ItemType File
New-Item app\services\tools.py -ItemType File
If a file already exists, PowerShell may report that it exists; keep the existing file.
What the setup commands mean
- mkdir ai-chatbot-mcp-server: creates the project folder.
- cd ai-chatbot-mcp-server: changes the terminal's current folder to the project folder.
- uv init --bare: initializes a minimal Python project without generating the usual starter source files. It creates project configuration such as pyproject.toml.
- uv python pin 3.12: records Python 3.12 as the preferred project version in .python-version. Pinning does not necessarily install Python by itself; uv can locate or install it when needed.
- uv add fastapi "uvicorn[standard]" fastmcp: adds the dependencies to the project and resolves/installs them. The quotes keep the optional-dependency syntax together in shells where square brackets have special meaning. standard installs Uvicorn's recommended extras, including support useful for development.
- mkdir app, mkdir app\services, mkdir tests: creates folders for application code, reusable service logic, and automated tests.
- New-Item ... -ItemType File: creates an empty file in PowerShell. touch is the common equivalent in macOS/Linux shells, but it is not a standard PowerShell command.
- __init__.py: marks a directory as a Python package; it can be empty.
- main.py: contains the FastAPI app and REST routes.
- mcp_server.py: registers and runs FastMCP tools.
- tools.py: contains reusable Python business logic.
- pyproject.toml: stores project metadata and dependency declarations.
- uv.lock: records resolved dependency versions for repeatable installs.
4. Project structure
ai-chatbot-mcp-server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── mcp_server.py
│   └── services/
│       ├── __init__.py
│       └── tools.py
├── tests/
├── .python-version
├── pyproject.toml
└── uv.lock
5. Add the business logic
Put this in app/services/tools.py:
def calculate_total(price: float, quantity: int) -> dict:
    """Calculate the total price for a given quantity."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")

    return {
        "price": price,
        "quantity": quantity,
        "total": round(price * quantity, 2),
    }


def get_server_status(service_name: str) -> dict:
    """Return sample status information for a service."""
    return {
        "service": service_name,
        "status": "healthy",
        "message": f"{service_name} is running",
    }
6. Add FastAPI REST routes
Put this in app/main.py:
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.services.tools import calculate_total, get_server_status

app = FastAPI(title="AI Chatbot Tool Server", version="1.0.0")


class CalculateRequest(BaseModel):
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)


@app.get("/")
async def home():
    return {"message": "AI Chatbot Tool Server is running"}


@app.post("/calculate")
async def calculate(request: CalculateRequest):
    return calculate_total(request.price, request.quantity)


@app.get("/server-status/{service_name}")
async def server_status(service_name: str):
    return get_server_status(service_name)
Run the REST API
From the project root (the directory containing pyproject.toml), run:
uv run uvicorn app.main:app --reload
Keep this terminal open. --reload restarts the development server when code changes.
REST URLs
- Home route: http://127.0.0.1:8000/
- Swagger interactive docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Example status route: http://127.0.0.1:8000/server-status/inventory
Test POST /calculate
In http://127.0.0.1:8000/docs:
1. Expand POST /calculate.
2. Click Try it out.
3. Enter:
{
  "price": 100,
  "quantity": 3
}
4. Click Execute.
Expected response:
{
  "price": 100.0,
  "quantity": 3,
  "total": 300.0
}
Negative price or quantity values are rejected by Pydantic validation.
Test with Bruno (optional)
Create a Bruno request:
- Method: POST
- URL: http://127.0.0.1:8000/calculate
- Body type: JSON
- Body: {"price": 100, "quantity": 3}
You can also send GET http://127.0.0.1:8000/server-status/inventory.
7. Add FastMCP tools
Put this in app/mcp_server.py:
from fastmcp import FastMCP

from app.services.tools import calculate_total, get_server_status

mcp = FastMCP("AI Chatbot Tool Server")


@mcp.tool()
def calculate_total_tool(price: float, quantity: int) -> dict:
    """Calculate the total price for a given quantity."""
    return calculate_total(price, quantity)


@mcp.tool()
def get_server_status_tool(service_name: str) -> dict:
    """Get sample status information for a service."""
    return get_server_status(service_name)


if __name__ == "__main__":
    mcp.run()
What does @mcp.tool() do?
It registers a Python function as an MCP tool. FastMCP uses the function name, type hints, and docstring to construct its tool definition and input schema. An MCP client can discover the tool and invoke it with the required arguments.
Run MCP with stdio transport
From the project root, run:
uv run python -m app.mcp_server
The default stdio transport communicates through standard input/output for a compatible MCP client. It does not create a browser URL. Keep the process running while the client uses it. Stop it with Ctrl+C.
8. Inspect MCP tools
FastMCP versions may expose different CLI options. Try the Inspector development command supported by your installed version:
uv run fastmcp dev inspector app/mcp_server.py
Open the URL printed in the terminal and connect to the server. The Inspector should let you view tool names, descriptions, input schemas, and invoke tools. If the command is not available, consult the current CLI docs: https://gofastmcp.com/
9. Optional: expose MCP over HTTP
To use HTTP transport, replace the bottom of app/mcp_server.py with:
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8001,
    )
Then run:
uv run python -m app.mcp_server
The MCP endpoint is typically http://127.0.0.1:8001/mcp for this configuration. This is an MCP protocol endpoint, not a normal webpage; use an MCP client or Inspector to discover and invoke tools. Keep FastAPI on port 8000 and MCP HTTP on port 8001 to avoid a port conflict.
10. Run both servers
Open two PowerShell windows and change both to the project root.
Terminal 1 — FastAPI:
uv run uvicorn app.main:app --reload
Terminal 2 — FastMCP:
uv run python -m app.mcp_server
Use stdio when launching through an MCP client, or use the HTTP configuration above when an HTTP MCP endpoint is needed.
11. Troubleshooting
python is not recognized
Open a new PowerShell window. If it still fails, rerun the Python installer and enable Add python.exe to PATH.
uv is not recognized
Close and reopen PowerShell, then check the uv installation and PATH using the official guide: https://docs.astral.sh/uv/getting-started/installation/
Could not import module "app.main"
Make sure the terminal is in the project root and app\main.py exists. Run:
Get-Location
Get-ChildItem
The output should include app, pyproject.toml, and uv.lock.
Port 8000 is already in use
Use another port:
uv run uvicorn app.main:app --reload --port 8002
MCP starts but no URL appears
This is expected for stdio transport. Use an MCP client/Inspector, or configure HTTP transport as described in section 9.
12. Engineer quick reference
Task	Command or URL
Install/sync dependencies	uv sync
Run REST API	uv run uvicorn app.main:app --reload
Swagger docs	http://127.0.0.1:8000/docs
Home route	http://127.0.0.1:8000/
Example status route	http://127.0.0.1:8000/server-status/inventory
Run stdio MCP server	uv run python -m app.mcp_server
Try Inspector command	uv run fastmcp dev inspector app/mcp_server.py
Stop a process	Ctrl+C


13. Suggested improvements
1. Add pytest tests and FastAPI TestClient tests.
2. Store real incident/service data in SQLite or PostgreSQL.
3. Add structured logging and consistent error responses.
4. Add authentication and authorization before exposing APIs outside localhost.
5. Connect a real MCP client and later an LLM.
6. Add .gitignore and .env.example; never commit real API keys or secrets.
Key distinction
FastAPI routes are HTTP endpoints called directly by HTTP clients. MCP tools are capabilities exposed through the MCP protocol and discovered/invoked by MCP clients. A REST endpoint that lists tool metadata is not the same as an MCP client discovering tools through the protocol.