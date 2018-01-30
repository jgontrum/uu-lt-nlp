import sys

IRREGULAR = {
    "AUX": {
        "'d": "would",
        "ve": "have",         
        "has": "have",
        "'ve": "have",
        "had": "have",
        "being": "be",
        "been": "be",
        "am": "be",
        "is": "be",
        "were": "be",
        "was": "be",
        "r": "be",
        "are": "be",
        "ll": "will",
        "'s": "be",
        "'m": "be",
        "does": "do",
        "done": "do",
        "ca": "can",
        "did": "do",
        "'ll": "will"
    },
    "ADJ": {
        "Best": "best",
        "better": "better",
        "best": "best",
        "other": "other"
    },
    "DET": {
        "an": "a",
        "An": "a"
    },
    "NOUN": {
        "men": "man",
        "Thanks": "thanks"
    },
    "PART": {
        "n't": "not"
    },
    "PRON": {
        "me": "my",         
        "me": "I",         
        "I": "I",
        "her": "she",
        "his": "he",
        "him": "he",
        "them": "they",
        "their": "they",
        "our": "we",
        "us": "we",
        "its": "its",
        "your": "you",
    },
    "VERB": {
        "gave": "give",
        "need": "need",
        "must": "must",
        "s": "be",
        "m": "be",
        "did": "do",
        "made": "make",
        "went": "go",
        "'d": "would",
        "ve": "have",         
        "Was": "be",
        "has": "have",
        "'ve": "have",
        "had": "have",
        "being": "be",
        "been": "be",
        "am": "be",
        "is": "be",
        "were": "be",
        "was": "be",
        "sold": "sell",
        "'re": "be",
        "found": "find",
        "stole": "steal",
        "stolen": "steal",
        "making": "make",
        "r": "be",
        "are": "be",
        "ll": "be",
        "'s": "be",
        "'m": "be",
        "done": "do",
        "took": "take",
        "met": "meet",
        "got": "get",
        "had": "have",
        "said": "say",
        "sent": "send",
        "saw": "see",
        "broke": "break",
        "taught": "teach"
    },
}

VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxz"

def lowercase(w, tag):
    if tag not in ["PROPN"]:
        return w.lower()

    return w

def noun_lemma(word):
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    elif word.endswith("ren"):
        return word[:-3]
    else:
        return word

def verb_lemma(word):
    if word.endswith("ed"):
        if word[-3] in "tgrc" or len(word[:-2]) <= 3:
            return word[:-1]
        else:
            return word[:-2]
    if word.endswith("ing"):
        if word[-4] in "pmrvct" and word[-5] not in "erct":
            return word[:-3] + "e"
        else:
            return word[:-3]
    elif len(word) > 1 and word.endswith("s"):
        #print(word[:-1], file=sys.stderr)
        return word[:-1]
    else:
        return word

def verb_repair(word, original):
    if word[-1] in CONSONANTS:
        return word + "e"
    return word

def adj_lemma(word):
    if word.endswith("er"):
        return word[:-2]
    elif word.endswith("est"):
        return word[:-3]
    else:
        return word

for line in sys.stdin:
    if line.strip():
        (word, tag) = line.strip().split("\t")
        lemma = word
        # Check for irregular words
        irregular_form = IRREGULAR.get(tag, {}).get(word)
        if not irregular_form:
            lemma = word
            if tag == "NOUN":
                lemma = noun_lemma(lemma)
            elif tag == "VERB":
                lemma = verb_lemma(lemma)
            lemma = lowercase(lemma, tag)

            if lemma.endswith("ie") and len(lemma) > 3: 
                lemma = lemma[:-2] + "y"
            lemma = lemma.replace("drew", "draw")
            

        else:
            lemma = irregular_form
        print("{0}\t{1}\t{2}".format(word, tag, lemma))
    else:
        print()
