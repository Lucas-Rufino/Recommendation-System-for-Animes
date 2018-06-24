import pandas as pd
import numpy as np

try:
    animes = pd.read_hdf('data/database/animes.h5', key='animes')
except Exception:
    animes = pd.read_csv('data/animes.csv')
    animes.to_hdf('data/database/animes.h5', key='animes')

try:
    ratings = pd.read_hdf('data/database/ratings.h5', key='ratings')
except Exception:
    ratings = pd.read_csv('data/ratings.csv')
    ratings = pd.pivot_table(ratings,'rating','user_id','anime_id',fill_value=0)
    ratings.to_hdf('data/database/ratings.h5', key='ratings')

user = pd.DataFrame([np.zeros(animes['anime_id'].shape[0], dtype=np.int32)], 
    columns=animes['anime_id'])