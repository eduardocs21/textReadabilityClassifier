from readability import Readability
import nltk
# nltk.download('punkt')
import os
import svm_evaluation
import grammar
import vocabulary
import re

training_dirPath = 'training_data'
test_dirPath = 'test_data'
path_additional_vocabulary = 'vocabulary_data'
numberOfFoldsForCrossVal = 10
grade = 8

data_metrics = []
data_grades = []
training_vocabulary = {"."} # define as a set
text: str


def training_readability():
    # calculate scores for training data
    global text
    global training_vocabulary

    for file in os.listdir(training_dirPath):
        with open(training_dirPath + '/' + file, encoding='utf-8') as f:
            text = f.read()
            f.close()

        # get Meta-Data through file name: ID (arbitrary), Grade (as set by the textbook authors),
        # Format (read/listen), Type (plain/blog/song/dialog/...)
        textGrade, textID, textFormat, textType = file.split("_")
        textType = textType.split(".")[0]

        # filter text types that arent suitable for this analysis
        if textType in ('dialog', 'cloze', 'mixed', 'german', 'poem', 'song', 'chants', 'bilingualmodule'):
            continue

        readab = Readability(text)


        # calculate readability scores and save as data
        data_metrics.append(
            [readab.flesch_kincaid().score, readab.flesch().score, readab.gunning_fog().score, readab.coleman_liau().score,
             readab.dale_chall().score, readab.ari().score, readab.linsear_write().score, readab.spache().score])

        data_grades.append(textGrade)


training_readability()
# print(data_metrics)
# print(data_grades)
print('size of used data set: ' + str(len(data_metrics)))

# cross-validation
# scores = svm_evaluation.crossValidation(data_metrics, data_grades, numberOfFoldsForCrossVal)
# accuracy = sum(scores) / numberOfFoldsForCrossVal
# print('f1-score = ' + str(accuracy))


# prediction of new data


for file in os.listdir(test_dirPath):
    with open(test_dirPath + '/' + file, encoding='utf-8') as f:
        text = f.read()
        f.close()

    # READABILITY: compare readability of test text to training data

    r = Readability(text)

    test_metrics = [[r.flesch_kincaid().score, r.flesch().score, r.gunning_fog().score, r.coleman_liau().score,
                     r.dale_chall().score, r.ari().score, r.linsear_write().score, r.spache().score]]

    print()
    print('Evaluation of file: ' + file)
    print('---------')
    print('Readability:')
    print('scores: ' + str(test_metrics))
    print('difficulty of input text is similar to a text from grade: ' + str(svm_evaluation.predict(
       data_metrics, data_grades, test_metrics)))
    print('---------')
    print('Grammar: ')

    # GRAMMAR: grammar checking of new data
    # grammar.check_grammar(text)   # TODO uncomment

    print('---------')
    print('Vocabulary: ')

    # VOCABULARY: check for unknown words
    training_vocabulary = vocabulary.add_training_vocabulary(training_dirPath, grade, training_vocabulary)
    training_vocabulary = vocabulary.add_additional_vocabulary(path_additional_vocabulary, training_vocabulary)
    vocabulary.print_unknown_words(text, training_vocabulary)

    print('---------' + '\n' + '\n' + '\n' + '\n' + '\n')



