import base64
import requests


class SpotifyAuth:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = "playlist-modify-public playlist-modify-private"
        self.access_token = None
        self.refresh_token = None

    def generate_auth_code(self):
        url = "https://accounts.spotify.com/authorize"
        auth_code_url = url + "?response_type=code" + f"&client_id={self.client_id}" + f"&redirect_uri={self.redirect_uri}" + f"&scope={self.scope}"
        print(f"Open link: {auth_code_url} and copy auth code from browser.")

    def get_api_token(self):
        code = input("Paste auth code: ")
        url = "https://accounts.spotify.com/api/token"
        credentials = f"{self.client_id}:{self.client_secret}"
        credentials_base64 = base64.b64encode(credentials.encode()).decode()
        authorization_header = f"Basic {credentials_base64}"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        headers = {
            "Authorization": authorization_header,
            "Content-type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data = data, headers = headers)
        response.raise_for_status()
        return response.json()

    def set_up_auth_tokens(self, response_with_tokens):
        self.access_token = response_with_tokens["access_token"]
        self.refresh_token = response_with_tokens["refresh_token"]
