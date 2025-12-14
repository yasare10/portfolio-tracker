import os
import requests
from dotenv import load_dotenv
import json

# -------------------------
# Auth & config
# -------------------------
load_dotenv()

TOKEN = os.getenv("SORARE_JWT_TOKEN")
AUD = os.getenv("SORARE_JWT_AUD")
API_URL = "https://api.sorare.com/graphql"

if not TOKEN or not AUD:
    raise ValueError("Missing auth config in .env")

HEADERS = {
    "content-type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
    "JWT-AUD": AUD,
}

# -------------------------
# Query: owned cards
# -------------------------
query = """
query MyCards {
  currentUser {
    slug
    cards(first: 100) {
      nodes {
        id
        slug
        rarityTyped
        seasonYear
        name

        ... on Card {
          player {
            displayName
          }
        }
      }
    }
  }
}
"""


resp = requests.post(API_URL, json={"query": query}, headers=HEADERS, timeout=30)
data = resp.json()

# -------------------------
# Safety checks
# -------------------------
if "errors" in data:
    print("GraphQL errors:")
    print(json.dumps(data["errors"], indent=2))
    raise SystemExit(1)

# -------------------------
# Persist raw data
# -------------------------
with open("cards_raw.json", "w") as f:
    json.dump(data, f, indent=2)

# -------------------------
# Inspect output
# -------------------------
cards = data["data"]["currentUser"]["cards"]["nodes"]

print(f"\nYou currently own {len(cards)} cards:\n")

for card in cards[:10]:
    player_name = (
        card["player"]["displayName"]
        if "player" in card and card["player"] is not None
        else "N/A"
    )

    print(
        f"{player_name} | "
        f"{card['rarityTyped']} | "
        f"Season {card['seasonYear']}"
    )

