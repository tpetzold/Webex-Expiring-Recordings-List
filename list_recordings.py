import requests
import datetime
import json
import os
import time
import csv

def token_refresh():
    url = "https://webexapis.com/v1/access_token"
    refresh_headers = {"Accept": "application/json", "Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "client_id": os.getenv('client_id'),
        "client_secret": os.getenv('client_secret'),
        "refresh_token": os.getenv('refresh_token')
    }
    for attempt in range(4):
        response = requests.post(url, json=data, headers=refresh_headers)
        if response.status_code == 200:
            return response.json()  # Parse JSON directly
        time.sleep(1)  # Optional: wait before retrying
    print("Failed to refresh token after multiple attempts.")
    return None

def store_recordings(items):
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(path, 'recordings.csv')
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as write_recordings:
        writer = csv.writer(write_recordings, delimiter=',')
        if not file_exists:
            writer.writerow(['Record ID', 'Host Email', 'Host Display Name', 'Topic', 'Time Recorded'])  # Header
        for item in items:
            writer.writerow([
                item['id'], 
                item['hostEmail'], 
                item['hostDisplayName'], 
                item['topic'], 
                item['timeRecorded']
            ])

def list_recordings(headers, site_url, retention, expires_in):
    now = datetime.datetime.now().replace(microsecond=0)
    from_time = now - datetime.timedelta(days=int(retention))
    end_time = from_time + datetime.timedelta(days=int(expires_in))
    to_time = from_time + datetime.timedelta(days=30)
    more = True
    count = 0

    while more:
        try:
            url = f"https://webexapis.com/v1/admin/recordings?siteUrl={site_url}&max=100&from={from_time}&to={to_time}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 401:
                if not all([os.getenv('client_id'), os.getenv('client_secret'), os.getenv('refresh_token')]):
                    print("Unable to refresh token. Please ensure all environment variables are set correctly.")
                    break
                else:
                    print("Token expired, generating new one...")
                    new_token_data = token_refresh()
                    if not new_token_data:
                        break
                    new_token = new_token_data['access_token']
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {new_token}"
                    }
                    with open('token.json', 'w') as update_token:
                        json.dump({"token": new_token}, update_token)

            elif response.status_code == 200:
                recordings = response.json()
                items = recordings.get('items', [])
                if items:
                    store_recordings(items)
                count += 1
                print(f"Page Count: {count}")

                next_url = response.headers.get("link")
                if next_url:
                    url = next_url.strip()[1:].split(">")[0]
                    response = requests.get(url, headers=headers)
                    continue

                from_time = to_time
                to_time = from_time + datetime.timedelta(days=30)
                if from_time > end_time:
                    more = False
                    print(f"Pulled all recordings expiring in the next {expires_in} days")

            elif response.status_code == 429:
                retry_after = response.headers.get("retry-after", 1)
                print(f"Rate limited. Waiting {retry_after} seconds.")
                time.sleep(int(retry_after))

            else:
                print("An unexpected error occurred.")
                print(response.text)
                break

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break