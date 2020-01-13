# -*- coding: utf-8 -*-
"""naive_bayes.ipynb

Automatically generated by Colaboratory.

This is a eMail Spam Classifers that uses Naive Bayes supervised machine learning algorithm.
"""

import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

"""This function builds a Dictionary of most common 3000 words from all the email content. First it adds all words and symbols in the dictionary. Then it removes all non-alpha-numeric characters and any single character alpha-numeric characters. After this is complete it shrinks the Dictionary by keeping only most common 3000 words in the dictionary. It returns the Dictionary."""

def make_Dictionary(root_dir):
  all_words = []
  emails = [os.path.join(root_dir,f) for f in os.listdir(root_dir)]
  for mail in emails:
    with open(mail) as m:
      for line in m:
        words = line.split()
        all_words += words
  dictionary = Counter(all_words)
  list_to_remove = list(dictionary)

  for item in list_to_remove:
    if item.isalpha() == False:
      del dictionary[item]
    elif len(item) == 1:
      del dictionary[item]
  dictionary = dictionary.most_common(3000)
  return dictionary

"""This function extracts feature columns and populates their values (Feature Matrix of 3000 comumns and rows equal to the number of email files). The function also analyzes the File Names of each email file and decides if it's a Spame or not based on the naming convention. Based on this the function also creates the Labelled Data Column. This function is used to extract the training dataset as well as the testing dataset and returns the Feature Dataset and the Label column."""

def extract_features(mail_dir):
  files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
  features_matrix = np.zeros((len(files),3000))
  train_labels = np.zeros(len(files))
  count = 1;
  docID = 0;
  for fil in files:
    with open(fil) as fi:
      for i, line in enumerate(fi):
        if i ==2:
          words = line.split()
          for word in words:
            wordID = 0
            for i, d in enumerate(dictionary):
              if d[0] == word:
                wordID = i
                features_matrix[docID,wordID] = words.count(word)
      train_labels[docID] = 0;
      filepathTokens = fil.split('/')
      lastToken = filepathTokens[len(filepathTokens)-1]
      if lastToken.startswith("spmsg"):
        train_labels[docID] = 1;
        count = count + 1
      docID = docID + 1
  return features_matrix, train_labels

"""The section is the main Program that calls the above two functions and gets executed first. First it "trains" the model using model.fit function and Training Dataset. After that it scores the Test Data set by running the Trained Model with the Test Data set. At the end it prints the model performance in terms of accuracy score."""

TRAIN_DIR = '/content/drive/My Drive/MSBA_Colab_2020/ML Algorithms/Naive_Bayes/train-mails'
TEST_DIR = '/content/drive/My Drive/MSBA_Colab_2020/ML Algorithms/Naive_Bayes/test-mails'

dictionary = make_Dictionary(TRAIN_DIR)

print ("reading and processing emails from TRAIN and TEST folders")
features_matrix, labels = extract_features(TRAIN_DIR)
test_features_matrix, test_labels = extract_features(TEST_DIR)

model = GaussianNB()

print ("Training Model using Gaussian Naibe Bayes algorithm .....")
model.fit(features_matrix, labels)
print ("Training completed")
print ("testing trained model to predict Test Data labels")
predicted_labels = model.predict(test_features_matrix)
print ("Completed classification of the Test Data .... now printing Accuracy Score by comparing the Predicted Labels with the Test Labels:")
print (accuracy_score(test_labels, predicted_labels))

"""======================= END OF PROGRAM ========================="""