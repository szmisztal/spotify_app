import urllib
import requests
from secrets import client_id, client_secret


def get_api_token():
      url = "https://accounts.spotify.com/api/token"
      data = {"grant_type": "client_credentials",
              "client_id": client_id,
              "client_secret": client_secret
             }
      response = requests.post(url, data = data)
      return response.json().get("access_token")

def call_spotify_api(endpoint):
    api_token = get_api_token()
    full_url = f"https://api.spotify.com/v1/{endpoint}"
    headers = {
       "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(full_url, headers = headers)
    response.raise_for_status()
    return response.json()

def search_query():
    encoded_user_inputs = user_inputs()
    album = encoded_user_inputs[0]
    artist = encoded_user_inputs[1]
    response = call_spotify_api(f"search?q={album}+artist:{artist}&type=album")
    return response

def user_inputs():
    album_input = input("Album: ")
    artist_input = input("Artist: ")
    album_encode = urllib.parse.quote(album_input)
    artist_encode = urllib.parse.quote(artist_input)
    return (album_encode, artist_encode)


print(search_query())
