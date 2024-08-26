# SPOTIFY TO YOUTUBE PLAYLIST CONVERTER READ ME
This program can be run in either a normal code environment or virtual environment
## STEP 1
Install all of the required packages with the following command:
`pip install -r requirements.txt`

## STEP 2
Create a Spotify Developer Account and go to the Developer Dashboard

Go to "Create an App". (Values given here do not matter)

Agree to terms and conditions.

After creating the app, access your Client ID and access your Client Secret through the app settings.

In the vars.env and credentials.json file, paste your respective ID's into them. 

**--DO NOT SHARE YOUR CLIENT SECRET ID ANYWHERE ELSE--**

## STEP 3
Visit Google Cloud Console and select "New Project" from the dropdown in the top left

Name your project and create it.

Go to "APIs & Services" to "Library"

Search for "YouTube Data API v3" and click it and then Enable it

Go back to Google Cloud Console, go to "APIs & Services" to "Credentials."


Click on "Create Credentials" and choose "OAuth 2.0 Client ID."

Choose "External" user type, rest of the values do not matter

Go back to "Credentials" and choose "OAuth 2.0 Client ID."

Select "Desktop App", give it a name and create it

Download the credentials.json file and replace the one provided with your downloaded one. Make sure it is in the same directory as the rest of the files

## STEP 4
Go to the main() method and choose your playlist title and description. Add the spotify playlist you'd like to convert from in the playlist_id.

Run the program.

On your first run, the code will create a playlist for you on YouTube and start adding songs to it until you reach your daily API quota.

You will now have a playlist_id.txt and progress.txt file as well. Change the number in the progress.txt to the index of the last song that was added. You can check this by going to YouTube and seeing how many songs were added already.

Then you can just run the program until all your songs are fully transferred each day as the daily API quota refreshes.
