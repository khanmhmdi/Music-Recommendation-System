import pickle
import numpy as np
import hdbscan


def load_model(path):
    return pickle.load(open(path, 'rb'))

def find_nearest_cluster(data , model ):
    test_labels, strengths = hdbscan.approximate_predict(model, np.array(data))
    return test_labels

def suggest_song(cluster_num , lables_path , df):
    suggestion_tracks_data = []
    lables = np.load(lables_path)
    song_index = np.where(lables==cluster_num)
    for i in song_index:
        suggestion_tracks_data.append(df.iloc[i])

    return suggestion_tracks_data


def find_nearest_cluster_outlier(point , model_path):
    test_lables= 0
    models = []
    for i in range(12):
        models.append(pickle.load(open(model_path+str(i) , 'rb')))
    while(test_lables==0):
        test_labels, strengths = hdbscan.approximate_predict(models[i], np.array(point))




