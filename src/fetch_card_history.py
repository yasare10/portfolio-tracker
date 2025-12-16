import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.getenv("SORARE_JWT_TOKEN")
AUD = os.getenv("SORARE_JWT_AUD")
API_URL = "https://api.sorare.com/graphql"

HEADERS = {
    "content-type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
    "JWT-AUD": AUD,
}

# Pick ONE card slug from cards_raw.json
CARD_SLUG = "albert-rusnak-2025-super_rare-2"

query = """
query CardInspect($slugs: [String!]!) {
  anyCards(slugs: $slugs) {
    slug
    name
    rarityTyped
    seasonYear

    ... on Card {
      tokenOwner {
        slug
      }
    }
  }
}
"""

resp = requests.post(
    API_URL,
    json={"query": query, "variables": {"slug": CARD_SLUG}},
    headers=HEADERS,
    timeout=30,
)

data = resp.json()

if "errors" in data:
    print(json.dumps(data["errors"], indent=2))
    raise SystemExit(1)

with open("card_history_raw.json", "w") as f:
    json.dump(data, f, indent=2)

print(json.dumps(data, indent=2))
