from __future__ import division

"""
General cross-validation functions and some
specifically implemented for the CLPsych2 Shared task
"""

def run_cross_validation_experiment( df, label_name, excluded_columns=set([]),
                                     n_folds=10, n_jobs=1,
                                     svm_kernel_types=['linear','rbf','sigmoid'] ):
    """
    Run the crossfold validation experiments via
    scikitlearn's internal functions
    `df` is a pandas dataframe full of the data to predict
    `label_name` is the header in `df` which has the label to be predicted
    `excluded_columns` will remove those columns from the df before creating the feature vectors.
    `n_folds` indicates the number of cross validation folds to run.
    `n_jobs` specifies the number of jobs to run in parallel
    `svm_kernel_types` is a list of kernels to try in the svm
    """
    from sklearn import grid_search, svm, linear_model
    from sklearn.cross_validation import cross_val_score

    #Wrangle the DataFrame into what SKL expects, pull labels out of the vector too
    labels = df[label_name].values
    columns = set(list(df)) - set(excluded_columns) - set([label_name]) #Pull out the label we're training for
    print columns
    print labels
    features = df[list(columns)].values

    """
    print "Starting SVM grid search..."
    svm_parameters = {'kernel':svm_kernel_types, 'C':[1, 10]}
    svr = svm.SVC()
    gridsearch = grid_search.GridSearchCV(svr, svm_parameters)
    scores = cross_val_score(gridsearch, features, labels, n_jobs=2, cv=n_folds)
    print scores

    """
    print "Starting logistic regression grid search..."
    #logistic = linear_model.LogisticRegression(class_weight='auto')
    logistic = linear_model.LogisticRegression()
    #logistic_parameters = {'C':[1e5,10,1],'class_weight':['auto',None],'penalty':['l1','l2']}
    logistic_parameters = {'C':[1e5,10,1],'penalty':['l1','l2']}
    gridsearch = grid_search.GridSearchCV(logistic, logistic_parameters)
    scores = cross_val_score(gridsearch, features, labels, n_jobs=2, cv=n_folds)
    print scores


    
if __name__ == '__main__':
    """Run this standalone to test it"""
    from extract_feature_vector import load_feature_vectors

    df = load_feature_vectors('test_feature_vector_writer.csv')

    run_cross_validation_experiment( df, 'ulm_ptsd_dec', excluded_columns=['ulm_ptsd_score'],n_folds=10, svm_kernel_types=['rbf','linear'])
    
    
    
    
