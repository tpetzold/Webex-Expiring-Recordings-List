import requests
import json
import csv
import time
import urllib.parse

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

def getDownloadLinks(headers):
    recordingDownloadLink = None
    with open('recordings.csv', 'r') as csvfile:
        recs = csv.reader(csvfile)
        next(recs)  # Skip the header row
        for row in recs:
            id = row[0]
            hostEmail = row[1].replace('@', '%40').replace("+", "%2B")
            print(f"RecordingId: {id}, HostEmail: {hostEmail}")
            url = f'https://webexapis.com/v1/recordings/{id}?hostEmail={hostEmail}'
            print(url)
            result = requests.get(url, headers=headers)
            downloadLink = json.loads(result.text)
            # print(result.text)
            links = downloadLink.get('temporaryDirectDownloadLinks')
            if links:
                recordingDownloadLink = links.get('recordingDownloadLink')
                #print(f"Download Link: {recordingDownloadLink}")
                if recordingDownloadLink:
                    try:
                        recording = requests.get(recordingDownloadLink)
                        if recording.status_code == 200:
                            fileName = recording.headers.get('Content-Disposition').split("''")[1]
                            fileName = urllib.parse.unquote(fileName)
                            print(f"Filename: {fileName}")
                            with open(f"Downloaded-Recordings/{fileName}", 'wb') as file:
                                file.write(recording.content)
                                print(f"{fileName} saved!")
                                print()
                        elif recording.status_code == 429:
                            retry_after = recording.headers.get("retry-after") or recording.headers.get("Retry-After")
                            print(f"Rate limited. Waiting {retry_after} seconds.")
                            time.sleep(int(retry_after))
                        else:
                            print("Unable to download, something went wrong!")
                            print(f"Status Code: {recording.status_code}")
                    except Exception as e:
                        print(e)
                else:
                    print("Something went wrong.")
            else:
                print("No links found.")