import base64
import datetime
import urllib

import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class spotify_API(object):

    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    POST_query = None
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def start_connection(self ,requests_timeout = 10 ):
        client_credentials_manager = SpotifyClientCredentials(self.client_id, self.client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_timeout=requests_timeout)
        return sp

    def getTrackIDs(user, playlist_id , sp ):
        ids = []
        playlist = sp.user_playlist(user, playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            ids.append(track['id'])
        return ids

    def access_TOKEN(self):
        auth_response = requests.post(self.AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        # Convert response to JSON
        auth_response_data = auth_response.json()
        # Save the access token
        access_token = auth_response_data['access_token']
        # Need to pass access token into header to send properly formed GET request to API server
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        return auth_response.json() , headers

    def get_audio_feature(self , headers  ,track_id):
        BASE_URL = 'https://api.spotify.com/v1/'
        r = requests.get(BASE_URL + self.POST_query + track_id, headers=headers)
        return r.json()


    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def find_song_artist(self , track_name , sp):
        result = sp.search(q=track_name, limit=20)
        return result['tracks']['items'][0]['name']

    def find_artist_songs(self , artist_name , sp):
         result = sp.search(q = artist_name , limit = 20)
         return result
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def search(self, query, search_type='artist'):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        data = urllib.parse.urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

