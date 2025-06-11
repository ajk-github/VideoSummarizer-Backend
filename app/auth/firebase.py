import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.config import settings

# Decode the base64-encoded Google credentials
json_str = base64.b64decode(settings.google_credentials_b64).decode("utf-8")
service_account_info = json.loads(json_str)

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)

db = firestore.client()
