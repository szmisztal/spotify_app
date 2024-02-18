import datetime
import urllib
import requests
from secrets import client_id, client_secret


class SpotifyAPI:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_token = self.get_api_token()
        self.client_start = datetime.datetime.now()

    def get_api_token(self):
        url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data = data)
        return response.json().get("access_token")

    def refresh_api_token(self):
        pass

    def call_spotify_api(self, endpoint):
        full_url = f"https://api.spotify.com/v1/{endpoint}"
        headers = {
           "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.get(full_url, headers = headers)
        response.raise_for_status()
        return response.json()

    def search_query(self):
        encoded_user_inputs = self.user_inputs()
        album = encoded_user_inputs[0]
        artist = encoded_user_inputs[1]
        response = self.call_spotify_api(f"search?q={album}+artist:{artist}&type=album")
        return response

    def user_inputs(self):
        album_input = input("Album: ")
        artist_input = input("Artist: ")
        album_encode = urllib.parse.quote(album_input)
        artist_encode = urllib.parse.quote(artist_input)
        return (album_encode, artist_encode)


a = SpotifyAPI()
print(a.client_start)

