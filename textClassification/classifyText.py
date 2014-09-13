from collections import defaultdict 
from nltk import word_tokenize, wordpunct_tokenize
import nltk
from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer 
import numpy as np
from sklearn.cross_validation import KFold
from sklearn import metrics 
from textClassification.porter2 import stem
from sklearn.feature_selection import SelectKBest,chi2
from sklearn.feature_extraction.text import TfidfVectorizer 
import string 
import operator
import cPickle as pickle


def getFeatures(attraction,title,bodyText,labels,stopwords): 
    features = defaultdict() 
    for word in attraction: 
        features[('attraction_word',word)]=1
    titleCount=0
    for word in title: 
        if word.lower() not in stopwords: 
            features[('title_word',word.lower())]=1
            if word.lower() in labels:
                features[('title_label',word.lower())]=1
            if titleCount==0:d
                features[('first_word',word)]=1
        titleCount+=1
    counter = 0
    previousWord = ''
    for word in bodyText: 
        if word.lower() not in stopwords and word not in string.punctuation: 
            features[('body_word',word)]=1
            features[('body_word_stemmed',stem(word).lower())]=1
            # if postags[counter][1]=='JJ':
            #   features[('body_jj',word)]=1
            # if postags[counter][1]=='NN':
            #   features[('body_nn',word)]=1
            if word.lower() in labels:
                features[('body_label',word.lower())]=1
            # if counter != 0:
            #   features[('bigram',previousWord.lower()+word.lower())]=1
            previousWord=word
            # for key,value in gazeteer.iteritems():
            #   if word.lower() in value: 
            #       features[(key+'gazeteer',word.lower())]=1

        counter+=1
    features[('length_review',len(bodyText))]=1
    return features

annotations_file = open('Annotations.tsv')
annotations_dict = defaultdict(lambda: defaultdict())
features_dict = []
true_labels = [] 
counter=0
labels = ['Fun','Social','Adventurous','Lazy','Hungry','Natural','Cultural','Education','Historical','Luxurious']
stopwords = [] 
gazeteer = defaultdict(lambda:defaultdict(int))
gazeteer_sorted = defaultdict(list)
# corpus=[]
for line in open('stopwords'):
    stopwords.append(line.strip())

for line in annotations_file:
    if counter>0:
        line = line.split('\t') 
        annotations_dict[counter]['attraction']=word_tokenize(line[0])
        annotations_dict[counter]['title']=word_tokenize(line[1])
        tokenized_review = word_tokenize(line[2])
        annotations_dict[counter]['review']=tokenized_review
        annotations_dict[counter]['category']=line[3].strip()
        # print line[2]
        # annotations_dict[counter]['postag']=nltk.pos_tag(tokenized_review)
        # print annotations_dict[counter]['postag']
        # print 'here'
        # corpus.append(tokenized_review)
    counter+=1

for key,value in annotations_dict.iteritems():
    for word in value['review']:
        if word.lower() not in stopwords and word not in string.punctuation: 
            gazeteer[value['category']][word.lower()]+=1

for key,value in gazeteer.iteritems():
    gazeteer_sorted[key] = sorted(value.iteritems(), key=operator.itemgetter(1),reverse=True)
    gazeteer_sorted[key] = [x[0] for x in gazeteer_sorted[key][:50]]
    
for key,value in annotations_dict.iteritems():
    features_dict.append(getFeatures(value['attraction'],value['title'],value['review'],labels,stopwords))
    true_labels.append(value['category'])

clf = LinearSVC()
vec = DictVectorizer()
# vectorizer = TfidfVectorizer(min_df=1)
number_of_reviews = len(true_labels)
features_dict_np = vec.fit_transform(features_dict)
''' Selecting K Best features ''' 
selector = SelectKBest(chi2, k=450)
true_labels_np = np.array(true_labels)
features_dict_np = selector.fit_transform(features_dict_np, true_labels_np)

save_object = raw_input('Press 1 for ten fold or 2 for saving classifier')
save_object = int(save_object)
if save_object == 1: 
    # running list of test and true 
    runningY_true = np.empty([2,2])
    runningY_predicted = np.empty([2,2])

    # 10 fold cross validation
    skf = KFold(n=number_of_reviews, n_folds=10,shuffle=True)
    count=0
    for train, test in skf: 
        print 'Testing fold',count

        # getting the training and test sets for this fold 
        X_train = features_dict_np[train]
        y_train = true_labels_np[train]
        X_test = features_dict_np[test]
        y_test = true_labels_np[test]

        if count==0:
            runningY_true=y_test
        else:
            # update runningY_true 
            runningY_true=np.append(runningY_true,y_test)
        # print runningY_true
        # train classifier using training set
        clf.fit(X_train,y_train)

        # classify test set
        predictedClass = clf.predict(X_test)

        if count==0:
            runningY_predicted=predictedClass
        else: 
            # update runningY_predicted 
            runningY_predicted=np.append(runningY_predicted,predictedClass)
        count+=1

    for y in runningY_true:
        if y not in labels:
            print y

    print metrics.classification_report(runningY_true, runningY_predicted,    target_names=labels)
else: 
    pickleFile = open('classifier.pkl','wb')
    clf.fit(features_dict_np,true_labels_np)
    pickle.dump(clf, pickleFile, pickle.HIGHEST_PROTOCOL)
    pickleFile.close()
