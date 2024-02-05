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

# def call_spotify_api(endpoint):
#    full_url = f"https://api.spotify.com/{endpoint}"
#    headers = {
#        "Authorization": f"Bearer {api_token}"
#    }
#    response = requests.get(full_url, headers = headers)
#    response.raise_for_status()
#    return response.json()

print(get_api_token())
