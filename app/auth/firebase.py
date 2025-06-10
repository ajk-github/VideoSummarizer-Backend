import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Load base64-encoded JSON from env
b64_key = os.getenv("GOOGLE_CREDENTIALS_B64")
if not b64_key:
    raise ValueError("Missing GOOGLE_CREDENTIALS_B64 environment variable")

# Decode base64 to JSON string
json_str = base64.b64decode(b64_key).decode("utf-8")
service_account_info = json.loads(json_str)

# Use the credentials
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

# Firestore DB client
db = firestore.client()
