import datetime
import urllib
import requests
from secrets import client_id, client_secret, user_name


class SpotifyClient:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.my_user_name = user_name
        self.api_token = self.get_api_token()
        self.client_start = datetime.datetime.now()

    def user_inputs(self):
        album_input = input("Album: ")
        artist_input = input("Artist: ")
        return (album_input, artist_input)

    def user_input_parser(self, user_input):
        parsed_input = urllib.parse.quote(user_input)
        return parsed_input

    def get_api_token(self):
        url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data = data)
        return response.json().get("access_token")

    def call_spotify_api(self, endpoint, data = None):
        url = f"https://api.spotify.com/v1/{endpoint}"
        headers = {
           "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.get(url, headers = headers, data = data)
        response.raise_for_status()
        return response.json()

    def search_query(self):
        # user_inputs = self.user_inputs()
        # album = self.user_input_parser(user_inputs[0])
        # artist = self.user_input_parser(user_inputs[1])
        album = "72 Seasons"
        artist = "Metallica"
        endpoint = f"search?q={album}+artist:{artist}&type=album"
        response = self.call_spotify_api(endpoint)
        return response

    def get_album_id(self, response_from_search_query):
        for album in response_from_search_query["albums"]["items"]:
            album_id = album["id"]
            return album_id

    def get_album_tracks(self, album_id):
        album_tracks_ids = []
        endpoint = f"albums/{album_id}/tracks"
        response = self.call_spotify_api(endpoint)
        for track in response["items"]:
            track_id = track["id"]
            album_tracks_ids.append(track_id)
        return album_tracks_ids

    def user_profile(self, user_id):
        endpoint = f"users/{user_id}"
        response = self.call_spotify_api(endpoint)
        return response


