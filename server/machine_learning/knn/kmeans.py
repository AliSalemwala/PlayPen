#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

YAVUZ ÇETİN ÖLÜMSÜZDÜR

@author: Mehmet
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

YAVUZ ÇETİN ÖLÜMSÜZDÜR

@author: Mehmet
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn import svm
import pickle
from sklearn.cluster import KMeans

y = list()

for i in range(1450):
    y.append(1)


kmeans = KMeans(n_clusters=10, random_state=0).fit(markov_malign_new)

pickle_out = open("model.pkl","wb")
pickle.dump(kmeans, pickle_out)

from tempfile import TemporaryFile

outfile = TemporaryFile()
np.save(outfile, markov_malign_new)


prediction = kmeans.predict(markov_malign[0].reshape(1, -1))

# gather everything in a dictionary
f = open('malware_files_data.dms', 'r').read().split('\n')[:-2]
ids = [i for i in range(0, len(f))]
tupled_hash = list(zip(ids, f))
file_to_id_hash = dict(tupled_hash)

names = list(file_to_id_hash.values())


markov_mapping = dict()
labels = kmeans.labels_

for i in range(markov_malign_new.shape[0]):
    tmp = list()
    tmp.append(markov_malign_new[i,])
    tmp.append(labels[i])
    
    markov_mapping[names[i]] = tmp


pickle_out = open("markov_mapping.pkl","wb")
pickle.dump(markov_mapping, pickle_out)

distances = dict()

for k, v in markov_mapping.items():
    if v[1] == prediction[0]:
        distances[k] = L2(markov_malign[0], v[0].reshape(1, -1))
        


def L2(x, y):
    return np.linalg.norm(x-y, axis=1)**2
