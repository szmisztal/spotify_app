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

def search_query(query):
    response = call_spotify_api(f"search?q={query}&type=album")
    return response


print(search_query("Demonologia"))
