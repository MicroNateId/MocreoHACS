#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import getpass

BASE_URL = "https://api.mocreo.com/v1"

def make_request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    
    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_content = e.read().decode("utf-8")
        try:
            err_json = json.loads(error_content)
            errors = err_json.get("errors", [])
            err_msg = ", ".join([err.get("message", "") for err in errors]) or error_content
        except Exception:
            err_msg = error_content
        raise Exception(f"HTTP {e.code}: {err_msg}")
    except Exception as e:
        raise Exception(f"Network error: {e}")

def main():
    print("====================================================")
    print(" MOCREO IoT Platform API Key Generator")
    print("====================================================")
    print("Enter your MOCREO login credentials to generate an API key.")
    
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    
    if not email or not password:
        print("Error: Email and password are required.")
        return

    print("\nAuthenticating with MOCREO...")
    try:
        login_res = make_request(
            f"{BASE_URL}/users/login",
            method="POST",
            data={"email": email, "password": password}
        )
    except Exception as e:
        print(f"Login failed: {e}")
        return

    token = login_res.get("result", {}).get("access_token") or login_res.get("result", {}).get("token")
    if not token:
        print("Error: Failed to obtain access token from response.")
        print(f"Debug - Full Response: {json.dumps(login_res, indent=2)}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    print("Fetching accessible assets...")
    try:
        assets_res = make_request(f"{BASE_URL}/assets", headers=headers)
    except Exception as e:
        print(f"Failed to fetch assets: {e}")
        return

    assets = assets_res.get("result", [])
    if not assets:
        print("Error: No assets found under this account.")
        return

    selected_asset = None
    if len(assets) == 1:
        selected_asset = assets[0]
        print(f"Found Asset: {selected_asset.get('displayName')} (ID: {selected_asset.get('id')})")
    else:
        print("\nMultiple Assets found:")
        for idx, asset in enumerate(assets):
            print(f"  [{idx + 1}] {asset.get('displayName')} (ID: {asset.get('id')})")
        
        while True:
            choice = input(f"Select an asset (1-{len(assets)}): ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(assets):
                    selected_asset = assets[idx]
                    break
            except ValueError:
                pass
            print("Invalid selection. Please try again.")

    asset_id = selected_asset.get("id")
    asset_name = selected_asset.get("displayName")

    print(f"\nGenerating permanent API Key for asset '{asset_name}'...")
    key_payload = {
        "displayName": "Home Assistant Integration",
        "permissions": [
            "asset.read",
            "asset.update",
            "device.read",
            "device.update",
            "membership.read"
        ],
        "expiresAt": None
    }

    try:
        key_res = make_request(
            f"{BASE_URL}/assets/{asset_id}/apikeys",
            method="POST",
            headers=headers,
            data=key_payload
        )
    except Exception as e:
        print(f"Failed to create API Key: {e}")
        return

    api_key = key_res.get("result", {}).get("key")
    if not api_key:
        print("Error: API Key was not returned in the server response.")
        return

    print("\n====================================================")
    print(" SUCCESS! Copy these credentials to Home Assistant:")
    print("====================================================")
    print(f" Asset ID: {asset_id}")
    print(f" API Key:  {api_key}")
    print("====================================================")
    print("Keep this API Key secure. It will not be shown again.")
    print("====================================================")

if __name__ == "__main__":
    main()
