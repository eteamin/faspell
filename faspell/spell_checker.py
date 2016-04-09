#!/usr/local/bin/env python3.5
# -*- coding: utf-8 -*-
import re


class SpellChecker(object):

    def __init__(self, database):
        self.NWORDS = database
    alphabet = 'آ ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی'

    def first_edit(self, word):
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in s for c in self.alphabet if b]
        inserts = [a + c + b for a, b in s for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def normalize(self, word):
        if '؟' in word:
            normalized = word.replace('؟', '')
            return normalized
        return word

    def correct(self, word):
        normalized = self.normalize(word)
        candidates = list(self.known([normalized])) or list(self.known(self.first_edit((normalized))))

        if candidates == []:
            return self.dictionary_maker(normalized, candidates)
        elif candidates[0] == normalized and len(candidates) == 1:
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

    def words(database):
        return re.split('\n', database)

    def train(features):
        model = dict.fromkeys(features, 1)
        return model


    with open('dictionary', 'r') as my_dictionary:
        check_spelling = SpellChecker(train(words(my_dictionary.read())))
        print(check_spelling.correct(''))


