import requests
import tkinter as tk
#################################################
######### API genaral set up ####################

def get_release_date(album_id):
    # Make an API request to get album details
    params = {
        'album_id': album_id,
        'apikey': '870b08e49e1148f452f5e12f86c1e75f'
    }
    response = requests.get('http://api.musixmatch.com/ws/1.1/album.get', params=params)

    if response.status_code == 200:
        data = response.json()
        if 'album' in data['message']['body']:
            album = data['message']['body']['album']
            release_date = album['album_release_date']
            # Format the release date as desired (you can adjust the format)
            formatted_release_date = release_date  # You can format this using Python's datetime module
            return formatted_release_date
        else:
            return "Release date not found"
    else:
        return "Error fetching data"


def get_lyrics(song_title, song_artist):
    # Make an API request to get lyrics
    lyrics_params = {
        'q_artist': song_artist,
        'q_track': song_title,
        'apikey': '870b08e49e1148f452f5e12f86c1e75f'  # Replace with your API key
    }
    lyrics_response = requests.get('http://api.musixmatch.com/ws/1.1/matcher.lyrics.get', params=lyrics_params)

    if lyrics_response.status_code == 200:
        lyrics_data = lyrics_response.json()
        if 'lyrics' in lyrics_data['message']['body']:
            lyrics_body = lyrics_data['message']['body']['lyrics']['lyrics_body']
            return lyrics_body
        else:
            return "Lyrics not found"
    else:
        return "Error fetching lyrics"


def get_info():
    song_title = song_title_entry.get()
    song_artist = song_artist_entry.get()

    if not song_title or not song_artist:
        result_label.config(text="Please enter both song title and artist.")
        return

    # Search for song details using both title and artist
    params = {
        'q_track': song_title,
        'q_artist': song_artist,
        'apikey': '870b08e49e1148f452f5e12f86c1e75f'  # Replace with your API key
    }
    response = requests.get('http://api.musixmatch.com/ws/1.1/track.search', params=params)

    if response.status_code == 200:
        data = response.json()
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

root = tk.Tk()
root.title("Music Info Search")

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

root.mainloop()