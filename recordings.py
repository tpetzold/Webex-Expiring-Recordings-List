import json
import os
import list_recordings
import download_recordings

from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

tokenPath = list_recordings.os.path.dirname(list_recordings.os.path.abspath(__file__))
filename = list_recordings.os.path.join(tokenPath, 'token.json')
with open (filename, 'r') as openfile:
    token = json.load(openfile)
    bearer = token["token"]
    if bearer == "":
        print("No stored token. \nEnter your access token.\n")
        token = input("> ")
        while token == "":
            print("No token entered. Try again.\n")
            token = input("> ")
        bearer = {"token":token}
        with open('token.json', 'w') as updateToken:
            json.dump(bearer, updateToken)
        bearer = token
    else:
        print('Current Token: '+str(bearer))

headers = {
    "Accept":"application/json",
    "Content-Type":"application/json",
    "Authorization":"Bearer "+str(bearer)
    }

if not list_recordings.os.path.exists("Downloaded-Recordings/"):
    list_recordings.os.makedirs("Downloaded-Recordings/")

def get_env_or_input(prompt, env_var):
    """ Helper function to get input from environment or prompt user """
    return os.getenv(env_var) or input(prompt)

print("This app can be used to collect all recordingIds and associated hostEmails and then download all recordings locally.")
print("First you'll choose option 1 to collect recording data and the app will terminate.")
print("After all recording data has been collected then run the app again and choose option 2 to download all recordings.\n")
print("Select an option:")
print("1 - List all recordings and save to .csv file.")
print("2 - Download recordings.\n")

run = True

while run:
    choice = input("> ")
    print(f"You selected {choice}")

    try:
        if choice == "1":
            site_url = get_env_or_input("Enter the Webex site URL you want to pull recordings from (e.g., sitename.webex.com):\n> ", 'site_url')
            retention = get_env_or_input("Enter the retention period:\n> ", 'retention')
            expiresIn = get_env_or_input("Enter the number of days before the files are deleted that you want to list:\n> ", 'expiresIn')
            
            print("Listing recordings and saving to file, please wait...\n")
            run = list_recordings.list_recordings(headers, site_url, retention, expiresIn)
            print("Finished!")
        
        elif choice == "2":
            print("Downloading recordings...\n")
            run = download_recordings.getDownloadLinks(headers)
            print("Finished!")
        
        else:
            print("Invalid option.\nTry again.\n> ")

    except Exception as e:
        print(f"An error occurred: {e}")