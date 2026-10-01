import os

import jwt
import requests
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class EntraIDAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid Authorization header")

        token = auth_header.split(" ", 1)[1]

        tenant_id = os.environ.get("ENTRA_TENANT_ID")
        api_client_id = os.environ.get("ENTRA_API_CLIENT_ID")

        if not tenant_id or not api_client_id:
            raise AuthenticationFailed(
                "Entra ID environment variables are not configured"
            )

        issuer = (
            f"https://login.microsoftonline.com/"
            f"{tenant_id}/v2.0"
        )

        jwks_url = (
            f"https://login.microsoftonline.com/"
            f"{tenant_id}/discovery/v2.0/keys"
        )

        try:
            jwks_client = jwt.PyJWKClient(jwks_url)

            signing_key = jwks_client.get_signing_key_from_jwt(token)
            unverified_payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )

            print("TOKEN VER:", unverified_payload.get("ver"))
            print("TOKEN ISS:", unverified_payload.get("iss"))
            print("TOKEN AUD:", unverified_payload.get("aud"))
            print("TOKEN TID:", unverified_payload.get("tid"))
            print("TOKEN SCP:", unverified_payload.get("scp"))
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=api_client_id,
                issuer=issuer,
            )

        except Exception as e:
            raise AuthenticationFailed(
                f"Invalid access token: {str(e)}"
            )

        scopes = payload.get("scp", "").split()

        if "Test.Access" not in scopes:
            raise AuthenticationFailed(
                "Required scope Test.Access is missing"
            )

        username = (
            payload.get("preferred_username")
            or payload.get("upn")
            or payload.get("sub")
        )

        if not username:
            username = "unknown"

        return (
            EntraUser(username, payload),
            None,
        )


class EntraUser:
    def __init__(self, username, claims):
        self.username = username
        self.claims = claims
        self.is_authenticated = True

    def __str__(self):
        return self.username