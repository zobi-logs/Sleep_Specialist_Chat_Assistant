import requests
import pandas as pd
from datetime import datetime
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# API credentials
CLIENT_ID = "6eb339e0-c66c-4e72-a20a-ed2f11c35d04_08dd2cae-6fd0-443b-af78-dd3c7e7ac3e1"
CLIENT_SECRET = "Pm0bvJD1cPlTMnCLIDPyf3iTnsqAZH1iWtUdlYeAiPU="
TOKEN_URL = "https://icdaccessmanagement.who.int/connect/token"
API_BASE_URL = "https://id.who.int/icd/entity"
ROOT_ID = ""  # Root entity (empty ID fetches the top level)

def get_access_token():
    """Fetch OAuth2 bearer token."""
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "icdapi_access"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    try:
        response = session.post(TOKEN_URL, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Failed to get token: {e}")
        return None

def fetch_icd11_data(entity_id, token):
    """Fetch data for a given ICD-11 entity ID."""
    url = f"{API_BASE_URL}/{entity_id}" if entity_id else API_BASE_URL
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Accept-Language": "en",
        "API-Version": "v2"
    }
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    print(f"Requesting: {url}")
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        print(f"Status Code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None

def extract_icd11_entities(data, token, entities_list=None):
    """Recursively extract all ICD-11 entities with definitions."""
    if entities_list is None:
        entities_list = []
    
    if not data:
        return entities_list
    
    entity_id = data.get("@id", "").split("/")[-1]
    title = data.get("title", {}).get("@value", "No title")
    definition = data.get("definition", {}).get("@value", "No definition available")
    print(f"Processing: {entity_id} - {title}")
    
    entities_list.append({"ID": entity_id, "Title": title, "Definition": definition})
    
    if "child" in data:
        for child_url in data["child"]:
            child_id = child_url.split("/")[-1]
            child_data = fetch_icd11_data(child_id, token)
            if child_data:
                extract_icd11_entities(child_data, token, entities_list)
            time.sleep(1)  # Longer delay for bulk download
    return entities_list

def save_to_csv(entities_list):
    """Save to CSV."""
    df = pd.DataFrame(entities_list)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"icd11_full_{timestamp}.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    print("Fetching entire ICD-11...")
    token = get_access_token()
    if not token:
        print("Aborting due to token failure.")
        return
    
    root_data = fetch_icd11_data(ROOT_ID, token)
    if root_data:
        all_entities = extract_icd11_entities(root_data, token)
        if all_entities:
            save_to_csv(all_entities)
        else:
            print("No entities found.")
    else:
        print("Couldn’t retrieve root data.")

if __name__ == "__main__":
    main()