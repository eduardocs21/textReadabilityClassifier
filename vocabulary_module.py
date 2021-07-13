import re
import os


def print_unknown_words(text, training_vocabulary):
    # print a list of every word that is not included in the training vocabulary

    print("Number of known words: " + str(len(training_vocabulary)))
    unknown_vocabulary = []

    # Compare vocabulary of unseen text with the set
    for word in text.split():
        word = re.sub(r'[^\w\s]', "", word).lower()  # remove punctuation and capital letters
        if word not in training_vocabulary:
            unknown_vocabulary.append(word)

    print("probably difficult vocabulary for these students (" + str(len(unknown_vocabulary)) + " words):")
    print(unknown_vocabulary)


def add_additional_vocabulary(path, training_vocabulary):
    # read every file in the directory (path) and save word in 'training_vocabulary'

    for file in os.listdir(path):
        with open(path + '/' + file, encoding='utf-8') as f:
            text = f.read()

            for word in text.split():
                training_vocabulary.add(word.lower())
            f.close()

    return training_vocabulary


def add_training_vocabulary(training_dirPath, grade, training_vocabulary):
    # save all words (except duplicates, thats why a set is used) of the training text
    # if the grade is lower (and the words therefore should be known)

    for file in os.listdir(training_dirPath):
        with open(training_dirPath + '/' + file, encoding='utf-8') as f:
            text = f.read()
            f.close()

        textGrade = file.split('_')[0]

        if int(textGrade) < grade:
            for word in text.split():
                word = re.sub(r'[^\w\s]', "", word).lower()  # remove punctuation and capital letters
                training_vocabulary.add(word)

    return training_vocabulary


