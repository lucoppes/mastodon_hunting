#!/usr/bin/env python3
import sys
import json
from pycti import OpenCTIApiClient

EXTRACTED_IOCS = "{\"EXTRACTED_IOCS\": {\"URLS\": [\"HTTPS://TEST-INDICATOR.OPENCTI.LOCAL\"], \"STRINGS\": [\"TEST_INDICATOR_12345\"]}}"

def load_stix_to_opencti(api_url: str, api_token: str, stix_json: str) -> dict:
    """Loads a STIX JSON bundle into OpenCTI and returns the response."""
    client = OpenCTIApiClient(api_url, api_token)

    try:
        bundle = json.loads(stix_json)
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON: {e}"}

    try:
        result = client.stix2.import_bundle(bundle=bundle, update=True)
        return {"success": True, "response": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({"success": False, "error": "Usage: script <api_url> <api_token> <stix_json>"}))
        sys.exit(1)

    api_url = sys.argv[1]
    api_token = sys.argv[2]
    stix_json = sys.argv[3]
    output = load_stix_to_opencti(api_url, api_token, stix_json)
    print(json.dumps(output))
