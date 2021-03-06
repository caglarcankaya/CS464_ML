# Title: Bilkent University Fall 2018 CS464: Introduction to Machine Learning Homework 1
# Author: Berat Biçer, 21503050
# E-mail: beratbbicer@gmail.com
# Description: Building a Newsgroup Classifier with Naive Bayes
# Date: Nov. 4, 2018
# Location: Ankara, Turkey

import numpy as np

train_features = np.loadtxt("dataset/question-4-train-features.csv", dtype='i', delimiter=',')
train_labels = np.loadtxt("dataset/question-4-train-labels.csv", dtype='i', delimiter=',')
test_features = np.loadtxt("dataset/question-4-test-features.csv", dtype='i', delimiter=',')
test_labels = np.loadtxt("dataset/question-4-test-labels.csv", dtype='i', delimiter=',')

vocabulary_size = len(train_features[0])
N = len(train_features)
sum_T_j_y_zero = 0
sum_T_j_y_one = 0
N_one = 0
N_zero = 0

# 1 space, 0 medical

for i in range(N):
    if train_labels[i] == 0: # medical       
        N_zero = N_zero + 1
        sum_T_j_y_zero = sum_T_j_y_zero + train_features[i].sum(axis = 0)
    else: # space
        N_one = N_one + 1
        sum_T_j_y_one = sum_T_j_y_one + train_features[i].sum(axis = 0)

T_j_y_zero = np.zeros(vocabulary_size)
T_j_y_one = np.zeros(vocabulary_size)

sum_T_j_y_zero = sum_T_j_y_zero + vocabulary_size
sum_T_j_y_one = sum_T_j_y_one + vocabulary_size

for i in range(vocabulary_size):
    for j in range(N):
        if train_labels[j] == 0:
            T_j_y_zero[i] = T_j_y_zero[i] + train_features[j][i]
        else:
            T_j_y_one[i] = T_j_y_one[i] + train_features[j][i]

theta_j_y_zero = np.zeros(vocabulary_size)
theta_j_y_one = np.zeros(vocabulary_size)
for i in range(vocabulary_size):
    theta_j_y_zero[i] = float((T_j_y_zero[i] + 1) / sum_T_j_y_zero)
    theta_j_y_one[i] = float((T_j_y_one[i] + 1) / sum_T_j_y_one)

    if theta_j_y_zero[i] != 0:
        theta_j_y_zero[i] = np.log(theta_j_y_zero[i])

    if theta_j_y_one[i] != 0:
        theta_j_y_one[i] = np.log(theta_j_y_one[i])

correct_prediction_count = 0
for i in range(len(test_features)):
    weighted_theta_j_y_zero = float(0)
    weighted_theta_j_y_one = float(0)
    for j in range(vocabulary_size):
        weighted_theta_j_y_zero = weighted_theta_j_y_zero + float(theta_j_y_zero[j] * test_features[i][j])
        weighted_theta_j_y_one = weighted_theta_j_y_one + float(theta_j_y_one[j] * test_features[i][j])

    prediction_zero = np.log(float(N_zero / N)) + weighted_theta_j_y_zero
    prediction_one = np.log(float(N_one / N)) + weighted_theta_j_y_one
    prediction = 0 if prediction_zero >= prediction_one else 1
    correct_prediction_count = correct_prediction_count + 1 if prediction == test_labels[i] else correct_prediction_count

accuracy = float(correct_prediction_count / len(test_features))
print("Accuracy -> " + str(accuracy))
print("False predictions -> " + str(len(test_features) - correct_prediction_count))

# Mutual information between class variable and features
mi = {}
for i in range(vocabulary_size):
    N00 = float(0)
    N01 = float(0)
    N10 = float(0)
    N11 = float(0)
    for j in range(N):
        if train_features[j][i] == 0 and train_labels[j] == 0: # N00 or N01
            N00 = N00 + 1
        if train_features[j][i] == 0 and train_labels[j] != 0:
            N01 = N01 + 1
        if train_features[j][i] != 0 and train_labels[j] == 0:
            N10 = N10 + 1
        if train_features[j][i] != 0 and train_labels[j] != 0:
            N11 = N11 + 1
    
    first_term = float((N11 / N) * (np.log2(N * N11) - np.log2(N10 + N11) - np.log2(N01 + N11)))
    second_term = float((N01 / N) * (np.log2(N * N01) - np.log2(N00 + N01) - np.log2(N01 + N11)))
    third_term = float((N10 / N) * (np.log2(N * N10) - np.log2(N10 + N11) - np.log2(N00 + N10)))
    forth_term = float((N00 / N) * (np.log2(N * N00) - np.log2(N00 + N01) - np.log2(N00 + N10)))   
    mi[i] = float(first_term + second_term + third_term + forth_term)

sorted_mi = sorted(mi.items(), key = lambda kv: kv[1], reverse = True)
print(sorted_mi)