from __future__ import division
import csv,sys,codecs,json


import re
URL_ex = re.compile(ur"http[s]{0,1}://\S+", re.UNICODE)
username_ex = re.compile(ur"@[a-zA-Z_1-9]+", re.UNICODE)

text_ex = re.compile(ur"[\w'#@]+", re.UNICODE)
text_URL_ex = re.compile(ur"http[s]{0,1}://\S+|[\w'#@]+", re.UNICODE)
strip_ex = re.compile(ur"http[s]{0,1}://\S+|[ ,.\"!:;\-&*\(\)\[\]]",re.UNICODE)
def tokenize( s, as_set=False ):
    if s:
        #return text_URL_ex.findall(s)
        if as_set:
            #return list(set(text_URL_ex.findall(s.strip())))
            return list(set(filter(None,[x.strip() for x in strip_ex.split(s.strip())])))
        else:
            #return text_URL_ex.findall(s.strip())
            return filter(None,[x.strip() for x in strip_ex.split(s.strip())])
    else:
        return []

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)
    
def normalize( s ):
    try:
        #a = unicode(s,'unicode-escape')
        a = unicode(s)
        ####a = a.encode('utf-8','replace')
        a = a.encode('utf-8')
    except UnicodeDecodeError, TypeError:
        print "problem on unicode decode:", s
        import sys
        sys.exit()
        return ""
    s_prime = s.replace(u'\u201d','"')
    s_prime = s_prime.replace(u'\u201c','"')
    final_string = unicode(s_prime).encode('utf-8').lower()
    return final_string

import codecs,unidecode
def clean_tweet(text):
    normalized = re.sub(URL_ex, '*', normalize(text))
    normalized = re.sub(username_ex, '@', normalized)
    return unidecode.unidecode(normalized)

def normalize_and_tokenize_tweet( tweet ):
    if 'text' in tweet and tweet['text']:
        tweet['clean_text'] = clean_tweet( tweet['text'])
        tweet['tokens'] = tweet['clean_text'].split() #Simple tokenizer, much room for improvement
    return tweet
        
