"""
A place to specify a lot of experiment-specific parameters so
their imports can be somewhat modularized.
"""
CODE_ROOT = './' #UPDATE to reflect your local setup

DATA_ROOT = 'data/' #UPDATE to reflect your local setup
GENERIC_CONDITION_ROOT = DATA_ROOT+'anonymized_%s_tweets/'
CONTROL_ROOT = GENERIC_CONDITION_ROOT % 'control'
PTSD_ROOT = GENERIC_CONDITION_ROOT % 'ptsd'
DEPRESSION_ROOT = GENERIC_CONDITION_ROOT % 'depression'

TRAIN_DEV_TEST_ROOT = DATA_ROOT + 'clpsych_train_dev_test/'

NUM_FOLDS=10

#To shuffle all of them so they are in the same not alphabetical order
import random


def load_usernames(condition, fold, data_set):
    filepath = TRAIN_DEV_TEST_ROOT + '{0}_fold{1}_{2}.lst'.format( condition,
                                                                   fold,
                                                                   data_set)
    names = [x.strip() for x in open(filepath)]
    return names

usernames_by_fold = [] #Provides the usernames for each condition, data set and test fold
for fold in range(NUM_FOLDS):
    usernames = {}
    for condition in ['ptsd','depression','control']:
        for data_set in ['train','dev','test']:
            usernames[ (condition,data_set) ] = load_usernames(condition,fold,data_set)
    usernames_by_fold.append(usernames)

def train_dev_test_usernames(fold,condition):
    return [ usernames_by_fold[fold][(condition,d)] for d in ['train','dev','test']]

import json
def load_annotated_tweet_ids():
    #TODO update this to reflect the anonymized IDs -- GAC has to do this
    annotation_json_loc = '/home/hltcoe/gcoppersmith/arbre/experiments/mental_health/'#HARDCODE
    import os
    fl = os.listdir(annotation_json_loc)
    filenames = filter(lambda x: x.startswith('annotated') and x.endswith('.json'),fl)

    tweet_ids = set([])
    for f in filenames:
        for raw in open(annotation_json_loc + f):
            tweet = json.loads(raw) 
            if 'id' in tweet:
                tweet_ids.add(tweet['id'])
    return tweet_ids
    
            
