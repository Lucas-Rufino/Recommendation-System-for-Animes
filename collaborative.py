from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import database

class Collaborative:
    def __init__(self, animes, ratings):
        self._users = None
        self._animes = animes
        self._ratings = ratings
    
    def process(self, user):
        zeros = np.zeros(len(self._ratings.columns))
        aux = pd.DataFrame([zeros], columns=self._ratings.columns)
        aux.loc[[0],:] = user.loc[[0], aux.columns].values
        cols = user.loc[:,(user==0).all()].columns              # melhoram em
        aux = aux.loc[:,~aux.columns.isin(cols)]                # tempo, mas
        ratings = self._ratings.loc[:,~aux.columns.isin(cols)]  # modificam um 
        #ratings = self._ratings                                # o resultado
        cs = cosine_similarity(aux, ratings)
        self._users = pd.DataFrame(cs, columns=ratings.index)
        self._users.sort_values(by=0, axis=1, ascending=False, inplace=True)

    def get_similar_by_user(self, user=None, size=10, k=10):
        users = self._users.iloc[:,:k]
        similarity = users.iloc[[0],:].values[0]
        ratings = self._ratings.loc[users.columns,:].T.mul(similarity)
        ratings = ratings.sum(axis=1).div(similarity.sum())
        ratings.sort_values(axis=0, ascending=False, inplace=True)
        ratings = pd.DataFrame([ratings.values], columns=ratings.index)
        if user is not None:
            aux = user.loc[:,(user==0).all()]
            return ratings.columns[ratings.columns.isin(aux.columns)][:size]
        return ratings.index[:size]
    
    def get_similar_by_anime(self, anime_id, user=None, size=10, k=10):
        anime_users = self._ratings.loc[self._ratings[anime_id] > 0,[anime_id]]
        users = self._users.loc[:,anime_users.index]
        users = users.iloc[:,:k]
        similarity = users.iloc[[0],:].values[0]
        ratings = self._ratings.loc[users.columns,:].T.mul(similarity)
        ratings = ratings.sum(axis=1).div(similarity.sum())
        ratings.sort_values(axis=0, ascending=False, inplace=True)
        ratings = pd.DataFrame([ratings.values], columns=ratings.index)
        if user is not None:
            aux = user.loc[:,(user==0).all()]
            return ratings.columns[ratings.columns.isin(aux.columns)][:size]
        return ratings.index[:size]