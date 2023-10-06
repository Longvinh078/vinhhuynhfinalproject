# Import necessary libraries
import requests  # For making HTTP requests
import tkinter as tk  # For creating the GUI window
import pytest  # For testing
import os  # For environment variables and file operations

API_KEY = '870b08e49e1148f452f5e12f86c1e75f'
# Function to retrieve the release date of an album using its ID
def get_release_date(album_id):
    # Set up the parameters for the API request
    params = {
        'album_id': album_id,
        'apikey': API_KEY
    }

    # Make an API request to get album details
    response = requests.get('http://api.musixmatch.com/ws/1.1/album.get', params=params)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Check if the 'album' key is present in the response
        if 'album' in data['message']['body']:
            album = data['message']['body']['album']
            release_date = album['album_release_date']

            # Format the release date as desired
            formatted_release_date = release_date  # You can format this using Python's datetime module
            return formatted_release_date
        else:
            return "Release date not found"
    else:
        return "Error fetching data"


# Function to retrieve lyrics based on song title and artist
def get_lyrics(song_title, song_artist):
    # Set up the parameters for the lyrics API request
    lyrics_params = {
        'q_artist': song_artist,
        'q_track': song_title,
        'apikey': API_KEY
    }

    # Make an API request to get lyrics
    lyrics_response = requests.get('http://api.musixmatch.com/ws/1.1/matcher.lyrics.get', params=lyrics_params)

    # Check if the API request was successful (status code 200)
    if lyrics_response.status_code == 200:
        lyrics_data = lyrics_response.json()  # Parse the JSON response

        # Check if the 'lyrics' key is present in the response
        if 'lyrics' in lyrics_data['message']['body']:
            lyrics_body = lyrics_data['message']['body']['lyrics']['lyrics_body']
            return lyrics_body
        else:
            return "Lyrics not found"
    else:
        return "Error fetching lyrics"


# Function to retrieve song information and display it in the GUI
def get_info():
    song_title = song_title_entry.get()  # Get the song title entered by the user
    song_artist = song_artist_entry.get()  # Get the song artist entered by the user

    # Check if either the song title or artist is missing
    if not song_title or not song_artist:
        result_label.config(text="Please enter both song title and artist.")
        return

    # Set up parameters for the API request to search for song details
    params = {
        'q_track': song_title,
        'q_artist': song_artist,
        'apikey': API_KEY
    }

    # Make an API request to search for the song details
    response = requests.get('http://api.musixmatch.com/ws/1.1/track.search', params=params)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response

        # Check if there are track results in the response
        if data['message']['body']['track_list']:
            track = data['message']['body']['track_list'][0]['track']
            album_id = track['album_id']
            album_name = track['album_name']
            artist_name = track['artist_name']

            # Get the release date using the get_release_date function
            release_date = get_release_date(album_id)

            # Get the lyrics using the get_lyrics function
            lyrics = get_lyrics(song_title, song_artist)

            # Display the information in the Tkinter window
            result_label.config(
                text=f"Album: {album_name}\nArtist: {artist_name}\nRelease Date: {release_date}\nLyrics:\n{lyrics}")
        else:
            result_label.config(text="No results found")
    else:
        result_label.config(text="Error fetching data")


# Create the main Tkinter window
root = tk.Tk()
root.title("Music Info Search")

# Create GUI elements (labels, entry fields, buttons, and result label)
song_title_label = tk.Label(root, text="Song Title:")
song_title_label.pack()
song_title_entry = tk.Entry(root)
song_title_entry.pack()

song_artist_label = tk.Label(root, text="Song Artist:")
song_artist_label.pack()
song_artist_entry = tk.Entry(root)
song_artist_entry.pack()

get_info_button = tk.Button(root, text="Get Info", command=get_info)
get_info_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Start the Tkinter main loop
root.mainloop()


# Define a test function for GUI functionality
@pytest.mark.skipif("DISPLAY" not in os.environ, reason="No display")
def test_gui_functionality():
    pass