import re
from re import Pattern, Match


def checkGrammar_KLP7(text):
    text = str(text)
# 1)
    # plural of nouns
    # s-genitive
    # adverbs (of frequency)
        # pos-tagging
    # adjective (comparative)
        # pos-tagging

# 2)
    # personal pronouns
    search('personal pronouns', ['i', 'you', 'he', 'She', 'it', 'we', 'they'], text)



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


def search_detailed(name, search_terms, text):
    print('X')
