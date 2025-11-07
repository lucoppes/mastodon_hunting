from pycti import OpenCTIApiClient
import json

# stix_json = '''
# {
#     "type": "bundle",
#     "id": "bundle--12345678-1234-5678-1234-567812345678",
#     "objects": [
#         {
#             "type": "indicator",
#             "spec_version": "2.1",
#             "id": "indicator--87654321-4321-8765-4321-876543218765",
#             "created": "2023-01-01T12:00:00.000Z",
#             "modified": "2023-01-01T12:00:00.000Z",
#             "name": "Test Indicator",
#             "description": "This is a test indicator",
#             "pattern": "[file:hashes.'SHA-256' = 'd41d8cd98f00b204e9800998ecf8427e']",
#             "pattern_type": "stix",
#             "valid_from": "2023-01-01T12:00:00.000Z"
#         }
#     ]
# }
# '''

# stix_json = '''
# {
#   "type": "bundle",
#   "id": "bundle--2c6a0c20-a7d5-4a5c-8d1e-2b3f4a5c6d7e",
#   "spec_version": "2.1",
#   "objects": [
#     {
#       "type": "identity",
#       "spec_version": "2.1",
#       "id": "identity--8c73456c-7e61-4191-9e8a-0d8677c7f763",
#       "created": "2025-08-12T00:00:05.421Z",
#       "modified": "2025-08-12T00:00:05.421Z",
#       "name": "Security Analyst Agent",
#       "identity_class": "system",
#       "description": "Automated system performing security analysis."
#     },
#     {
#       "type": "marking-definition",
#       "spec_version": "2.1",
#       "id": "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
#       "created": "2014-04-07T20:00:00.000Z",
#       "definition_type": "tlp",
#       "definition": {
#         "tlp": "white"
#       }
#     },
#     {
#       "type": "indicator",
#       "spec_version": "2.1",
#       "id": "indicator--e8f9d0c1-b2a3-4b5c-6d7e-8f9a0b1c2d3e",
#       "created": "2023-10-27T11:35:00.000Z",
#       "modified": "2023-10-27T11:35:00.000Z",
#       "pattern": "[ipv4-addr:value = '39.101.74.162']",
#       "pattern_type": "stix",
#       "valid_from": "2023-10-27T11:35:00.000Z",
#       "indicator_types": ["malicious-activity"],
#       "name": "Cobalt Strike Beacon IP",
#       "description": "Observed IP address associated with a Cobalt Strike Beacon.",
#       "marking_ref": "marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9",
#       "object_refs": ["ipv4-addr--a7b8c9d0-e1f2-3a4b-5c6d-7e8f9a0b1c2d"]
#     },
#     {
#       "type": "ipv4-addr",
#       "spec_version": "2.1",
#       "id": "ipv4-addr--a7b8c9d0-e1f2-3a4b-5c6d-7e8f9a0b1c2d",
#       "value": "39.101.74.162"
#     }
#   ]
# }
# '''

stix_json = "{\n  \"type\": \"bundle\",\n  \"id\": \"bundle--2c6a0c20-a7d5-4a5c-8d1e-2b3f4a5c6d7e\",\n  \"spec_version\": \"2.1\",\n  \"objects\": [\n    {\n      \"type\": \"identity\",\n      \"spec_version\": \"2.1\",\n      \"id\": \"identity--8c73456c-7e61-4191-9e8a-0d8677c7f763\",\n      \"created\": \"2025-08-12T00:00:05.421Z\",\n      \"modified\": \"2025-08-12T00:00:05.421Z\",\n      \"name\": \"Security Analyst Agent\",\n      \"identity_class\": \"system\",\n      \"description\": \"Automated system performing security analysis.\"\n    },\n    {\n      \"type\": \"marking-definition\",\n      \"spec_version\": \"2.1\",\n      \"id\": \"marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9\",\n      \"created\": \"2014-04-07T20:00:00.000Z\",\n      \"definition_type\": \"tlp\",\n      \"definition\": {\n        \"tlp\": \"white\"\n      }\n    },\n    {\n      \"type\": \"indicator\",\n      \"spec_version\": \"2.1\",\n      \"id\": \"indicator--e8f9d0c1-b2a3-4b5c-6d7e-8f9a0b1c2d3e\",\n      \"created\": \"2023-10-27T11:35:00.000Z\",\n      \"modified\": \"2023-10-27T11:35:00.000Z\",\n      \"pattern\": \"[ipv4-addr:value = '39.101.74.162']\",\n      \"pattern_type\": \"stix\",\n      \"valid_from\": \"2023-10-27T11:35:00.000Z\",\n      \"indicator_types\": [\"malicious-activity\"],\n      \"name\": \"Cobalt Strike Beacon IP\",\n      \"description\": \"Observed IP address associated with a Cobalt Strike Beacon.\",\n      \"marking_ref\": \"marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9\",\n      \"object_refs\": [\"ipv4-addr--a7b8c9d0-e1f2-3a4b-5c6d-7e8f9a0b1c2d\"]\n    },\n    {\n      \"type\": \"ipv4-addr\",\n      \"spec_version\": \"2.1\",\n      \"id\": \"ipv4-addr--a7b8c9d0-e1f2-3a4b-5c6d-7e8f9a0b1c2d\",\n      \"value\": \"39.101.74.162\"\n    }\n  ]\n}"

client = OpenCTIApiClient("http://opencti:8080", "3a5de77a-7a21-11f0-add4-dfa602df585b")

stix_dict = json.loads(stix_json)

try:
    result = client.stix2.import_bundle(stix_dict, update=True)  # Pass parsed dict
    print("response: " + str(result))
except Exception as e:
    print("error: " + str(e))