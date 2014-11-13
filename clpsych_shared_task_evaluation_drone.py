#!/export/apps/bin/python

from __future__ import division

"""
This houses all the specific nitty-gritty for running the shared task
learning and evaluation procedures so number are maximally comparable.

We built this for a parallel environment (e.g. SunGridEngine), but
it should be lightweight enough to run the 10 folds sequentially.
"""
import sys
#TODO: Improve argument parsing


from clpsych_2015_shared_task_experiments import train_dev_test_usernames
from clpsych_2015_shared_task_experiments import GENERIC_CONDITION_ROOT, CONTROL_ROOT
from load_tweets import load_tweets_from_file as tweets_from_username

condition = sys.argv[1]
fold = int(sys.argv[2])
output_dir = sys.argv[3]

#Make sure the output path exists
import os
os.system('mkdir -p '+output_dir)

output_path = output_dir + '{0}_fold{1}_results.csv'.format( condition,
                                                             fold)

pos_train_names,pos_dev_names,pos_test_names = train_dev_test_usernames(fold, condition)
positive_names = {}
positive_names['train'] = pos_train_names
positive_names['dev'] = pos_dev_names
positive_names['test'] = pos_test_names

neg_train_names,neg_dev_names,neg_test_names = train_dev_test_usernames(fold, 'control')
negative_names = {}
negative_names['train'] = neg_train_names
negative_names['dev'] = neg_dev_names
negative_names['test'] = neg_test_names

#HARDCODE DEBUG
"""
for dataset in ['train','dev','test']:
    negative_names[dataset] = negative_names[dataset][:15]
    positive_names[dataset] = positive_names[dataset][:15]
    """
#END DEBUG


#Load the data
pos_root = GENERIC_CONDITION_ROOT % condition
def tweets_from_pos_name_gen(username):
    return tweets_from_username(pos_root + username + '.tweets', strip_annotations=True)
neg_root = CONTROL_ROOT
def tweets_from_neg_name_gen(username):
    return tweets_from_username(neg_root + username + '.tweets', strip_annotations=True)

#Actually load the twitter data, retaining only the texts
positive_texts = {}
for data_set,usernames in positive_names.items():
    texts = [" ".join([t['clean_text'] for t in tweets_from_pos_name_gen(u) if 'clean_text' in t]) for u in usernames]
    positive_texts[data_set] = texts

negative_texts = {}
for data_set,usernames in negative_names.items():
    texts = [" ".join([t['clean_text'] for t in tweets_from_neg_name_gen(u) if 'clean_text' in t]) for u in usernames]
    negative_texts[data_set] = texts

#Do training on the language of the training tweets
training_tweets = [ ('pos',t) for t in positive_texts['train']] + \
                  [ ('neg',t) for t in negative_texts['train']]


#HEre is where we train, sadly this code isn't immediately shareable (and Rube Goldbergesque to boot!).
#Theoretically this should be able to use any scikitlearn stuff. I'll work to get the LMs to a better state to share. --GAC
#ngm = train_from_strings(training_tweets)

    
#Do some fusion learning on examples and scores
print "Extracting training vectors"
positive_train_fvs = []
negative_train_fvs = []
from extract_feature_vector import extract_feature_pipeline as pipeline
for tweets in (tweets_from_pos_name_gen(u) for u in positive_names['dev']): #Train?
    sparse_fv = pipeline(tweets,sparse=True)
    text = " ".join([t['clean_text'] for t in tweets if 'clean_text' in t and not '*' in t['clean_text']])
    print ngm.score(text, sort_it=False)
    lm_fv = {'language_model':ngm.score(text, sort_it=False)[0][1]}
    sparse_fv = dict(sparse_fv.items() + lm_fv.items())
    positive_train_fvs.append(sparse_fv)
for tweets in (tweets_from_neg_name_gen(u) for u in negative_names['dev']): #Train?
    sparse_fv = pipeline(tweets,sparse=True)
    text = " ".join([t['clean_text'] for t in tweets if 'clean_text' in t and not '*' in t['clean_text']])
    lm_fv = {'language_model':ngm.score(text, sort_it=False)[0][1]}
    sparse_fv = dict(sparse_fv.items() + lm_fv.items())
    negative_train_fvs.append(sparse_fv)

