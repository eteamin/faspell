#!/usr/local/bin/env python3.5
# -*- coding: utf-8 -*-
import re
import collections
from os import path
import spell_checker

__author__ = 'amin'


class SpellChecker(object):

    def __init__(self, database_file):
        self.data_base_file = database_file
        self.NWORDS = self.train(self.words(self.data_base_file))

    def words(self, text):
        return re.findall('[ا-ی]+', text)

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    alphabet = 'آ ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی'

    def first_edit(self, word):
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in s for c in self.alphabet if b]
        inserts = [a + c + b for a, b in s for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def second_edit(self, word):
        return set(e2 for e1 in self.first_edit(word) for e2 in self.first_edit(e1) if e2 in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    # this method splits the input text to individual lines, fetching all words from each line and spell checks each one
    # then provides the dictionary maker with the line, character and suggestions

    def correct(self, word):
        candidates = list(self.known([word])) or \
                     list(self.known(self.first_edit(word))) or \
                     list(self.second_edit(word))

        if candidates == []:
            return self.dictionary_maker(word, candidates)
        elif candidates[0] == word and len(candidates) == 1:
            return []
        else:
            return self.dictionary_maker(word, candidates)


    @staticmethod
    def dictionary_maker(word, candidates):
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
    dictionary_filename = path.abspath(path.join(path.dirname(spell_checker.__file__), '..', 'tests', 'dictionary'))
    with open(dictionary_filename, 'r') as mydict:
        checker = SpellChecker(mydict.read())
        print(checker.correct('سلام'))
        print(checker.correct('شلام'))
        print(checker.correct('یبشسیبلیسبیشس'))
        print(checker.correct('dasdsadas'))

