import re
import os


def print_unknown_words(text, training_vocabulary):
    print("Number of known words: " + str(len(training_vocabulary)))
    unknown_vocabulary = []

    # Compare vocabulary of unseen text with the set
    for word in text.split():
        word = re.sub(r'[^\w\s]', "", word).lower()  # remove punctuation and capital letters
        if word not in training_vocabulary:
            unknown_vocabulary.append(word)

    # print out unseen words as “probably difficult words for the students”
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


