import pathlib
import sys
import os
import numpy as np
import pandas as pd
import Model
import pre_process_data
import spotify_API


def main(args) -> None:
    arg_list = args[1:]

    model_columns = ['danceability', 'energy', 'key', 'loudness', 'mode',
                     'speechiness', 'acousticness',
                     'instrumentalness', 'liveness', 'valence', 'tempo',
                     'duration_ms',
                     'time_signature']
    df = pd.read_csv('/home/mohamad/MusicRecommendationSystem/genres_v2.csv')

    track_features = df[model_columns][100:105]
    arg_list = args[1:]

    data_scaled = pre_process_data.UFS(np.asarray(track_features),4,4)
    client_id = input()
    client_secret = input()
    print(data_scaled)
    print(type(data_scaled))
    user_suggestion(client_id , client_secret , data_scaled ,df )


    if len(arg_list) == 0:
        print("Usage: python3 musicRecommender.py <csv file>")
        sys.exit()
    else:
        file_name = arg_list[0]
        if not os.path.isfile(file_name):
            print("File does not exist")
            sys.exit()
        else:
            userPreferences = pd.read_csv(file_name)

    # this code is just to check, delete later.
    print(userPreferences.head())



def find_audio_feature(track_id):
    track_features = []
    user = spotify_API.spotify_API('6a036371e3174307b476133ccd2142e7', 'e4d046580369456481b023ed09d65559')

    sp = user.start_connection(20)
    auth_response, headers = user.access_TOKEN()
    user.POST_query = 'audio-features/'
    # track_id = '7pgJBLVz5VmnL7uGHmRj6p'
    track_feature = user.get_audio_feature(headers, track_id)
    print("Loading track featrues")

    track_features.append(track_feature)
    columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
     'type', 'id', 'uri',
     'track_href',
     'analysis_url', 'duration_ms',
     'time_signature']
    print("track featrues loaded")
    model_columns = ['danceability', 'energy', 'key', 'loudness', 'mode',
                                                    'speechiness', 'acousticness',
                                                    'instrumentalness', 'liveness', 'valence', 'tempo',
                                                    'duration_ms',
                                                    'time_signature']
    track_feature_dataframe = pd.DataFrame(track_features, columns)
    print("kl"+str(len(track_feature_dataframe.index)))
    return track_feature_dataframe[model_columns]


def get_more_info(Client_ID , Client_Secret ,song_name):
    spotify = spotify_API.spotify_API(Client_ID , Client_Secret)
    # spotify = SpotifyAPI(Client_ID, Client_Secret)
    spotify.get_access_token()
    spotify.get_client_credentials()
    spotify.get_token_headers()
    spotify.get_token_data()
    spotify.perform_auth()
    spotify.get_access_token()
    spotify.get_resource_header()
    spotify.search({'track':song_name},search_type='track')


def user_suggestion(client_id , client_secret , track_feature , df):
    track_id_suggestion = {}

    model_path = ''
    model_path = pathlib.Path(model_path)
    model_loaded = Model.load_model(model_path)

    cluster_nums = Model.find_nearest_cluster(track_feature , model_loaded)


    for i in cluster_nums:
        # if i == -1 :
            # get_more_info(client_id ,client_secret )

        # else:
            result = []
            result.append(Model.suggest_song(i, 'PythonFile/lables.npy', df))
            track_id_suggestion[str(i)] = result



if __name__ == "__main__":
    main(['3lTAwJ7GAsm6mFkRejOXIm' , '2U03OmZKC7YIPkYBgJnJfA' , '3jnTBMdckWNzC7PJV96kQ1' , '164uPGiUKnYHwJOHcgfy1e'
             ,'6HXgExFVuE1c3cq9QjFCcU', '1j82fFDqVM2Sgb8tfMidBv',])


    # get arguments from command line
    # args = sys.argv
    # main(args)



