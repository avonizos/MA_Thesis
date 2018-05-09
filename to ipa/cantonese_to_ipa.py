# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for converting the Cantonese
# version of Shijing from romanisation system into IPA


import codecs
import re

class IPAConverter():
    out = codecs.open('../txt/ipa ambiguous/cantonese_ipa.txt', 'w', 'utf-8')
    text = []
    result = ''
    search_pron = re.compile(u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?')
    vowels = u'aeuioy'

    initials = {
        u'ng': u'ŋ',
        u'gw': u'kʷ',
        u'kw': u'kʷʰ',
        u'z': u'ts',
        u'c': u'tsʰ',
        u'b': u'p',
        u'p': u'pʰ',
        u'd': u't',
        u't': u'tʰ',
        u'g': u'k',
        u'k': u'kʰ'
    }
    finals = {
        u'aang': u'aŋ',
        u'oeng': u'œŋ',
        u'aai': u'ai',
        u'aau': u'au',
        u'aam': u'am',
        u'aan': u'an',
        u'ang': u'ɐŋ',
        u'aap': u'ap',
        u'aat': u'at',
        u'aak': u'ak',
        u'eng': u'ɛŋ',
        u'ong': u'ɔŋ',
        u'onk': u'ɔŋ',
        u'ing': u'ɪŋ',
        u'ung': u'ʊŋ',
        u'yun': u'yn',
        u'yut': u'yt',
        u'oey': u'œy',
        u'oen': u'œn',
        u'oet': u'œt',
        u'oek': u'œk',
        u'eon': u'øn',
        u'eot': u'øt',
        u'eoi': u'øy',
        u'aa': u'a',
        u'ai': u'ɐi',
        u'au': u'ɐu',
        u'am': u'ɐm',
        u'an': u'ɐn',
        u'ap': u'ɐp',
        u'at': u'ɐt',
        u'ak': u'ɐk',
        u'eu': u'ɛu',
        u'em': u'ɛm',
        u'ep': u'ɛp',
        u'et': u'ɛt',
        u'ek': u'ɛk',
        u'uk': u'ʊk',
        u'oi': u'ɔi',
        u'on': u'ɔn',
        u'ot': u'ɔt',
        u'ok': u'ɔk',
        u'oe': u'œ',
        u'yu': u'y',
        u'ik': u'ɪk',
        u'o': u'ɔ',
        u'e': u'ɛ',
    }
    tone = {
        u'1': u'55',
        u'2': u'35',
        u'3': u'33',
        u'4': u'21',
        u'5': u'23',
        u'6': u'22'
    }
    combinations = {
        u'sy': u'ʃy',
        u'su': u'ʃu',
        u'so': u'ʃo',
        u'sø': u'ʃø',
        u'sœ': u'ʃœ',
        u'sʊ': u'ʃʊ',
        u'sɔ': u'ʃɔ',
        u'tsy': u'tʃy',
        u'tsu': u'tʃu',
        u'tso': u'tʃo',
        u'tsø': u'tʃø',
        u'tsœ': u'tʃœ',
        u'tsʊ': u'tʃʊ',
        u'tsɔ': u'tʃɔ',
        u'tsʰy': u'tʃʰy',
        u'tsʰu': u'tʃʰu',
        u'tsʰo': u'tʃʰo',
        u'tsʰø': u'tʃʰø',
        u'tsʰœ': u'tʃʰœ',
        u'tsʰʊ': u'tʃʰʊ',
        u'tsʰɔ': u'tʃʰɔ'
    }

    def load(self):
        f = codecs.open('../txt/shijing_original/dialects/cantonese.txt', 'r', 'utf-8')
        for line in f:
            self.text.append(line)

    def vowel(self, s):
        seq = u''
        if s is not None:
            for char in s:
                if char in self.vowels:
                    seq += char
        return seq

    def bracket_words(self, word):
        result = []
        words_brackets = re.findall(u'([^ \(\),]+)', word)
        if len(words_brackets) > 0:
            for word in words_brackets:
                word = word.strip('\r\n')
                result.append(word)
        return result

    def convert_tone(self, w):
        for t in self.tone:
            if t in w:
                w = w.replace(t, self.tone[t])
                break
        return w

    def convert_initial(self, w):
        vowel = self.vowel(w)
        ind = w.find(vowel[0])
        initial = w[0:ind]
        w_part = w[0:ind]
        if initial in self.initials:
            w_part = w_part.replace(initial, self.initials[initial])
        new_w = w_part + w[ind:]
        return new_w

    def convert_final(self, w):
        vowel = self.vowel(w)
        ind = w.find(vowel[0])
        final = w[ind:-2]
        if final in self.finals:
            w = w.replace(final, self.finals[final])
        return w

    def convert_combinations(self, w):
        for comb in self.combinations:
            if comb in w:
                w = w.replace(comb, self.combinations[comb])
        return w

    def convert_all(self, w):
        is_ng_vocalic = re.search(u'(^| )ng([0-9]+)', w)
        if is_ng_vocalic is not None:
            w = w.replace(u'ng', u'ŋ̩')
            return w
        else:
            is_m_vocalic = re.search(u'(^| )m([0-9]+)', w)
            if is_m_vocalic is not None:
                w = w.replace(u'm', u'm̩')
                return w
            else:
                w = self.convert_initial(w)
                w = self.convert_final(w)
                w = self.convert_combinations(w)
        return w

    def transcribe(self):
        for line in self.text:
            words = re.search(self.search_pron, line)
            line_words = []
            if words is not None:
                i = 1
                while i <= 8:
                    if words.group(i):
                        line_words.append(words.group(i).strip('\r\n'))
                    i += 1

            for w in line_words:
                if w != '-':
                    if '(' not in w:
                        w = self.convert_tone(w)
                        w = self.convert_all(w)
                        self.result += w + ' '
                    else:
                        brackets = self.bracket_words(w)
                        if len(brackets) == 2 and brackets[0] == brackets[1]:
                            w = brackets[0]
                            w = self.convert_tone(w)
                            w = self.convert_all(w)
                            self.result += w + ' '
                        else:
                            word1 = self.convert_tone(brackets[0])
                            word1 = self.convert_all(word1)
                            if word1 is not None:
                                result = word1 + '('
                            for word in brackets[1:]:
                                word = self.convert_tone(word)
                                word = self.convert_all(word)
                                result += word + ','
                            result += ')'
                            result = result.replace(',)', ')')
                            self.result += result + ' '
                else:
                    if w is not None:
                        self.result += w + ' '
            self.result += '\n'
            self.result = self.result.replace(u' \n', '\n')
        self.out.write(self.result)

c = IPAConverter()
c.load()
c.transcribe()
print c.result