from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import database

class Collaborative:
    def __init__(self, animes, ratings):
        self._animes = animes
        self._ratings = ratings
    
    def get_similar_by_user(self, user, ):
        zeros = np.zeros(len(self._ratings.columns))
        aux = pd.DataFrame([zeros], columns=self._ratings.columns)
        aux.loc[[0],:] = user.loc[[0], aux.columns].sub(5).values
        cs = cosine_similarity(aux, self._ratings)
        users = pd.DataFrame(cs, columns=self._ratings.index)
        user.sort_values(by=0, axis=1, ascending=False)



# ctx = Collaborative(database.animes, database.ratings)
database.user.loc[[0], [32281]] = 9
print(database.user.loc[[0],:].sub(5).values)
# print('ok')
# ctx.get_similar_by_user(database.user)