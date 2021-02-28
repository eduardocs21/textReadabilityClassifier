import re

personalPronouns = 'I', 'You', 'We'


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
    # personal pronouns + be
    # can/can't
    print(re.findall('can', text))
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
