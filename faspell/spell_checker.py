#!/usr/local/bin/env python3.5
# -*- coding: utf-8 -*-
import re


class SpellChecker(object):

    def __init__(self, database):
        self.all_words = database
        self. alphabet = 'آ ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی'

    def edit(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts = [a + c + b for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def declare_known_words(self, words):
        return set(w for w in words if w in self.all_words)

    def correct(self, word):
        normalized = self.normalize(word)
        candidates = list(self.declare_known_words([normalized])) or list(self.declare_known_words(self.edit(normalized)))
        return self.analyze_correction(candidates, normalized, word)

        # this analysis is logically based on CKEditor response expectation:
    def analyze_correction(self, candidates, normalized, word):
        if candidates == []:  # no result due to non-persian input
            return self.make_dictionary(normalized, candidates)
        elif candidates[0] == normalized and len(candidates) == 1:  # candidate is same as word (word is correct)
            return []
        else:  # word is misspelled, ergo returning the word and the suggested candidates
            return self.make_dictionary(word, candidates)

    @staticmethod
    def normalize(word):
        if '؟' in word:
            return word.replace('؟', '')
        return word

    @staticmethod
    def make_dictionary(word, candidates):
        suggestion = []
        for item in candidates:
            suggestion.append(item)
        suggestion.sort()
        return [{
            'word': word,
            'ud': False,
            'suggestions': suggestion
        }]


if __name__ == '__main__':

    def words(database):
        return re.split('\n', database)

    def train(features):
        model = dict.fromkeys(features, 1)
        return model


    with open('dictionary', 'r') as my_dictionary:
        check_spelling = SpellChecker(train(words(my_dictionary.read())))
        print(check_spelling.correct('%$#%$#^#'))


