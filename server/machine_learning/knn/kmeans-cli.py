#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

YAVUZ ÇETİN ÖLÜMSÜZDÜR

@author: Mehmet
"""

import argparse

import numpy as np
import pickle
import sys

FULL_PATH_PREFIX = "./machine_learning/knn/"

# create an argument parser
parser = argparse.ArgumentParser(description='Command line tooling for making predictions')
# add related arguments there
parser.add_argument('--predict', nargs='+', help='The prediction matrix to pass', required=True, dest='pred_list')
parser.add_argument('--model-path', help='Path to the model', dest='model_path')
# parse the actual arguments
args = parser.parse_args()
# convert to numpy array
pred_list = [float(n) for n in args.pred_list]
pred_list = np.array(pred_list).reshape(1, -1)

# check if the model path is specified
model_path = args.model_path
# load the model
if model_path is None:
    kmeans = pickle.load(open(FULL_PATH_PREFIX + "model.pkl", 'rb'))
    #kmeans = pickle.load(open("model.pkl", 'rb'))
else:
    kmeans = pickle.load(open(model_path), 'rb')
    
# do the prediction print out to stdout
prediction = kmeans.predict(pred_list)
#print(str(prediction))
# load the mapping

pickle_in = open(FULL_PATH_PREFIX+"markov_mapping.pkl","rb")
#pickle_in = open("markov_mapping.pkl","rb")

markov_mapping = pickle.load(pickle_in)
# load the markov_malign_new
from tempfile import TemporaryFile
infile = TemporaryFile()

markov_malign_new = np.load(FULL_PATH_PREFIX+"array.npy")
#markov_malign_new = np.load("array.npy")

# get everything with the required label

str_names = ""
str_distances = ""


def L2(x, y):
    return np.linalg.norm(x-y, axis=1)**2

#print(markov_mapping.items())

#print('****************************************************')
#print("\n\n\n")

#for k, v in markov_mapping.items():
 #   print(k)
  #  print(v)
   # print("\n")

distances_dictionary = list()


for k, v in markov_mapping.items():
    if v[1] == prediction[0]:
        distance = L2(pred_list, v[0].reshape(1, -1))
        if distance != 0:
            distances_dictionary.append( (k, distance) )


distances_dictionary.sort(key=lambda tup: tup[1][0])

largest_dist = distances_dictionary[-1][1][0] + 1


for i in range(0, 10):
    (name, dist) = distances_dictionary[i]
    sim_val = largest_dist - dist[0]
    str_names = str_names + name + ":"
    str_distances = str_distances + str(sim_val) + ":"
    #str_distances = str_distances + str(dist[0]) + ":"
        
final_output = str_names + str_distances
final_output = str(prediction[0]) + ":" + final_output

print( final_output)