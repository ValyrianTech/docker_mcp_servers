# MCP Run Python - Local Setup

This guide explains how to run the MCP Run Python server locally without Docker.

## Prerequisites

1. Install Deno: https://deno.com/manual@v1.41.3/getting_started/installation
2. Install Python and pip
3. Install the MCP Python client: `pip install mcp-python-client`

## Running the Server

The MCP Run Python server runs using Deno and connects via stdio to your Python client.

### Test the Setup

Run the included Python script to test the connection:

```bash
python run_mcp_python.py
```

This will:
1. Start the MCP Run Python server using Deno
2. Connect to it via stdio
3. Execute a simple Python code snippet that uses NumPy
4. Display the results

## How It Works

The script uses Deno to run the MCP Run Python server, which executes Python code in a sandboxed WebAssembly environment using Pyodide. The server automatically detects and installs required dependencies.

## Troubleshooting

- Make sure Deno is properly installed and in your PATH
- The first run may take longer as it downloads and caches the Python standard library
- If you encounter permission issues, make sure the script is executable: `chmod +x run_mcp_python.py`
