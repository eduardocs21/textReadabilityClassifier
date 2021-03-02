import re
from re import Pattern, Match
import nltk
# nltk.download('averaged_perceptron_tagger')


def checkGrammar_KLP7(text):

    # preparation (get string and pos-tags)
    text = str(text)
    pos_text = nltk.pos_tag(nltk.word_tokenize(text))
    print(pos_text)

# 1)
    # plural of nouns
    print(search_postags(pos_text, ['NNS', 'NNPS']))


    # s-genitive
    # adverbs (of frequency)
        # pos-tagging
    # adjective (comparative)
        # pos-tagging

# 2)
    # personal pronouns
    search('personal pronouns', ['i', 'you', 'he', 'she', 'it', 'we', 'they'], text.lower())



    # can/can't

    # imperatives

    # have got

    # there + be
    # possessive determiners
    # simple present statements
    # word order
    # have to
    # simple present questions
    # some/any
    # Mengenangaben
    # personal pronouns
    # present progressive
    # simple past
    # this/that/these/those
    # word order subordinate clause


def checkGrammar_KLP9():
    print('checking')


def search(name, search_terms, text):
    for pp in search_terms:
        if re.search(pp, text):
            print(name + ': YES')
            return

    print(name + ': NO')


def search_postags(pos_text, pos_tags):
    words = []
    for word in pos_text:
        for pos_tag in pos_tags:
            if word[1] == pos_tag:
                words.append(word[0])

    return words





def search_detailed(name, search_terms, text):
    print('X')
