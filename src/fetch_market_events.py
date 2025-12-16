import os
import requests
from dotenv import load_dotenv
import json

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

query = """
query MyDeals {
  currentUser {
    slug
    deals(first: 50) {
      nodes {
        id
        createdAt
        dealType

        cards {
          slug
          name
          rarityTyped
        }

        price {
          amount
          currency
        }

        buyer {
          slug
        }

        seller {
          slug
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
    print("GraphQL errors:")
    print(json.dumps(data["errors"], indent=2))
    raise SystemExit(1)

with open("deals_raw.json", "w") as f:
    json.dump(data, f, indent=2)

deals = data["data"]["currentUser"]["deals"]["nodes"]

print(f"\nFetched {len(deals)} deals:\n")

for deal in deals[:10]:
    card_slugs = [c["slug"] for c in deal["cards"]]
    print(
        f"{deal['createdAt']} | "
        f"{deal['dealType']} | "
        f"Cards: {card_slugs} | "
        f"{deal['price']['amount'] if deal['price'] else '0'} "
        f"{deal['price']['currency'] if deal['price'] else ''}"
    )
