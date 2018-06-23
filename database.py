import pandas as pd
import numpy as np

animes = pd.read_csv('data/animes.csv')
ratings = pd.read_csv('data/ratings.csv')
ratings = pd.pivot_table(ratings, 'rating', 'user_id', 'anime_id', fill_value=0)
user = pd.DataFrame([np.zeros(animes['anime_id'].shape[0], dtype=np.int32)], 
    columns=animes['anime_id'])