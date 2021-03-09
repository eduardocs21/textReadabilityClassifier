import re
from re import Pattern, Match
import nltk
# nltk.download('averaged_perceptron_tagger')
from nltk.parse import CoreNLPParser, CoreNLPDependencyParser

# variables tense aspects
# abbreviations: fu = future, pa = past, pre = present
#               pro = progressive, per = perfect, si = simple, gt = going-to, part = participle
fu_si = []
fu_gt = []

pre_per = []
pa_per = []
fu_per = []

pre_pro = []
pa_pro = []
fu_pro = []

pre_part = []
pa_part = []
gerund = []

pre_per_pro = []
pa_per_pro = []
fu_per_pro = []

# basic data
text: str
pos_text: list
parsed_text: list


def check_grammar_klp7(raw_text):
    # preparation (convert to string, generate and print pos-tags and dependency parses)
    global text
    global pos_text
    global parsed_text

    text = str(raw_text)
    pos_text = nltk.pos_tag(nltk.word_tokenize(raw_text))
    print("POS-Tags: " + str(pos_text))
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parsed_text = list(dep_parser.parse(text.split()))
    parsed_text = list(parsed_text)

    print("Dependency Parsing: " + str(
        [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parsed_text]))
    print("---")
    print("Results:")

    # 1)
    # plural of nouns
    print(search_postags(['NNS', 'NNPS'], "plural of nouns"))
    print()

    # s-genitive
    print(search_postags(['POS'], "possessive ending (s-Genitiv)"))
    print()

    # adverbs (of frequency)
    print(search_postags(['RB'], "adverbs"))
    print()

    # comparative adjectives and adverbs
    print(search_postags(['JJR', 'JJS', 'RBR', 'RBS'], "comparative adjectives (and adverbs)"))
    print()

    # 2)
    # personal pronouns
    # print(search('personal pronouns', ['i', 'you', 'he', 'she', 'it', 'we', 'they'], text.lower()))
    print(search_postags(['PRP'], "personal pronoun"))
    print()

    # modal verbs (can/can't)
    print(search_postags(['MD'], "modal verbs"))
    print()

    # imperatives

    # have got

    # there + be

    # possessive determiners (different to absolute possessive pronouns)
    poss_det, poss_pro = search_possessive_pronouns()

    # if there are matches, print it out and return a dictionary containing word frequencies
    if poss_det:
        print('possessive determiners' + ': YES --- Details:')
        frequency = {}
        for item in poss_det:
            frequency[item] = poss_det.count(item)
        print(frequency)
    else:
        print('possessive determiners' + ': NO')
    print()

    # have to

    # Mengenangaben

    # present progressive
    search_tense_aspects()

    # simple past
    print(search_postags(['VBD'], "simple past"))
    print()

    # this/that/these/those
    # word order subordinate clause

    # possessive pronouns (different to possessive determiners)
    # if there are matches, print it out and return a dictionary containing word frequencies
    if poss_pro:
        print('possessive pronouns' + ': YES --- Details:')
        frequency = {}
        for item in poss_pro:
            frequency[item] = poss_pro.count(item)
        print(frequency)
    else:
        print('possessive pronouns' + ': NO')
    print()


def check_grammar_klp9():
    print('checking')


def search_postags(pos_tags, name):
    words = []
    frequency = {}

    # search the text for every tag and save matches in list "words"
    for word in pos_text:
        for pos_tag in pos_tags:
            if word[1] == pos_tag:
                words.append(word[0])

    # if there are matches, print it out and return a dictionary containing word frequencies (all lowercase)
    if words:
        print(name + ': YES --- Details:')
        for i in range(0, len(words)):
            words[i] = words[i].lower()
        for item in words:
            frequency[item] = words.count(item)
        return frequency

    print(name + ': NO')
    return frequency


# searches for possessive pronouns and differentiates them between possessive determiners and pronouns
# returns separate word lists (all lowercase)
def search_possessive_pronouns():
    pd_words = []
    pp_words = []

    # search the text for personal pronouns and determiners and separate them
    for i in range(0, len(pos_text)):
        word = pos_text[i]
        if word[1] == 'PRP$':
            w = word[0]
            # separate clear cases
            if w == 'my' or w == 'your' or w == 'her' or w == 'our' or w == 'their':
                pd_words.append(word[0])
            elif w == 'mine' or w == 'yours' or w == 'hers' or w == 'ours' or w == 'theirs':
                pp_words.append(word[0])

            # separate special cases (its and his) by checking if following word is a noun
            else:
                if pos_text[i + 1][1] == ('NN' or 'NNS' or 'NNP' or 'NNPS'):
                    pd_words.append(word[0])
                else:
                    pp_words.append(word[0])

    # to lowercase
    for i in range(0, len(pd_words)):
        pd_words[i] = pd_words[i].lower()
    for i in range(0, len(pp_words)):
        pp_words[i] = pp_words[i].lower()

    return pd_words, pp_words


def search_tense_aspects():
    # search every occurrence of every tense aspect in the text and save it in the according global list
    # form (example): pre_pro = ["walking", "climbing"], pa_par = ["formed", "sung", "taken"]]
    # abbreviations: fu = future, pa = past, pre = present
    #               pro = progressive, per = perfect, si = simple, gt = going-to, part = participle
    # save sentence boundaries to check sentence context for more complicated distinctions, f.i. between
    #   'will be doing' (fu_pro) and 'will have been doing' (fu_per_pro)

    print('TENSE ASPECTS:')
    for parse in parsed_text:

        # calculate sentence boundaries to have a scope for later distinction searches
        sentences_start_indexes = []
        for x in range(0, len(list(parse.triples()))):
            governor, dep, dependent = list(parse.triples())[x]
            if dep == 'punct':
                sentences_start_indexes.append(x)

        for governor, dep, dependent in parse.triples():
            t1 = governor[1]
            w2 = dependent[0]
            if dep == 'aux':
                # future simple / will-future
                if (t1 == 'VB' or t1 == 'JJ') and (w2 == 'will' or w2 == 'wo'):
                    fu_si.append(dependent[0] + " " + governor[0])
                # present participle ("-ing")
                elif t1 == 'VBG':
                    # present progressive
                    if w2 == 'am' or w2 == 'are' or w2 == 'is':
                        pre_pro.append(w2 + " " + governor[0])
                    # past progressive
                    elif w2 == 'was' or w2 == 'were':
                        pa_pro.append(w2 + " " + governor[0])
                    # future progressive
                    elif w2 == 'will' or w2 == 'wo':
                        # sentence_end = list(parse.triples())[1].index("'punct'", sentence_start)
                        fu_pro.append(w2 + " be " + governor[0])

            # update sentence_start (index) if necessary
            # elif dep == 'punct':
                # sentence_start = list(parse.triples()).index((governor, dep, dependent), sentence_start)
                # print(sentence_start)

    # difference parses will be counted up for higher precision, therefore numbers won´t be accurate in this case
    # a warning follows:
    if len(parsed_text) > 1:
        print("WARNING: Tense aspect numbers aren't accurate since the text dependencies are ambiguous "
              "(according to Stanford Core NLP")

    print(fu_si)
    print(pre_pro)
    print(pa_pro)
    print(fu_pro)
    print()







