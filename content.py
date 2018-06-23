from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import csv
import re

class Content:
    def __init__(self, animes):
        self._animes = animes
        self._process()

    def _convGenre(self, genre):
        genre = str(genre).lower()
        return set(genre.split(', '))

    def _convName(self, name, chars):
        name = name.lower()
        name = re.sub('&#[0-9][0-9][0-9];', '', name)
        name = re.sub('[àâäă]', 'a', name)
        name = re.sub('[èéē]', 'e', name)
        name = re.sub('[üμ]', 'u', name)
        name = re.sub('ß', 'ss', name)
        name = re.sub('š', 's', name)
        name = re.sub('ö', 'o', name)
        name = re.sub(chars, ' ', name)
        return set(name.split())
    
    def _process(self):
        try:
            with open('data/processed.csv') as fl:
                processed = list(csv.reader(fl))
        except Exception:
            with open('data/words.csv') as fl:
                words = list(csv.reader(fl))[0]
            types = ['Movie', 'Music', 'ONA', 'OVA', 'Special', 'TV']
            genres = ['action', 'adventure', 'cars', 'comedy', 'dementia', 'demons', 
                'drama', 'ecchi', 'fantasy', 'game', 'harem', 'hentai', 
                'historical', 'horror', 'josei', 'kids', 'magic', 'martial arts', 
                'mecha', 'military', 'music', 'mystery', 'parody', 'police', 
                'psychological', 'romance', 'samurai', 'school', 'sci-fi', 'seinen',
                'shoujo', 'shoujo ai', 'shounen', 'shounen ai', 'slice of life', 
                'space', 'sports', 'super power', 'supernatural', 'thriller', 
                'vampire', 'yaoi', 'yuri']
            chars = '[' + "".join(['®', '°', '²', '³', '½', 'ψ', '“', '”', '†', '…', 
                'δ', '℃', '←', '→', '√', '∞', '␣', '◎', '◯', '★', '☆', '♡', '♥', 
                '♪', '♭', '＊', '\!', '\#', '\$', '\%', '\&', '\(', '\)', '\*', 
                '\+', '\,', '\-', '\.', '\/', '\:', '\;', '\=', '\?', '\@', '\[', 
                '\]', '\^', '\~']) + ']'
            
            processed = []
            for i, d in self._animes.iterrows():
                ws = self._convName(d['name'], chars)
                gs = self._convGenre(d['genre'])
                ts = d['type']
                processed.append([])
                processed[-1].extend([ 1 if w in ws else 0 for w in words])
                processed[-1].extend([ 1 if g in gs else 0 for g in genres])
                processed[-1].extend([ 1 if t == ts else 0 for t in types])
            
            with open('data/processed.csv', 'w') as fl:
                wcsv = csv.writer(fl)
                wcsv.writerows(processed)

        labels = [x[0] for x in self._animes.loc[:,['anime_id']].values]
        df = pd.DataFrame(cosine_similarity(processed), columns=labels)
        self._processed = df
    
    def get_similar(self, anime_id, user=None, size=10):
        df = self._processed.loc[:,[anime_id]]
        df.sort_values(by=anime_id, ascending=False, inplace=True)
        result = self._processed.columns[df.index[1:size+1]]
        if user is not None:
            aux = user.loc[:,(user==0).all()]
            result = self._processed.columns[df.index]
            result = result[result.isin(aux.columns)]
            if result[0] != anime_id:
                return(result[:size])
            else:
                return(result[1:size+1])
        return(self._processed.columns[df.index[1:size+1]])

# EXEMPLO DE ANIMES SIMILARES PARA DEATH_NOTE
# [1, 4037, 1022, 1226, 1293, 1490, 1184, 34502, 28145, 30016]
# animes = pd.read_csv('data/animes.csv')
# cols = animes['anime_id']
# user = pd.DataFrame([np.zeros(cols.shape[0], dtype=np.int32)], columns=cols)
# user.loc[[0], [4037]] = 1
# user.loc[[0], [1]] = 1
# print(Content(animes, None).get_similar(1, user))