#Get all the possible values so we can order and unsparsify the feature vectors
all_fvs = negative_train_fvs + positive_train_fvs
all_keys = set()
for fv in all_fvs:
    all_keys = all_keys.union(fv.keys())
all_keys = sorted(list(all_keys))

def densify_fv(fv):
    return [fv.get(k,0) for k in all_keys]

neg_train_fvs = map(densify_fv, negative_train_fvs)
pos_train_fvs = map(densify_fv, positive_train_fvs)

#Actually do the training
from sklearn.linear_model import LogisticRegression
answers = ['pos'] * len(pos_train_fvs) + ['neg'] * len(neg_train_fvs)
fusion_model = LogisticRegression()
fusion_model.fit( pos_train_fvs + neg_train_fvs, answers)



#Score the test users
positive_test_fvs = []
for tweets in (tweets_from_pos_name_gen(u) for u in positive_names['test']):
    sparse_fv = pipeline(tweets,sparse=True)
    text = " ".join([t['clean_text'] for t in tweets if 'clean_text' in t and not '*' in t['clean_text']])
    #lm_fv = {'language_model':ngm.predict_proba(text)[0]}
    lm_fv = {'language_model':ngm.score(text, sort_it=False)[0][1]}
    sparse_fv = dict(sparse_fv.items() + lm_fv.items())
    positive_test_fvs.append(sparse_fv)

negative_test_fvs = []
for tweets in (tweets_from_neg_name_gen(u) for u in negative_names['test']):
    sparse_fv = pipeline(tweets,sparse=True)
    text = " ".join([t['clean_text'] for t in tweets if 'clean_text' in t and not '*' in t['clean_text']])
    lm_fv = {'language_model':ngm.score(text, sort_it=False)[0][1]}
    #lm_fv = {'language_model':ngm.predict_proba(text)[0]}
    sparse_fv = dict(sparse_fv.items() + lm_fv.items())
    negative_test_fvs.append(sparse_fv)

pos_test_fvs = map(densify_fv,positive_test_fvs)
neg_test_fvs = map(densify_fv,negative_test_fvs)

#Predictions from the classifier -- almost always junk
pos_labels = [x[0] for x in map(fusion_model.predict,pos_test_fvs)]
neg_labels = [x[0] for x in map(fusion_model.predict,neg_test_fvs)]

#Probability of being positive -- more likely to be useful (after we jigger the threshold)
pos_scores = [x[0][1] for x in map(fusion_model.predict_proba,pos_test_fvs)]
neg_scores = [x[0][1] for x in map(fusion_model.predict_proba,neg_test_fvs)]

print 'pos:',pos_labels, pos_scores
print 'neg:',neg_labels, neg_scores

num_pos_correct = len(filter(lambda x: x=='pos', pos_labels))
num_neg_correct = len(filter(lambda x: x=='neg', neg_labels))

num_condition_correct = num_pos_correct
prop_condition_correct = num_pos_correct / len(pos_test_fvs)
num_control_correct = num_neg_correct
prop_control_correct = num_neg_correct / len(neg_test_fvs)

#Write results to a file or DB
header = "condition,fold,num_condition_correct,prop_condition_correct,num_control_correct,prop_control_correct".split(",")
results = [condition,fold,num_condition_correct,prop_condition_correct,
           num_control_correct,prop_control_correct]
print results

import csv
#File locking or databasing the results seem to be non generic enough for the Hackathon, so we opt for the stone-cold simple solution with a post-processing reduce step.
OUT = open(output_path,'w')
CSV = csv.writer(OUT)
CSV.writerow(header)
CSV.writerow(results)
#Breaking the CSV conventions for the moment to write out all the scores
#Perhaps this whole thing shoudl be in more JDB type format, since we will post-process them into a single CSV later anyhow
CSV.writerow(['pos_scores',pos_scores])
CSV.writerow(['neg_scores',neg_scores])
OUT.close()



