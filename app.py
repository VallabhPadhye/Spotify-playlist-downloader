import os

import spotipy

import youtube_dl

import streamlit as st

# Set up the Spotify API client

client_id = '997520ddc3424e7982763005cdf62d88'

client_secret = 'c980f35218c7499eb9d442c460d1c222'

redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(

    client_id=client_id,

    client_secret=client_secret,

    redirect_uri=redirect_uri,

    scope='playlist-read-private'))

# Helper function to download a track given its Spotify URI

def download_track(uri):

    track = sp.track(uri)

    artist = track['artists'][0]['name']

    title = track['name']

    search_query = f"{artist} {title} audio"

    ydl_opts = {

        'format': 'bestaudio/best',

        'outtmpl': f"{artist} - {title}.%(ext)s",

        'postprocessors': [{

            'key': 'FFmpegExtractAudio',

            'preferredcodec': 'mp3',

            'preferredquality': '320'

        }]

    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        ydl.download([search_query])

# Streamlit app

st.title("Spotify Playlist Downloader")

# Get the playlist URL from the user

playlist_url = st.text_input("Enter the URL of the Spotify playlist:")

# If the user has entered a playlist URL, download all the tracks in the playlist

if playlist_url:

    st.write(f"Downloading playlist {playlist_url}...")

    playlist_id = playlist_url.split("/")[-1]

    results = sp.playlist_items(playlist_id)

    tracks = results['items']

    while results['next']:

        results = sp.next(results)

        tracks.extend(results['items'])

    st.write(f"Found {len(tracks)} tracks in playlist {playlist_url}.")

    st.write("Downloading...")

    for track in tracks:

        uri = track['track']['uri']

        download_track(uri)

    st.write("Download complete!")

