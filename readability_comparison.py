import os
from readability import Readability

import svm_evaluation

data_metrics = []
data_grades = []


def training_readability(path):
    # calculate scores for training data

    for file in os.listdir(path):
        with open(path + '/' + file, encoding='utf-8') as f:
            text = f.read()
            f.close()

        # get Meta-Data through file name: ID (arbitrary), Grade (as set by the textbook authors),
        # Format (read/listen), Type (plain/blog/song/dialog/...)
        textGrade, textID, textFormat, textType = file.split("_")
        textType = textType.split(".")[0]

        # filter text types that arent suitable for this analysis
        if textType in ('dialog', 'cloze', 'mixed', 'german', 'poem', 'song', 'chants', 'bilingualmodule'):
            continue

        r = Readability(text)

        # calculate readability scores and save as data
        data_metrics.append(
            [r.flesch_kincaid().score, r.flesch().score, r.gunning_fog().score, r.coleman_liau().score,
             r.dale_chall().score, r.ari().score, r.linsear_write().score, r.spache().score])

        data_grades.append(textGrade)

    return data_metrics, data_grades


def compare(text, grade):
    r = Readability(text)

    test_metrics = [[r.flesch_kincaid().score, r.flesch().score, r.gunning_fog().score, r.coleman_liau().score,
                     r.dale_chall().score, r.ari().score, r.linsear_write().score, r.spache().score]]

    print('scores of test text: ' + str(test_metrics))
    calculated_grade = int(svm_evaluation.predict(data_metrics, data_grades, test_metrics))
    print('difficulty of input text is similar to a text from grade: ' + str(calculated_grade))
    if calculated_grade < grade:
        print("=> suitable, but may be too easy to read for the students")
    elif calculated_grade > grade:
        print("=> may be too difficult to read for the students")
    else:
        print("=> suitable for the students")
