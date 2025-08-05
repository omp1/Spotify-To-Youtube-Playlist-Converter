# 🎵 Spotify-to-YouTube Playlist Converter

A Python-based automation tool that transfers Spotify playlists to YouTube Music using the Spotify and YouTube Data APIs.

This project bridges the gap between two major music platforms by automatically locating and recreating a Spotify playlist on your YouTube account. The program searches for each track on YouTube and adds it to a newly created YouTube playlist with minimal manual input.

---

## ⚙️ Features

- 🔄 Transfers entire Spotify playlists to YouTube Music  
- 🔍 Automatically searches for each song on YouTube  
- ✅ Handles progress tracking and API quota limits  
- 🗂️ Supports OAuth2.0 authentication for both platforms  
- 💾 Resumes from last progress using `progress.txt`

---

## 📦 Setup Instructions

### 🧪 Step 1: Install Dependencies  
```bash
pip install -r requirements.txt


🛠️ Step 1: Set Up Spotify Developer Access
Create a Spotify Developer Account.

Click "Create an App" — values don't matter for testing.

Agree to the terms and conditions.

Once the app is created, go to Settings and copy the following:

Client ID

Client Secret

Open the vars.env and credentials.json files and paste the respective values:

SPOTIPY_CLIENT_ID=...

SPOTIPY_CLIENT_SECRET=...

⚠️ Do not share your client secret publicly.

🎬 Step 2: Enable YouTube Data API
Visit Google Cloud Console.

Click the dropdown in the top-left and select "New Project".

Name the project and click "Create".

Go to APIs & Services → Library.

Search for YouTube Data API v3 → Click it → Click Enable.

Now go to APIs & Services → Credentials.

Click Create Credentials → OAuth 2.0 Client ID.

For user type, select External, then continue.

Go back to Credentials, and click OAuth 2.0 Client ID again.

Select Desktop App, give it a name, and click Create.

Download the credentials.json file.

Replace the existing credentials.json in your project directory with the new one.

🎵 Step 3: Configure Playlist and Run
Open the main() method in your script.

Update:

Your desired playlist title

Your playlist description

The playlist_id of the Spotify playlist you'd like to convert

Run the script:

bash
Copy
Edit
python your_script_name.py
🔁 Handling API Quotas and Progress
The first run will create a new playlist on YouTube and add songs until you hit your daily quota.

After running once, two files will be generated:

playlist_id.txt: stores the new YouTube playlist ID

progress.txt: stores the index of the last added song

To resume where you left off:

Look at your YouTube playlist to see how many songs were added

Update the number in progress.txt to the index of the last added song

Run the script again the next day (after the daily API quota resets)

📂 File Overview
main.py – main script for execution

credentials.json – Google OAuth2 credentials

vars.env – environment variables for Spotify API

requirements.txt – required Python packages

playlist_id.txt – stores the YouTube playlist ID after creation

progress.txt – keeps track of how far the script progressed

⚠️ Disclaimer
This tool is intended for educational or personal use only. Make sure you comply with Spotify and YouTube's terms of service
