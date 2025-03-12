This code is a derivative of the Webex Recording Downloader
https://github.com/WebexSamples/WebexRecordingsDownloader

This application was created to allow a customer to list all Webex recordings that will be deleted due to reaching the retention period.

A customer has asked if we can create a list so they can send a custom e-mail to users whose recordings will be deleted when reaching the retention period. This code was adopted from the Webex Recording Downloader code at the link above so it retains the ability to download the recordings and has the same basic structure.

It is a two-step process which requires the app to be ran twice.

On first run choose option 1 and provide your Webex site URL, for example _sitename.webex.com_, the retention period, and the number of days before the retention period you want to search.

- For all recordings in this site between the days before and the retention period it collects the recording ID, Host Email, Host Display Name, Meeting Topic, and Time Recorded and stores them in the recordings.csv file.
- The app will terminate itself after completion.

Run the app again choose option 2.

- This will download all recordings that were retrieved from step 1 and save them to the "Downloaded-Recordings" folder.

---

**Install and Run**

Clone project:

- `git clone https://github.com/tpetzold/Webex-Expiring-Recordings-List.git`

Install dependencies:

- `pip install -r requirements.txt`

Run app:

- `python recordings.py`

---

**Setup**

Unfortunately you can't simply us a key from the developer portal. The token generated from the developer portal won't allow you to generante a download link. You must either setup a Integration or Service App in the developer portal then authorize the app in Control Hub

- Create an [Integration](https://developer.webex.com/docs/integrations) or [Service App](https://developer.webex.com/docs/service-apps) with the admin and compliance related recording scopes.
    - Required Scopes are:
        spark-compliance:recordings_read
        spark-compliance:meetings_read
        spark-admin:recordings_read
        meeting:admin_recordings_read
- In Webex Control Hub in Management - Apps select either the Integrations or Service Apps and search for the app or integration you just created using ID shown on the developer.webex.com site
- You now need to authorize the app for your organization
- Now go back to the developer.webex.com site and generate the client secret
- In the Org Authorizations section choose your Control Hub organization
- Now copy the Client Secret and paste it into the Generate Tokens box in the Org Authorizations section
- Generate your access and refresh tokens
- Rename the [.env.local](.env.local) file to .env. And add .env to the .gitignore file
- Add your Client ID, Client Secret and Refresh Token to the .env file.
- You can also add your Access Token to the [token.json](token.json) file but the app will also ask you to enter one at first run if you haven't added it to the token.json file.
