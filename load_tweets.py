from __future__ import division

"""
Interface to various twitter data sources -- on disk, db, and live twitter.
"""
import json

from tweet_normalization import normalize_and_tokenize_tweet

annotated_tweet_ids = set([])
    
def load_tweets_from_file( filepath, strip_annotations=False ):
    """
    `filepath` specifies a link to one-json-object-per-line
    """
    #If we are stripping annotations, bake it into the data load
    if strip_annotations:
        global annotated_tweet_ids
        if len(annotated_tweet_ids) < 1:
            #Executes only the first time, and populates the annotated tweets set
            from clpsych_2015_shared_task_experiments import load_annotated_tweet_ids
            annotated_tweet_ids = load_annotated_tweet_ids()
            
        def tweet_processor(x):
            """
            Takes a raw string, jsonifys it, normalizes it and tokenizes it,
            also strips out any of the tweets we have previously annotated
            """
            t = json.loads(x)
            if 'id' in t and not t['id'] in annotated_tweet_ids:
                return normalize_and_tokenize_tweet(t)

    #Otherwise just return all the tweets
    else:
        def tweet_processor(x):
            """
            Takes a raw string, jsonifys it, normalizes it and tokenizes it.
            """
            return normalize_and_tokenize_tweet(json.loads(x))
    
        
    IN = open(filepath)
    tweets = filter(None,map(tweet_processor, IN))
    return tweets

if __name__ == '__main__':
    """Run as standalone to test"""
    import os
    data_on_disk = 'data/anonymized_ptsd_tweets/'

    example_usernames = [x.split('.')[0] for x in os.listdir(data_on_disk)]

    print example_usernames
    
    for username in example_usernames:
        tweets = load_tweets_from_file(data_on_disk + username + '.tweets')
        print username, len(tweets)
    
