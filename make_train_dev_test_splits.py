"""
To be run once prior to the start of the shared task,
by the shared task administrators to create
the 10-fold train/dev/test splits.
These splits will be added to the github repo and shared.
"""

"""
This is the location of the downloaded data. Immediately under this
directory should be 'positive_ptsd_users/' etc.
"""
DATA_ROOT = './data/' #UPDATE for your setup, or create shell-scripts

TRAIN_DEV_TEST_ROOT = DATA_ROOT + 'clpsych_train_dev_test/'
import os
os.system('mkdir -p {0}'.format(TRAIN_DEV_TEST_ROOT))


#To shuffle all of them so they are in the same not alphabetical order
import random
random.seed(111612)

#NB: These will need to be revistited after we have age- and gender-matched controls --GAC
def load_positive_usernames_in_experiments(condition):
    usernames = [x.split('.')[0].strip() for x in os.listdir(DATA_ROOT+'anonymized_%s_tweets/' % condition)]
    random.seed(123212321)
    random.shuffle(usernames)
    return usernames

def load_control_usernames_in_experiments(count=1000):
    usernames = [x.split('.')[0].strip() for x in os.listdir(DATA_ROOT+'anonymized_control_tweets/') ]
    random.seed(123212321)
    random.shuffle(usernames)
    return usernames[:count]

usernames = {'control':load_control_usernames_in_experiments()}
for condition in ['ptsd','depression']:
    usernames[condition] = load_positive_usernames_in_experiments(condition)

NUM_FOLDS = 10
DEV_FOLDS = 4

for condition,names in usernames.items():
    fold_size = int(len(names) / NUM_FOLDS) #May lose some data if not checked
    for held_out_fold in range(NUM_FOLDS):
        #Dev folds are the two folds prior to the held_out_fold (wrapping)
        dev_folds = [x % NUM_FOLDS for x in range(held_out_fold - DEV_FOLDS, held_out_fold)]

        train_folds = list(set(range(NUM_FOLDS)) - set(dev_folds) - set([held_out_fold]))
        train_folds.sort()

        test_data = names[held_out_fold * fold_size : (held_out_fold + 1) * fold_size ]

        dev_data = []
        for dev_fold in dev_folds:
            dev_data += names[dev_fold * fold_size : (dev_fold + 1) * fold_size ]

        train_data = []
        for train_fold in train_folds:
            train_data += names[train_fold * fold_size : (train_fold + 1) * fold_size]
        

        
        def write_out( filename, fold_names ):
            OUT = open(TRAIN_DEV_TEST_ROOT + filename,'w')
            [OUT.write(str(x) + '\n') for x in fold_names]
            OUT.close()
        
        filename = '{0}_fold{1}_{2}.lst'.format( condition, held_out_fold, 'train' )
        write_out(filename, train_data)

        filename = '{0}_fold{1}_{2}.lst'.format( condition, held_out_fold, 'dev' )
        write_out(filename, dev_data)

        filename = '{0}_fold{1}_{2}.lst'.format( condition, held_out_fold, 'test' )
        write_out(filename, test_data)

    

