from fastmcp import FastMCP
from pycti import OpenCTIApiClient
import json

mcp = FastMCP("OpenCTI STIX Importer")


@mcp.tool
def stix_importer(stix_json: str) -> str:
    """Load a STIX JSON string into OpenCTI."""
    print("Starting STIX import..." + str(stix_json))
    # client = OpenCTIApiClient(api_url, api_token)
    client = OpenCTIApiClient("http://opencti:8080", "3a5de77a-7a21-11f0-add4-dfa602df585b")
    # client = OpenCTIApiClient("http://172.20.0.6:8080", "3a5de77a-7a21-11f0-add4-dfa602df585b")
    stix_dict = json.loads(stix_json)
    try:
        result = client.stix2.import_bundle(stix_dict, update=True)  # Pass parsed dict
        print("response: " + str(result))
        return "Success! Imported STIX bundle."
    except Exception as e:
        print("error: " + str(e))
        return "Error: " + str(e)

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8008)