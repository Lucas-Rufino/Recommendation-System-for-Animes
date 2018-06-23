import pandas as pd

animes = pd.read_csv('data/animes.csv')
ratings = pd.read_csv('data/ratings.csv')
ratings = pd.pivot_table(ratings, 'rating', 'user_id', 'anime_id', fill_value=0)