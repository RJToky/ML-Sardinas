import random
import pandas as pd
from sardinas import *
from sklearn.ensemble import RandomForestClassifier
from util import *
from sklearn.metrics import accuracy_score

def generate_word(): 
    word_size = random.randint(1, 7)
    chars = "01"
    result = [chars[random.randint(0,len(chars)-1)] for i in range(word_size)]
    return str().join(result)

def generate_language():
    random_size = random.randint(1, 10)
    result = [generate_word() for i in range(random_size)]
    return list(set(result))

def generate_info_language(language_list): 
    word_min = len(min(language_list, key=len))
    word_max = len(max(language_list, key=len))
    word_average = sum([len(word) for word in language_list]) / len(language_list)
    nbr_1 = count_char("1", language_list)
    nbr_0 = count_char("0", language_list)
    transition_0_1_mean = sum([transition_0_1(word) for word in language_list]) / len(language_list)
    transition_1_0_mean = sum([transition_1_0(word) for word in language_list]) / len(language_list)
    _levenshtein_mean = levenshtein_mean(language_list)

    data = {
        'word_min': [word_min],
        'word_max': [word_max],
        'word_average': [word_average],
        'nbr_1': [nbr_1],
        'nbr_0': [nbr_0],
        'transition_0_1_mean': [transition_0_1_mean],
        'transition_1_0_mean': [transition_1_0_mean],
        'levenshtein_mean': [_levenshtein_mean]
    }
    return data

def generate_pandas_data_frame(data_size):
    data_is_code = []
    data_is_not_code = []

    while len(data_is_code) < int(data_size/2):
        language = generate_language()
        if is_code_by_sardinas(language):
            data_is_code.append(language)
    
    while len(data_is_not_code) < data_size-len(data_is_code):
        language = generate_language()
        if not is_code_by_sardinas(language):
            data_is_not_code.append(language)

    randomized_data = data_is_code + data_is_not_code

    info_data = None
    word_min = []
    word_max = []
    word_average = []
    nbr_1 = []
    nbr_0 = []
    transition_0_1_mean = []
    transition_1_0_mean = []
    _levenshtein_mean = []
    _is_code = []

    for language in randomized_data : 
        info_data = generate_info_language(language)
        word_min.append(info_data['word_min'][0])
        word_max.append(info_data['word_max'][0])
        word_average.append(info_data['word_average'][0])
        nbr_1.append(info_data['nbr_1'][0])
        nbr_0.append(info_data['nbr_0'][0])
        transition_0_1_mean.append(info_data['transition_0_1_mean'][0])
        transition_1_0_mean.append(info_data['transition_1_0_mean'][0])
        _levenshtein_mean.append(info_data['levenshtein_mean'][0])
        _is_code.append(int(is_code_by_sardinas(language)))

    frame_data = {
        'word_min': word_min,
        'word_max': word_max,
        'word_average': word_average,
        'nbr_1': nbr_1,
        'nbr_0': nbr_0,
        'transition_0_1_mean': transition_0_1_mean,
        'transition_1_0_mean': transition_1_0_mean,
        'levenshtein_mean': _levenshtein_mean,
        'is_code': _is_code
    }

    pd_data_frame  = pd.DataFrame(frame_data)
    return pd_data_frame

def generate_new_model(data_size) : 
    pd_data_frame = generate_pandas_data_frame(data_size)

    X = pd_data_frame.iloc[:, :-1].values
    Y = pd_data_frame.iloc[:, -1].values

    clf = RandomForestClassifier(random_state=0)
    clf = clf.fit(X, Y)

    dump_model(clf)

def test_precision(model, data_test_size):
    test_x = generate_pandas_data_frame(data_test_size)
    test_y = test_x.iloc[:, -1].values
    print(test_x)

    test_x.drop(["is_code"],axis=1,inplace=True)
    pred_y = model.predict(test_x)
    
    score = accuracy_score(test_y, pred_y)
    return score * 100

def is_code_by_IA(model, language):
    data_predict = generate_info_language(language)
    return model.predict(pd.DataFrame(data_predict))
