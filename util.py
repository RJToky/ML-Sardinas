import joblib
import os
from Levenshtein import distance

def count_char(char, language_list):
    counts = []
    for binary_string in language_list:
        counts.append(binary_string.count(char))
    return sum(counts)

def levenshtein_mean(language_list):
    list_distance = []
    for i in range(len(language_list)):
        for j in range(i, len(language_list)):
            list_distance.append(distance(language_list[i], language_list[j]))
    return sum(list_distance) / len(list_distance)

def str_list(language_list):
    output = ''
    for item in language_list:
        output += item + ','
    return output[:-1]

def transition_0_1(word):
    temp = 0
    output = 0
    for c in word:
        if c == '0':
            temp = 1
        if temp > 0:
            if c == '1':
                output += 1
                temp = 0
    return output

def transition_1_0(word):
    temp = 0
    output = 0
    for c in word:
        if c == '1':
            temp = 1
        if temp > 0:
            if c == '0':
                output += 1
                temp = 0
    return output

MODEL_FOLDER = "./models"
def dump_model(model) : 
    size = len(os.listdir(MODEL_FOLDER))
    version = size + 1
    joblib.dump(model, MODEL_FOLDER+'/model-'+str(version)+'.pkl')

def load_model():
    last_version = len(os.listdir(MODEL_FOLDER))
    return joblib.load(MODEL_FOLDER+'/model-'+str(last_version)+'.pkl')
