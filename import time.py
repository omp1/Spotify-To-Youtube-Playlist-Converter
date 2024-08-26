import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv('vars.env')

# Spotify Setup
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri='http://localhost:8888/callback',
    scope='playlist-read-private'
))

# YouTube Setup
SCOPES = ['https://www.googleapis.com/auth/youtube']
creds = None

# Load the credentials from file
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

youtube = build('youtube', 'v3', credentials=creds)

def get_spotify_playlist_tracks(playlist_id):
    tracks = []
    results = spotify.playlist_tracks(playlist_id)
    tracks.extend(f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in results['items'])

    # Handle pagination
    while results['next']:
        results = spotify.next(results)
        tracks.extend(f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in results['items'])

    return tracks


def search_youtube(query):
    try:
        request = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=1
        )
        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
    except HttpError as e:
        print(f"An error occurred during YouTube search: {e}")
    return None

def create_youtube_playlist(title, description):
    try:
        request = youtube.playlists().insert(
            part='snippet,status',
            body={
                'snippet': {
                    'title': title,
                    'description': description
                },
                'status': {
                    'privacyStatus': 'private'
                }
            }
        )
        response = request.execute()
        return response['id']
    except HttpError as e:
        print(f"An error occurred during playlist creation: {e}")
        return None

def add_video_to_playlist(playlist_id, video_url, retries=3):
    video_id = video_url.split('v=')[-1]
    for attempt in range(retries):
        try:
            request = youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            )
            request.execute()
            print(f"Successfully added video {video_id} to playlist {playlist_id}")
            break
        except HttpError as e:
            if e.resp.status in [403, 409]:
                print(f"Rate limit or conflict error, retrying... ({attempt + 1}/{retries})")
                time.sleep(2 ** attempt) 
            else:
                print(f"HttpError occurred: {e}")
                raise
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            raise

def resume_addition(tracks, youtube_playlist_id, start_index=0):
    for i, track in enumerate(tracks[start_index:], start=start_index):
        print(f"Processing track {i+1}: {track}")
        try:
            video_url = search_youtube(track)
            if video_url:
                add_video_to_playlist(youtube_playlist_id, video_url)
                print(f'Added {track} to YouTube playlist (Track {i+1})')
            else:
                print(f'Could not find a YouTube video for {track} (Track {i+1})')
        except Exception as e:
            print(f"Error processing track {track} (Track {i+1}): {e}")
            print("Sleeping before retrying...")
            time.sleep(600)  
            return i  # Return current index to be used for resumption
        # Save progress
        with open('progress.txt', 'w') as f:
            f.write(str(i + 1))  # Save the next track index to be processed


def main():
    playlist_id = '' #Spotify playlist to add from
    playlist_title = '' 
    playlist_description = 'Converted from Spotify playlist'
    progress_file = 'progress.txt'
    playlist_id_file = 'playlist_id.txt'

    
    tracks = get_spotify_playlist_tracks(playlist_id)

    # Check if the progress file exists to decide if we need to create a new YouTube playlist
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                start_index = int(f.read())
            print(f"Resuming from track {start_index+1}")

            # Check if the playlist ID file exists
            if os.path.exists(playlist_id_file):
                with open(playlist_id_file, 'r') as f:
                    youtube_playlist_id = f.read().strip()
                print(f"Resuming with existing YouTube playlist ID: {youtube_playlist_id}")
            else:
                print("YouTube playlist ID file not found. Creating a new playlist...")
                youtube_playlist_id = create_youtube_playlist(playlist_title, playlist_description)
                if youtube_playlist_id:
                    with open(playlist_id_file, 'w') as f:
                        f.write(youtube_playlist_id)
                    print(f'Created YouTube playlist with ID: {youtube_playlist_id}')
                else:
                    print('Failed to create YouTube playlist')
                    return

        except FileNotFoundError:
            start_index = 0  # Start from the beginning if no progress file exists
            youtube_playlist_id = create_youtube_playlist(playlist_title, playlist_description)
            if youtube_playlist_id:
                with open(playlist_id_file, 'w') as f:
                    f.write(youtube_playlist_id)
                print(f'Created YouTube playlist with ID: {youtube_playlist_id}')
            else:
                print('Failed to create YouTube playlist')
                return
    else:
        start_index = 0  # Start from the beginning if no progress file exists
        youtube_playlist_id = create_youtube_playlist(playlist_title, playlist_description)
        if youtube_playlist_id:
            with open(playlist_id_file, 'w') as f:
                f.write(youtube_playlist_id)
            print(f'Created YouTube playlist with ID: {youtube_playlist_id}')
        else:
            print('Failed to create YouTube playlist')
            return

    # Resume adding tracks to YouTube playlist
    resume_addition(tracks, youtube_playlist_id, start_index)

if __name__ == "__main__":
    main()
