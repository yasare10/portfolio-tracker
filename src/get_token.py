import json
import urllib.parse
import requests
import bcrypt
from getpass import getpass

API_URL = "https://api.sorare.com/graphql"
SALT_URL_TEMPLATE = "https://api.sorare.com/api/v1/users/{email}"

AUD = "portfolio-tracker"  # pick any string; keep it consistent

SIGN_IN_MUTATION = """
mutation SignInMutation($input: signInInput!) {
  signIn(input: $input) {
    currentUser { slug }
    jwtToken(aud: "%s") { token expiredAt }
    otpSessionChallenge
    tcuToken
    errors { message }
  }
}
""" % AUD

ACCEPT_TERMS_MUTATION = """
mutation AcceptTermsMutation($input: acceptTermsInput!) {
  acceptTerms(input: $input) {
    errors { message }
  }
}
"""

def post_graphql(query: str, variables: dict):
    r = requests.post(
        API_URL,
        headers={"content-type": "application/json"},
        json={"operationName": None, "query": query, "variables": variables},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()

def main():
    email = input("Sorare email: ").strip()
    password = getpass("Sorare password (input hidden): ")

    # 1) Get salt
    email_enc = urllib.parse.quote(email, safe="")
    salt_resp = requests.get(SALT_URL_TEMPLATE.format(email=email_enc), timeout=30)
    salt_resp.raise_for_status()
    salt = salt_resp.json().get("salt")
    if not salt:
        raise SystemExit("Could not fetch salt (did you type the email correctly?).")

    # 2) Hash password with bcrypt using that salt
    # (Sorare docs: bcrypt hash client-side using returned salt) :contentReference[oaicite:2]{index=2}
    salt_bytes = salt.replace(" ", "").encode("utf-8")
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt_bytes).decode("utf-8")

    # 3) Sign in to get JWT
    data = post_graphql(SIGN_IN_MUTATION, {"input": {"email": email, "password": hashed_pw}})
    sign_in = (data.get("data") or {}).get("signIn")

    if not sign_in:
        print(json.dumps(data, indent=2))
        raise SystemExit("Sign-in failed (no signIn payload).")

    # If Sorare returns errors
    errs = sign_in.get("errors") or []
    if errs:
        print("Sign-in errors:")
        print(json.dumps(errs, indent=2))

    # Terms & Conditions flow (if required)
    tcu_token = sign_in.get("tcuToken")
    if tcu_token:
        print("\nSorare requires accepting updated Terms & Conditions before sign-in can succeed.")
        print("Attempting to accept terms now...")

        accept_vars = {
            "input": {
                "acceptTerms": True,
                "acceptPrivacyPolicy": True,
                "acceptGameRules": True,
                "tcuToken": tcu_token,
            }
        }
        accept_resp = post_graphql(ACCEPT_TERMS_MUTATION, accept_vars)
        print("acceptTerms response:", json.dumps(accept_resp, indent=2))
        print("\nNow run this script again to sign in.")
        return

    # 2FA flow (if enabled)
    otp_challenge = sign_in.get("otpSessionChallenge")
    if otp_challenge:
        otp = input("\n2FA enabled. Enter the one-time code from your authenticator/email: ").strip()
        data2 = post_graphql(
            SIGN_IN_MUTATION,
            {"input": {"otpSessionChallenge": otp_challenge, "otpAttempt": otp}},
        )
        sign_in = (data2.get("data") or {}).get("signIn")
        if not sign_in:
            print(json.dumps(data2, indent=2))
            raise SystemExit("2FA sign-in failed (no signIn payload).")

    jwt = sign_in.get("jwtToken")
    user = sign_in.get("currentUser")

    if not jwt or not jwt.get("token"):
        print("\nNo JWT returned. Full response:")
        print(json.dumps({"data": data, "signIn": sign_in}, indent=2))
        raise SystemExit("Could not obtain JWT token.")

    print("\n✅ JWT acquired")
    print("User:", (user or {}).get("slug"))
    print("AUD:", AUD)
    print("Expires at:", jwt.get("expiredAt"))
    print("\nPaste these into your .env (DO NOT commit .env):")
    print(f"SORARE_JWT_TOKEN={jwt['token']}")
    print(f"SORARE_JWT_AUD={AUD}")

if __name__ == "__main__":
    main()
