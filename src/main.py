import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SORARE_API_KEY")
API_URL = "https://api.sorare.com/graphql"

query = """
query MyUser {
  currentUser {
    slug
    nickname
  }
}
"""

response = requests.post(
    API_URL,
    json={"query": query},
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

print(response.json())

