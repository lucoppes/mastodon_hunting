import asyncio
from fastmcp import Client

client = Client("http://localhost:8008/mcp")


import json

stix_json = '''
{
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
'''

async def call_tool():
    async with client:
        result = await client.call_tool("stix_importer", {"api_url": "http://172.20.0.6:8080", "api_token": "3a5de77a-7a21-11f0-add4-dfa602df585b", "stix_json": stix_json})
        if result is not None:
            print(result)
        else:
            print("No result returned from tool.")

asyncio.run(call_tool())