# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for converting the Taiwanese Hokkien
# version of Shijing from romanisation system into IPA

import codecs
import re

class IPAConverter():
    out = codecs.open('../txt/ipa ambiguous/hokkien_ipa.txt', 'w', 'utf-8')
    text = []
    result = ''
    search_pron = re.compile(u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?')
    vowels = u'aeəioɔuãẽĩɔ̃ũ'
    second = {
        u'á': u'a',
        u'é': u'e',
        u'í': u'i',
        u'ó': u'o',
        u'ú': u'u',
        u'ń': u'n̩',
        u'ḿ': u'm̩',
        u'ŋ̍' : u'ŋ̍'
    }
    third = {
        u'à': u'a',
        u'è': u'e',
        u'ì': u'i',
        u'ò': u'o',
        u'ù': u'u',
        u'ǹ': u'n̩'
    }
    fourth = u'ptkh'  # 3ʔ (32)
    fifth = {
        u'â': u'a',
        u'ê': u'e',
        u'î': u'i',
        u'ô': u'o',
        u'û': u'u',
        u'm̂': u'm̩',
        u'n̂': u'n̩'
    }
    seventh = {
        u'ā': u'a',
        u'ē': u'e',
        u'ī': u'i',
        u'ō': u'o',
        u'ū': u'u',
        u'm̄': u'm̩',
        u'n̄': u'n̩'
    }
    eighth = {
        u'a̍': u'a',
        u'e̍': u'e',
        u'i̍': u'i',
        u'o̍': u'o',
        u'u̍': u'u',
        u'm̍': u'm̩'
    }
    ipa_combinations = {
        u'tshi': u'tɕʰ',
        u'tsʰi': u'tɕʰ',
        u'tsi': u'tɕ',
        u'si': u'ɕ',
        u'ji': u'ʑ',
        u'tshe': u'tɕʰ',
        u'tsʰe': u'tɕʰ',
        u'tse': u'tɕ',
        u'se': u'ɕ',
        u'je': u'ʑ',
    }
    ipa_i_combinations = {
        u'tshi': u'tɕʰi',
        u'tsʰi': u'tɕʰi',
        u'tsi': u'tɕi',
        u'si': u'ɕi',
        u'ji': u'ʑi',
        u'tshe': u'tɕʰe',
        u'tsʰe': u'tɕʰe',
        u'tse': u'tɕe',
        u'se': u'ɕe',
        u'je': u'ʑe',
    }
    ipa_3_cons = {
        u'tsh': u'tsʰ',
    }
    ipa_2_cons = {
        u'ph': u'pʰ',
        u'th': u'tʰ',
        u'ng': u'ŋ',
        u'kh': u'kʰ'
    }
    ipa_1_cons = {
        u'j': u'z'
    }
    ipa_finals = {
        u'p': u'p̚',
        u't': u't̚',
        u'k': u'k̚',
        u'h': u'ʔ',
    }
    ipa_5_vowels = {
        u'iaunn': u'iãu',
        u'uainn': u'uãi',
    }
    ipa_4_vowels = {
        u'ainn': u'ãi',
        u'iann': u'iã',
        u'iunn': u'iũ',
        u'iong': u'iɔŋ',
        u'uann': u'uã',
    }
    ipa_3_vowels = {
        u'ann': u'ã',
        u'enn': u'ẽ',
        u'inn': u'ĩ',
        u'ioh': u'iəʔ',
        u'iok': u'iɔk',
        u'ong': u'ɔŋ',
        u'onn': u'ɔ̃',
    }
    ipa_2_vowels = {
        u'io': u'iə',
        u'oh': u'əʔ',
        u'ok': u'ɔk',
        u'op': u'ɔp',
        u'om': u'ɔm',
        u'oo': u'ɔ',
    }
    ipa_1_vowels = {
        u'o': u'ə',
    }

    def load(self):
        f = codecs.open('../txt/shijing_original/dialects/hokkien.txt', 'r', 'utf-8')
        for line in f:
            self.text.append(line)

    def vowel(self, s):
        seq = ''
        for char in s:
            if char in self.vowels:
                seq += char
        return seq

    def convert_combinations(self, w):
        vowels = self.vowel(w)
        if u'i' in vowels:
            if len(vowels) > 1:
                for comb in self.ipa_combinations:
                    w = w.replace(comb, self.ipa_combinations[comb])
            else:
                for comb in self.ipa_i_combinations:
                    w = w.replace(comb, self.ipa_i_combinations[comb])
        if vowels in u'':
            if u'ng' in w:
                w = w.replace(u'ng', u'ŋ̍')
            if u'n̩g' in w:
                w = w.replace(u'n̩g', u'ŋ̍')
            if u'ŋ' in w:
                w = w.replace(u'ŋ', u'ŋ̍')
            if u'm' in w:
                w = w.replace(u'm', u'm̩')
            if u'n' in w:
                w = w.replace(u'n', u'n̩')
        return w

    def bracket_words(self, word):
        result = []
        words_brackets = re.findall(u'([^ \(\),]+)', word)
        if len(words_brackets) > 0:
            for word in words_brackets:
                word = word.strip('\r\n')
                result.append(word)
        return result

    def convert_tone(self, w):
        for tone in self.second:
            if tone in w and '(' not in w:
                w = w.replace(tone, self.second[tone])
                w += u'51'
                return w
        for tone in self.third:
            if tone in w and '(' not in w:
                w = w.replace(tone, self.third[tone])
                w += u'21'
                return w
        for tone in self.fifth:
            if tone in w and '(' not in w:
                w = w.replace(tone, self.fifth[tone])
                w += u'24'
                return w
        for tone in self.seventh:
            if tone in w and '(' not in w:
                w = w.replace(tone, self.seventh[tone])
                w += u'33'
                return w
        for tone in self.eighth:
            if tone in w and '(' not in w:
                w = w.replace(tone, self.eighth[tone])
                w += u'5ʔ'
                return w
        if w[-1] in self.fourth:
            w += u'2ʔ'
            return w
        return w + u'55'

    def convert_vowels(self, w):
        for vowel in self.ipa_5_vowels:
            if vowel in w:
                w = w.replace(vowel, self.ipa_5_vowels[vowel])
                return w
        for vowel in self.ipa_4_vowels:
            if vowel in w:
                w = w.replace(vowel, self.ipa_4_vowels[vowel])
                return w
        for vowel in self.ipa_3_vowels:
            if vowel in w:
                w = w.replace(vowel, self.ipa_3_vowels[vowel])
                return w
        for vowel in self.ipa_2_vowels:
            if vowel in w:
                w = w.replace(vowel, self.ipa_2_vowels[vowel])
                return w
        for vowel in self.ipa_1_vowels:
            if vowel in w:
                w = w.replace(vowel, self.ipa_1_vowels[vowel])
                return w
        return w

    def convert_finals(self, w):
        for final in self.ipa_finals:
            num_pos = re.search(u'[0-9]+', w)
            if num_pos is not None:
                num = num_pos.group(0)
                position = w.find(num[0])
                if w[position-1] == final:
                    n = 0
                    new_w = u''
                    while n < position-1:
                        new_w += w[n]
                        n += 1
                    new_w += self.ipa_finals[w[position-1]]
                    new_w += w[position:]
                    return new_w
        return w

    def convert_cons(self, w):
        for cons in self.ipa_3_cons:
            if cons in w:
                w = w.replace(cons, self.ipa_3_cons[cons])
                return w
        for cons in self.ipa_2_cons:
            if cons in w:
                w = w.replace(cons, self.ipa_2_cons[cons])
                return w
        for cons in self.ipa_1_cons:
            if cons in w:
                w = w.replace(cons, self.ipa_1_cons[cons])
                return w

        num_pos = re.search(u'[0-9]+', w)
        if num_pos is not None:
            num = num_pos.group(0)
            position = w.find(num[0])
            if w[position-1] not in u'mngŋ':
                  if w[0] == u'b':
                    w = w.replace(w[0], u'ᵐb')
                    return w
                  if w[0] == u'g':
                    w = w.replace(w[0], u'ᵑɡ')
                    return w
        return w

    def convert_all(self, w):
        w = self.convert_vowels(w)
        w = self.convert_cons(w)
        w = self.convert_finals(w)
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
                        if w.startswith(u'-'):
                            w = w.replace(u'--', u'')
                            num_pos = re.search(u'[0-9]+', w)
                            if num_pos is not None:
                                num = num_pos.group(0)
                                w = w.replace(num, u'')
                        else:
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
                            result = word1 + '('
                            for word in brackets[1:]:
                                word = self.convert_tone(word)
                                word = self.convert_all(word)
                                result += word + ','
                            result += ')'
                            result = result.replace(',)', ')')
                            self.result += result + ' '
                else:
                    self.result += w + ' '
            self.result += '\n'
            self.result = self.result.replace(u' \n', '\n')
        self.out.write(self.result)


c = IPAConverter()
c.load()
c.transcribe()
print c.result