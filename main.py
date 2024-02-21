import datetime
import requests
from secrets import client_id, client_secret, user_name, redirect_uri
from spotify_auth import SpotifyAuth
from interaction_with_user import UserInteraction


class SpotifyClient:
    def __init__(self, user_name, access_token, refresh_token):
        self.client_start = datetime.datetime.now()
        self.user_name = user_name
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_interaction = UserInteraction()

    def call_spotify_api(self, endpoint, request_type, data = None):
        url = f"https://api.spotify.com/v1/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        if request_type == "get":
            response = requests.get(url, headers = headers)
        elif request_type == "post":
            response = requests.post(url, headers = headers, json = data)
        elif request_type == "put":
            response = requests.put(url, headers = headers, json = data)
        response.raise_for_status()
        return response.json()

    def search_query(self):
        user_inputs = self.user_interaction.user_album_and_artist_inputs()
        album = user_inputs[0]
        artist = user_inputs[1]
        endpoint = f"search?q={album}+artist:{artist}&type=album"
        return self.call_spotify_api(endpoint, "get")

    def get_album_id(self, response_from_search_query):
        for album in response_from_search_query["albums"]["items"]:
            album_id = album["id"]
            return album_id

    def get_album_tracks(self, album_id):
        album_tracks_ids = []
        endpoint = f"albums/{album_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = self.call_spotify_api(endpoint, "get", headers)
        for track in response["items"]:
            track_id = track["id"]
            album_tracks_ids.append(track_id)
        return album_tracks_ids

    def create_playlist(self):
        endpoint = f"users/{self.user_name}/playlists"
        playlist_name = self.user_interaction.playlist_name_input()
        data = {
            "name": playlist_name
        }
        self.call_spotify_api(endpoint, "post", data)

    def start_playback(self, album_id):
        endpoint = f"me/player/play"
        data = {
            "context_uri": album_id
        }
        self.call_spotify_api(endpoint, "put", data)


if __name__ == "__main__":
    auth = SpotifyAuth(client_id, client_secret, redirect_uri)
    auth.generate_auth_code()
    token_response = auth.get_api_token()
    tokens = auth.set_up_auth_tokens(token_response)
    client = SpotifyClient(user_name, tokens["access_token"], tokens["refresh_token"])
    searched_query = client.search_query()
    album_id = client.get_album_id(searched_query)
    client.start_playback(album_id)

