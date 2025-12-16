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

query = """
query CardDealInspect {
  currentUser {
    cards(first: 20) {
      nodes {
        slug
        name
        rarityTyped
        seasonYear

        ... on Card {
          lastDeal {
            id
            createdAt
            price {
              amount
              currency
            }
            buyer { slug }
            seller { slug }
          }
        }
      }
    }
  }
}
"""
resp = requests.post(
    API_URL,
    json={"query": query},
    headers=HEADERS,
    timeout=30,
)

data = resp.json()

if "errors" in data:
    print(json.dumps(data["errors"], indent=2))
    raise SystemExit(1)

with open("card_deals_raw.json", "w") as f:
    json.dump(data, f, indent=2)

for card in data["data"]["currentUser"]["cards"]["nodes"]:
    deal = card["lastDeal"]
    if deal:
        print(
            f"{card['slug']} | "
            f"{deal['price']['amount']} {deal['price']['currency']} | "
            f"{deal['buyer']['slug']} <- {deal['seller']['slug']}"
        )
    else:
        print(f"{card['slug']} | no deal history")
