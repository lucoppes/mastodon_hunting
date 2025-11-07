import requests
import json
import asyncio
from fastmcp import Client

stix = {
    "type": "bundle",
    "id": "bundle--12345678-1234-5678-1234-567812345678",
    "objects": [
        {
            "type": "indicator",
            "spec_version": "2.1",
            "id": "indicator--87654321-4321-8765-4321-876543218765",
            "created": "2023-01-01T12:00:00.000Z",
            "modified": "2023-01-01T12:00:00.000Z",
            "name": "Test Indicator",
            "description": "This is a test indicator",
            "pattern": "[file:hashes.'SHA-256' = 'd41d8cd98f00b204e9800998ecf8427e']",
            "pattern_type": "stix",
            "valid_from": "2023-01-01T12:00:00.000Z"
        }
    ]
}

mcp_url = "http://172.20.0.7:8008/mcp"
client = Client(mcp_url)

async def call_tool(name: str):
    async with client:
        api_url = "http://172.20.0.6:8080"
        api_token = "3a5de77a-7a21-11f0-add4-dfa602df585b"
        stix_bundle = {
            "type": "bundle",
            "id": "bundle--12345678-1234-5678-1234-567812345678",
            "objects": []
        }
        # stix_json = json.dumps(stix_bundle)
        stix_json = json.dumps(stix_bundle)
        payload = {
                "api_url": api_url,
                "api_token": api_token,
                "stix_json": stix_json
            }
        headers = {
            "Accept": "application/json, text/event-stream"
        }
        result = await client.call_tool("stix_importer", payload)
        print(result)

asyncio.run(call_tool("Ford"))
