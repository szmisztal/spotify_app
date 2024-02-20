import datetime
import urllib
import requests
from secrets import client_id, client_secret, user_name, redirect_uri
from spotify_auth import SpotifyAuth

class SpotifyClient:
    def __init__(self, access_token, refresh_token):
        self.client_start = datetime.datetime.now()
        self.user_name = user_name
        self.api_url = "https://api.spotify.com/v1/"
        self.access_token = access_token
        self.refresh_token = refresh_token

    @staticmethod
    def user_inputs():
        album_input = input("Album: ")
        artist_input = input("Artist: ")
        return (album_input, artist_input)

    @staticmethod
    def user_input_parser(user_input):
        parsed_input = urllib.parse.quote(user_input)
        return parsed_input

    def get_auth_headers(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        return headers

    def create_request_url(self, endpoint):
        url = self.api_url + endpoint
        return url

    def search_query(self):
        # user_inputs = self.user_inputs()
        # album = self.user_input_parser(user_inputs[0])
        # artist = self.user_input_parser(user_inputs[1])
        album = "72 Seasons"
        artist = "Metallica"
        endpoint = f"search?q={album}+artist:{artist}&type=album"
        response = requests.get(url = self.create_request_url(endpoint),
                                headers = self.get_auth_headers())
        response.raise_for_status()
        return response.json()

    def get_album_id(self, response_from_search_query):
        for album in response_from_search_query["albums"]["items"]:
            album_id = album["id"]
            return album_id

    def get_album_tracks(self, album_id):
        album_tracks_ids = []
        endpoint = f"albums/{album_id}/tracks"
        response = requests.get(url = self.create_request_url(endpoint),
                                headers = self.get_auth_headers())
        response.raise_for_status()
        for track in response.json()["items"]:
            track_id = track["id"]
            album_tracks_ids.append(track_id)
        return album_tracks_ids

    def create_playlist(self):
        endpoint = f"users/{self.user_name}/playlists"
        data = {
            "name": "test_playlist"
        }
        headers = {"Authorization": f"Bearer {self.access_token}",
                   "Content-Type": "application/json"}
        response = requests.post(url = self.create_request_url(endpoint),
                                 headers = headers,
                                 json = data)
        response.raise_for_status()
        return response


if __name__ == "__main__":
    auth = SpotifyAuth(client_id, client_secret, redirect_uri)
    auth.generate_auth_code()
    token_response = auth.get_api_token()
    tokens = auth.set_up_auth_tokens(token_response)
    client = SpotifyClient(tokens["access_token"], tokens["refresh_token"])
    print(client.create_playlist())
