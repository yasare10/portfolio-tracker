import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.getenv("SORARE_JWT_TOKEN")
AUD = os.getenv("SORARE_JWT_AUD")
API_URL = "https://api.sorare.com/graphql"

if not TOKEN or not AUD:
    raise ValueError("Missing SORARE_JWT_TOKEN or SORARE_JWT_AUD in .env")

query = """
query CurrentUserQuery {
  currentUser {
    slug
    email
  }
}
"""

resp = requests.post(
    API_URL,
    json={"query": query},
    headers={
        "content-type": "application/json",
        "Authorization": f"Bearer {TOKEN}",
        "JWT-AUD": AUD,
    },
    timeout=30,
)

data = resp.json()
print(json.dumps(data, indent=2))
