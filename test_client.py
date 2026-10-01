import msal
import requests

TENANT_ID = "5ee5b59e-8d9b-46c0-b6fd-69a030e105ca"
CLIENT_ID = "b16b5856-bc03-4b99-9c3c-fb8eed652b90"
API_CLIENT_ID = "ba967ba9-6ec7-4784-ae9b-d7c9ff3ce05d"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

SCOPES = [
    f"api://{API_CLIENT_ID}/Test.Access"
]

API_URL = "https://entra-django-api-test.onrender.com/api/test/auth/"


app = msal.PublicClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
)

flow = app.initiate_device_flow(scopes=SCOPES)

if "user_code" not in flow:
    raise RuntimeError(flow)

print(flow["message"])

result = app.acquire_token_by_device_flow(flow)

if "access_token" not in result:
    print("Token取得失敗")
    print(result)
    raise SystemExit(1)

access_token = result["access_token"]

print("Access Token取得成功")

response = requests.get(
    API_URL,
    headers={
        "Authorization": f"Bearer {access_token}"
    },
)

print("Status:", response.status_code)
print("Response:")
print(response.text)