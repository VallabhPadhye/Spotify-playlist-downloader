import streamlit as st

import spotipy

import spotipy.util as util

from spotipy.oauth2 import SpotifyClientCredentials

import os

import requests

# Spotify API credentials

CLIENT_ID = '997520ddc3424e7982763005cdf62d88'

CLIENT_SECRET = 'c980f35218c7499eb9d442c460d1c222'

# Spotipy object initialization

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Streamlit app title and description

st.title("Spotify Playlist Downloader")

st.markdown("Download your favorite playlists with just a few clicks!")

# Authenticate with Spotify using OAuth 2.0

scope = 'user-library-read playlist-read-private'

token = util.prompt_for_user_token('vallabhpadhye@rediffmail.com', scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET,

                                   redirect_uri='http://localhost:8080/callback/')

if token:

    sp = spotipy.Spotify(auth=token)

    user = sp.current_user()

    st.write(f"Logged in as {user['display_name']}")

    # Get the list of user's playlists

    playlists = sp.current_user_playlists()

    playlist_names = [p['name'] for p in playlists['items']]

    selected_playlist = st.selectbox("Select a playlist", playlist_names)

    # Get the tracks of the selected playlist and download them

    for playlist in playlists['items']:

        if selected_playlist == playlist['name']:

            st.write(f"Downloading tracks for {selected_playlist} playlist...")

            playlist_id = playlist['id']

            tracks = sp.playlist_tracks(playlist_id, fields='items.track.id')

            track_ids = [t['track']['id'] for t in tracks['items']]

            # Create folder to store downloaded tracks

            folder_path = f"{selected_playlist} playlist"

            if not os.path.exists(folder_path):

                os.makedirs(folder_path)

            # Download tracks

            for track_id in track_ids:

                track_info = sp.track(track_id)

                track_name = track_info['name']

                artist_name = track_info['artists'][0]['name']

                track_file_name = f"{artist_name} - {track_name}.mp3"

                track_file_path = os.path.join(folder_path, track_file_name)

                track_preview_url = track_info['preview_url']

                # Download track preview from the Spotify API

                if track_preview_url:

                    response = requests.get(track_preview_url)

                    with open(track_file_path, 'wb') as f:

                        f.write(response.content)

            st.success("Tracks downloaded successfully!")

else:

    st.error("Authentication failed!")

