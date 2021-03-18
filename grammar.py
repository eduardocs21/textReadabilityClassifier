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
per_part = []
gerund = []

pre_per_pro = []
pa_per_pro = []
fu_per_pro = []

passive = []

# basic data
text: str
pos_text: list
parsed_text: list


def check_grammar(raw_text):
    # preparation (convert to string, generate and print pos-tags and dependency parses)
    global text
    global pos_text
    global parsed_text

    text = str(raw_text)
    pos_parser = CoreNLPParser(url='http://localhost:9000', tagtype='pos')
    pos_text = pos_parser.tag(text.split())
    print("POS-Tags: " + str(pos_text))
    dep_parser = CoreNLPDependencyParser(url='http://localhost:9000')
    parsed_text = list(dep_parser.parse(text.split()))


    # tense aspects
    search_tense_aspects()

    # TODO: sentence parsing
    # sentences = text.split('. ')
    # sentences_token_list = []
    # for sentence in sentences:
    #     sentences_token_list.append(sentence.split())
    #
    # parsed_sentences = list(dep_parser.parse_sents(sentences_token_list))
    # for x in parsed_sentences:
    #     for y in x:
    #         print(y)
    #         break
    #     break

    print("Dependency Parsing: " + str(
        [[(governor, dep, dependent) for governor, dep, dependent in parse.triples()] for parse in parsed_text]))
    print("---")
    print("Results:")

    # 1)
    # plural of nouns
    print(search_postags(['NNS', 'NNPS'], "plural of nouns"))
    print()

    # possessive ending (s-genitive)
    print(search_postags(['POS'], "possessive ending (s-genitive)"))
    print()

    # adverbs (of frequency)
    print(search_postags(['RB'], "adverbs and negations"))
    print()

    # comparative adjectives and adverbs
    print(search_postags(['JJR', 'JJS', 'RBR', 'RBS'], "comparative adjectives (and adverbs)"))
    print()

    # 2)
    # personal pronouns
    print(search_postags(['PRP'], "personal pronoun"))
    print()

    # modal verbs (can/can't)
    print(search_postags(['MD'], "modal verbs"))
    print()

    # TODO imperatives

    # TODO have got

    # TODO there + be

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

    # TODO have to

    # present progressive
    if pre_pro:
        print("present progressive: YES --- Details:")
        print(pre_pro)
    else:
        print("present progressive: NO")
    print()

    # simple past
    print(search_postags(['VBD'], "simple past"))
    print()

    # TODO conditional clauses

    # present progressive
    if pre_pro:
        print("present progressive: YES --- Details:")
        print(pre_pro)
    else:
        print("present progressive: NO")
    print()

    # present perfect
    if pre_per:
        print("present perfect: YES --- Details:")
        print(pre_per)
        print()
    else:
        print("present perfect: NO")
        print()

    # future simple (will-future)
    if fu_si:
        print("future simple (will-future): YES --- Details:")
        print(fu_si)
    else:
        print("future simple (will-future): NO")
    print()

    # going-to-future
    if fu_gt:
        print("going-to-future: YES --- Details:")
        print(fu_gt)
    else:
        print("going-to-future: NO")
    print()

    # KLP9
    print('-----')
    print('KLP9')
    print('-----')

    # past progressive
    if pa_pro:
        print("past progressive: YES --- Details:")
        print(pa_pro)
    else:
        print("past progressive: NO")
    print()

    # past perfect
    if pa_per:
        print("past perfect: YES --- Details:")
        print(pa_per)
    else:
        print("past perfect: NO")
    print()

    # gerund
    if gerund:
        print("gerund: YES --- Details:")
        print(gerund)
    else:
        print("gerund: NO")
    print()

    # TODO since/for

    # passive
    if passive:
        print("passive: YES --- Details:")
        print(passive)
    else:
        print("passive: NO")
    print()

    # TODO relative clauses

    # TODO contact clauses

    # TODO reflexive pronouns


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

    # search the text for possessive pronouns and determiners and separate them
    for i in range(0, len(pos_text)):
        word = pos_text[i]
        if word[1] == 'PRP$':
            w = word[0].lower()
            # separate clear cases
            # if w == 'my' or w == 'your' or w == 'her' or w == 'our' or w == 'their':
            if w in ('my', 'your', 'her', 'our', 'their'):
                pd_words.append(w)
            elif w in ('mine', 'yours', 'hers', 'ours', 'theirs'):
                pp_words.append(w)

            # separate special cases (its and his) by checking if following word is a noun
            else:
                if pos_text[i + 1][1] in ('NN', 'NNS', 'NNP', 'NNPS'):
                    pd_words.append(w)
                else:
                    pp_words.append(w)

    return pd_words, pp_words


