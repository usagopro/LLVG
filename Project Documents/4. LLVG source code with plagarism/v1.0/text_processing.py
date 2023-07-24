import spacy
import string

nlp = spacy.load('en_core_web_sm')


def remove_punctuation(sentence):
    translator = str.maketrans("", "", string.punctuation)
    return sentence.translate(translator)


def Numbers(doc):
    numbers = []
    i = 0
    while i < len(doc):
        if doc[i].like_num or doc[i].ent_type_ == 'CARDINAL':  # Check if the token is a numerical value
            number = doc[i].text
            j = i + 1
            while j < len(doc):
                if doc[j].like_num or doc[j].ent_type_ == 'CARDINAL':
                    number = number + " " + doc[j].text
                    j += 1
                else:
                    break
            i = j + 1
            numbers.append(number)
        else:
            i += 1

    return numbers


def Verbs(doc):
    return [token.lemma_ for token in doc if token.pos_ == "VERB"]


def Nouns(doc):
    return [token.text for token in doc if token.pos_ == "NOUN"]
