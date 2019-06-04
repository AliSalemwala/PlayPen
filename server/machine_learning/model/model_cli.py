#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

YAVUZ ÇETİN ÖLÜMSÜZDÜR

@author: Mehmet
"""

import argparse

import numpy as np
import pickle

FULL_PATH_PREFIX = "./machine_learning/model/"

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
    clf = pickle.load(open(FULL_PATH_PREFIX+"model.pkl", 'rb'))
else:
    clf = pickle.load(open(model_path), 'rb')
    
# do the prediction print out to stdout
prediction = clf.predict(pred_list)
print(str(prediction[0]))