# TODO write method for things like since/for (with module 're'?)
def search_regex():
    print()


def search_tense_aspects():
    # search every occurrence of every tense aspect in the text and save it in the according global list
    # form (example): pre_pro = ["walking", "climbing"], pa_par = ["formed", "sung", "taken"]]
    # abbreviations: fu = future, pa = past, pre = present
    #               pro = progressive, per = perfect, si = simple, gt = going-to, part = participle
    # save sentence boundaries to check sentence context for more complicated distinctions, f.i. between
    #   'will be doing' (fu_pro) and 'will have been doing' (fu_per_pro)

    for parse in parsed_text:

        parses_list = list(parse.triples())
        sentence_start = 0

        # identify dependency parses for tense aspects in the text and save it in the according list
        for i in range(0, len(parses_list)):

            tag1 = parses_list[i][0][1]
            word1 = parses_list[i][0][0]
            tag2 = parses_list[i][2][1]
            word2 = parses_list[i][2][0]
            dep = parses_list[i][1]

            # Update sentence_start (index) if necessary
            if dep in ('punct', 'nsubj', 'csubj', 'nsubj:pass', 'csubj:pass'):
                sentence_start = i

            elif dep == 'parataxis':
                continue

            elif dep == 'aux':
                # future simple / will-future
                if (tag1 in ('VB', 'JJ')) and (word2 in ('will', 'wo', "'ll")):
                    fu_si.append(word2 + " " + word1)
                # present participle: ("-ing")
                elif tag1 == 'VBG':
                    # present progressive and going-to future and one passive form (to be + having + VBN)
                    if word2 == 'am' or word2 == 'are' or word2 == 'is' or word2 == "'m" or word2 == "'re":
                        not_identified = True
                        if word1 == 'going':
                            # search for additional xcomp VB with dependency to word1 until sentence part ends
                            for j in range(sentence_start + 1, len(parses_list)):
                                dep = parses_list[j][1]
                                if dep == 'punct' or dep == 'nsubj' or dep == 'csubj' or \
                                        dep == 'nsubj:pass' or dep == 'csubj:pass':
                                    break
                                if dep == 'xcomp' and parses_list[j][2][1] == 'VB':
                                    fu_gt.append(word2 + " " + word1 + " to " + parses_list[j][2][0])
                                    not_identified = False
                                    break
                        elif word1 == 'having':
                            # search for additional ccomp VBN with dependency to word1 until sentence part ends
                            for j in range(sentence_start + 1, len(parses_list)):
                                dep = parses_list[j][1]
                                if dep == 'punct' or dep == 'nsubj' or dep == 'csubj' or \
                                        dep == 'nsubj:pass' or dep == 'csubj:pass':
                                    break
                                if dep == 'ccomp' and parses_list[j][2][1] == 'VBN':
                                    passive.append(word2 + " " + word1 + " (obj) " + parses_list[j][2][0])
                                    not_identified = False
                                    break
                        if not_identified:
                            pre_pro.append(word2 + " " + word1)
                    # past progressive
                    elif word2 == 'was' or word2 == 'were':
                        pa_pro.append(word2 + " " + word1)
                    # future progressive
                    elif word2 == 'will' or word2 == 'wo' or word2 == "'ll":
                        # search for additional keyword "be" with dependency to word1 until sentence part ends
                        for j in range(sentence_start + 1, len(parses_list)):
                            dep = parses_list[j][1]
                            if dep == 'punct' or dep == 'nsubj' or dep == 'csubj' or \
                                    dep == 'nsubj:pass' or dep == 'csubj:pass':
                                break
                            if parses_list[j][2][0] == 'be' and parses_list[j][0][0] == word1:
                                fu_pro.append(word2 + " be " + word1)
                                break
                    # present/past/future perfect progressive
                    elif word2 == 'been':
                        not_identified = True
                        # search for additional keyword "have" with dependency to word1 until sentence part ends
                        for j in range(sentence_start + 1, len(parses_list)):
                            dep = parses_list[j][1]
                            if dep == 'punct' or dep == 'nsubj' or dep == 'csubj' or \
                                    dep == 'nsubj:pass' or dep == 'csubj:pass':
                                break
                            if parses_list[j][2][0] == 'have' or parses_list[j][2][0] == 'has' \
                                    or parses_list[j][2][0] == "'ve":
                                # search for additional keyword "will" with dependency to word1 until sentence part ends
                                for k in range(sentence_start + 1, len(parses_list)):
                                    dep = parses_list[k][1]
                                    if dep == 'punct' or dep == 'nsubj' or dep == 'csubj' or \
                                            dep == 'nsubj:pass' or dep == 'csubj:pass':
                                        break
                                    if parses_list[k][2][0] == 'will' or parses_list[k][2][0] == 'wo' \
                                            or parses_list[k][2][0] == "'ll":
                                        fu_per_pro.append("will/won't have " + word2 + " " + word1)
                                        not_identified = False
                                        break
                                if not_identified:
                                    pre_per_pro.append("have/has " + word2 + " " + word1)
                                    not_identified = False
                                break
                        if not_identified:
                            pa_per_pro.append("had " + word2 + " " + word1)

                # past participle ("-ed")
                elif tag1 == 'VBN':
                    # past perfect
                    if word2 == 'had':
                        pa_per.append(word2 + " " + word1)
                    # present perfect and future perfect
                    elif word2 == 'has':
                        pre_per.append(word2 + " " + word1)
                    elif word2 == 'have' or word2 == "'ve":
                        not_identified = True
                        # search for additional keyword "will" with dependency to word1 until sentence part ends
                        for j in range(sentence_start + 1, len(parses_list)):
                            dep = parses_list[j][1]
                            if dep == 'punct' or dep == 'nsubj' or dep == 'csubj' or \
                                    dep == 'nsubj:pass' or dep == 'csubj:pass':
                                break
                            if parses_list[j][2][0] == 'will' or parses_list[j][2][0] == 'wo' \
                                    or parses_list[j][2][0] == "'ll":
                                fu_per.append("will/won't " + word2 + " " + word1)
                                not_identified = False
                                break
                        if not_identified:
                            pre_per.append(word2 + " " + word1)
                    # perfect participle ("having" + PP)
                    elif tag2 == 'VBG':
                        per_part.append(word2 + " " + word1)

            # passive
            elif dep == 'aux:pass':
                passive.append(word2 + " " + word1)

            # gerund
            elif str(word2).endswith('ing') and tag2 == 'NN' and dep == 'obj':
                gerund.append(word1 + " " + word2)

            # present participle (other)
            elif tag1 == 'VBG' or tag2 == 'VBG':
                pre_part_bool = True
                word = word1
                if tag2 == 'VBG':
                    word = word2
                # if the VBG-verb doesnt have an auxiliary, it's not recognized above, but still a present participle
                # and therefore added to the "present participle (other)" list pre_part
                for j in range(sentence_start + 1, len(parses_list)):
                    dep = parses_list[j][1]
                    if dep == 'punct':
                        break
                    if (dep == 'aux' or dep == 'aux:pass') and (parses_list[j][0][0] == word or parses_list[j][2][0] == word):
                        pre_part_bool = False
                        break
                if pre_part_bool:
                    pre_part.append(word)

            # past participle (other) - case 1
            elif tag1 == 'VBN' or tag2 == 'VBN':
                pa_part_bool = True
                word = word1
                if tag2 == 'VBN':
                    word = word2
                # if the VBG-verb doesnt have an auxiliary, it's not recognized above, but still a present participle
                # and therefore added to the "present participle (other)" list pre_part
                for j in range(sentence_start + 1, len(parses_list)):
                    dep = parses_list[j][1]
                    if dep == 'punct':
                        break
                    if (dep == 'aux' or dep == 'aux:pass') and (parses_list[j][0][0] == word or parses_list[j][2][0] == word):
                        pa_part_bool = False
                        break
                if pa_part_bool:
                    pa_part.append(word)

    # difference parses will be counted up for higher precision, therefore numbers won´t be accurate in this case
    # a warning follows:
    if len(parsed_text) > 1:
        print("WARNING: Tense aspect numbers aren't accurate since the text dependencies are ambiguous "
              "(according to Stanford Core NLP")





