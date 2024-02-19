import datetime
import urllib
import requests
from secrets import client_id, client_secret


class SpotifyClient:
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

    # def refresh_api_token(self):
    #     url = "https://accounts.spotify.com/api/token"
    #     headers = {
    #         "Content-Type": "application/x-www-form-urlencoded"
    #     }
    #     data = {
    #         "grant_type": "refresh_token",
    #         "refresh_token": self.api_token,
    #         "client_id": client_id,
    #         "client_secret": client_secret
    #     }
    #     response = requests.post(url, data = data, headers = headers)
    #     return response.json()

    def call_spotify_api(self, endpoint, data = None):
        full_url = f"https://api.spotify.com/v1/{endpoint}"
        headers = {
           "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.get(full_url, headers = headers, data = data)
        response.raise_for_status()
        return response.json()

    def user_inputs(self):
        album_input = input("Album: ")
        artist_input = input("Artist: ")
        return (album_input, artist_input)

    def user_input_parser(self, user_input):
        parsed_input = urllib.parse.quote(user_input)
        return parsed_input

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

    def open_player(self, album_id):
        endpoint = "me/player/play"
        data = {
            "context_uri": f"spotify:album:{album_id}"
        }
        response = self.call_spotify_api(endpoint, data)
        return response

api = SpotifyClient()
album_id = api.get_album_id(api.search_query())
print(api.get_album_tracks(album_id))

