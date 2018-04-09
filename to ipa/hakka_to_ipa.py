# -*- coding: utf-8 -*-

import codecs
import re

class IPAConverter():
    out = codecs.open('../txt/ipa ambiguous/hakka_ipa.txt', 'w', 'utf-8')
    text = []
    result = ''
    search_pron = re.compile(u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?'
                             u'([^ ]+)? ?([^ ]+)? ?')
    vowels = u'aeuiɨoy'

    initials = {
        u'ng': u'ŋ',
        u'z': u'ts',
        u'c': u'tsʰ',
        u'b': u'p',
        u'p': u'pʰ',
        u'd': u't',
        u't': u'tʰ',
        u'g': u'k',
        u'k': u'kʰ',
        u'j': u'tɕ',
        u'q': u'tɕʰ',
        u'x': u'ɕ',
    }
    finals = {
        u'uang': u'uaŋ',
        u'iung': u'iuŋ',
        u'iong': u'ioŋ',
        u'iang': u'iaŋ',
        u'ang': u'aŋ',
        u'ong': u'oŋ',
        u'ung': u'uŋ',
        u'iag': u'iak̚',
        u'iog': u'iok̚',
        u'iug': u'iuk̚',
        u'uag': u'uak̚',
        u'iib': u'ɨp̚',
        u'iab': u'iap̚',
        u'ieb': u'iep̚',
        u'iid': u'ɨt̚',
        u'iad': u'iat̚',
        u'ied': u'iet̚',
        u'iod': u'iot̚',
        u'iud': u'iut̚',
        u'uad': u'uat̚',
        u'ued': u'uet̚',
        u'ii': u'ɨ',
        u'ab': u'ap̚',
        u'eb': u'ep̚',
        u'ib': u'ip̚',
        u'ad': u'at̚',
        u'od': u'ot̚',
        u'id': u'it̚',
        u'ed': u'et̚',
        u'ud': u'ut̚',
        u'ag': u'ak̚',
        u'og': u'ok̚',
        u'ug': u'uk̚'
    }

    def load(self):
        f = codecs.open('../txt/shijing_original/dialects/hakka.txt', 'r', 'utf-8')
        for line in f:
            self.text.append(line)

    def vowel(self, s):
        seq = ''
        for char in s:
            if char in self.vowels:
                seq += char
        if seq == '':
            if u'ng' in s:
                seq = u'ŋ̍'
            if u'm' in s:
                seq = u'm̩'
            if u'n' in s:
                seq = u'n̩'
        return seq

    def bracket_words(self, word):
        result = []
        words_brackets = re.findall(u'([^ \(\),]+)', word)
        if len(words_brackets) > 0:
            for word in words_brackets:
                word = word.strip('\r\n')
                result.append(word)
        return result

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
        final = w[ind:]
        final = final.replace('1', '')
        final = final.replace('2', '')
        final = final.replace('3', '')
        final = final.replace('4', '')
        final = final.replace('5', '')
        if final in self.finals:
            w = w.replace(final, self.finals[final])
        return w

    def convert_all(self, w):
        w = self.convert_final(w)
        w = self.convert_initial(w)
        # w = self.convert_cons(w)
        # w = self.convert_finals(w)
        # w = self.convert_combinations(w)
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
                        # w = self.convert_tone(w)
                        w = self.convert_all(w)
                        self.result += w + ' '
                    else:
                        brackets = self.bracket_words(w)
                        if len(brackets) == 2 and brackets[0] == brackets[1]:
                            w = brackets[0]
                            # w = self.convert_tone(w)
                            w = self.convert_all(w)
                            self.result += w + ' '
                        else:
                            # word1 = self.convert_tone(brackets[0])
                            word1 = self.convert_all(brackets[0])
                            result = word1 + '('
                            for word in brackets[1:]:
                                # word = self.convert_tone(word)
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