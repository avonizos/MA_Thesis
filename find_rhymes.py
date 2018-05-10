# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for finding Shijing rhymes
# Search in the same stanza, +-5 lines from the current
# Count statistics on rhymes (some require addtional coding/uncommenting lines)
# -----------------------------------------------------
# Rhyming types:
# 1-2 lines -- paired
# 1-3 lines -- crossed
# 1-4 lines -- encircling
# -----------------------------------------------------
# Rhyme types:
# inexact -- only vowel
# exact -- vowel + coda
# tonal inexact -- vowel + tone
# tonal exact -- vowel + tone + coda

import codecs
import re

f = codecs.open('csv/shijing_original/shijing_ipa.csv', 'r', 'utf-8')
out = codecs.open('csv/rhymes/rhymes_mandarin_ipa.csv', 'w', 'utf-8')

class Rhymes():
    text = []
    parsed = []
    parsed_tonal_inexact = []
    parsed_vowel_final = []
    parsed_final_tone = []
    cur_rhymes = 0
    chars = ''
    vowels = u'aɐeəiɨɔouãẽĩɔ̃ũɑɛyɿʅɤøœʊɪ' # Mandarin + Fuzhou + Cantonese
    parse = re.compile(u'(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)$')
    search_pron = re.compile(u'([^ ]+)$')
    search_tone = re.compile(u'([0-9]+)')
    stanzas_density = 0
    poem_density = 0
    no_rhyme = 0
    max_stanza_density = 0

    def density(self, cur_words):
        possible_rhymes = (len(cur_words) * (len(cur_words) - 1)) / 2
        if possible_rhymes != 0:
            if self.cur_rhymes/float(possible_rhymes) > 0.99:
                self.max_stanza_density += 1
            return self.cur_rhymes/float(possible_rhymes)
        return 0

    def search_rhymes(self, book, poem, stanza, cur_ch_words, cur_words, i, j):
        vowel1 = self.vowel(cur_words[i][0])
        vowel2 = self.vowel(cur_words[i+j][0])

        if vowel1 == vowel2:
            type = self.rhyming(cur_words[i][1] + 1, cur_words[i + j][1] + 1)
            rhyme = 'inexact'
            res = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d-%d\n' % (
                book, poem, stanza, cur_ch_words[i], cur_ch_words[i + j], cur_words[i][0][:-1],
                cur_words[i + j][0][:-1], rhyme, type, cur_words[i][1] + 1, cur_words[i + j][1] + 1)

            if self.is_same_tone(cur_words, i, j):
                if self.is_same_final(cur_words, vowel1, vowel2, i, j):
                    self.check_final_tone(book, poem, stanza, cur_ch_words, cur_words, i, j)
                else:
                    self.check_same_tone(book, poem, stanza, cur_ch_words, cur_words, i, j)
            else:
                if self.is_same_final(cur_words, vowel1, vowel2, i, j):
                    self.check_same_final(book, poem, stanza, cur_ch_words, cur_words, i, j)
                else:
                    if res not in self.parsed:
                        self.parsed.append(res)
                        out.write(res)
                        self.cur_rhymes += 1
                        print res

    def is_same_final(self, cur_words, vowel1, vowel2, i, j):
        ind1 = cur_words[i][0].find(vowel1[-1])
        ind2 = cur_words[i+j][0].find(vowel2[-1])
        if cur_words[i][0][ind1+1] not in '0123456789' and cur_words[i+j][0][ind2+1] not in '0123456789':
            if cur_words[i][0][ind1+1] == cur_words[i+j][0][ind2+1]:
                return True
        return False

    def is_same_tone(self, cur_words, i, j):
        t1 = re.search(self.search_tone, cur_words[i][0])
        t2 = re.search(self.search_tone, cur_words[i + j][0])
        if t1 is not None and t2 is not None:
            tone1 = t1.group(1)
            tone2 = t2.group(1)
            if tone1 == tone2:
                return True
        return False

    def check_final_tone(self, book, poem, stanza, cur_ch_words, cur_words, i, j):
        type = self.rhyming(cur_words[i][1] + 1, cur_words[i + j][1] + 1)
        rhyme = 'tonal exact'
        res = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d-%d\n' % (
            book, poem, stanza, cur_ch_words[i], cur_ch_words[i + j], cur_words[i][0][:-1],
            cur_words[i + j][0][:-1], rhyme, type, cur_words[i][1] + 1, cur_words[i + j][1] + 1)
        if res not in self.parsed_final_tone:
            self.parsed_final_tone.append(res)
            out.write(res)
            print res
            self.cur_rhymes += 1

    def check_same_final(self, book, poem, stanza, cur_ch_words, cur_words, i, j):
        type = self.rhyming(cur_words[i][1] + 1, cur_words[i + j][1] + 1)
        rhyme = 'exact'
        res = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d-%d\n' % (
            book, poem, stanza, cur_ch_words[i], cur_ch_words[i + j], cur_words[i][0][:-1],
            cur_words[i + j][0][:-1], rhyme, type, cur_words[i][1] + 1, cur_words[i + j][1] + 1)
        if res not in self.parsed_vowel_final:
            self.parsed_vowel_final.append(res)
            out.write(res)
            print res
            self.cur_rhymes += 1

    def check_same_tone(self, book, poem, stanza, cur_ch_words, cur_words, i, j):
        type = self.rhyming(cur_words[i][1] + 1, cur_words[i + j][1] + 1)
        rhyme = 'tonal inexact'
        res = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d-%d\n' % (
            book, poem, stanza, cur_ch_words[i], cur_ch_words[i + j], cur_words[i][0][:-1],
            cur_words[i + j][0][:-1], rhyme, type, cur_words[i][1] + 1, cur_words[i + j][1] + 1)
        if res not in self.parsed_tonal_inexact:
            self.parsed_tonal_inexact.append(res)
            out.write(res)
            self.cur_rhymes += 1

    def vowel(self, s):
        seq = ''
        for char in s:
            if char not in self.chars:
                self.chars += char
            if char in self.vowels:
                seq += char
        if seq == '':
            if u'ŋ̍' in s:
                seq = u'ŋ̍'
            if u'm̩' in s:
                seq = u'm̩'
        return seq

    # Rhyming type
    def rhyming(self, i, j):
        if j - i == 1:
            return 'paired'
        elif j - i == 2:
            return 'crossed'
        elif j - i == 3:
            return 'encircling'
        else:
            return '-'

    def find(self):
        out.write("Part\tPoem\tStanza\tWord1\tWord2\tIPA1\tIPA2\tType\tRhyming\tLines\n")
        cur_poem = 'Guan Ju'
        cur_stanza = 1
        cur_words = []
        cur_ch_words = []
        num_line = 0
        poem_words = []

        for line in f:
            self.text.append(line)

        for line in self.text:
            if line[-3] != '-':
                find_parts = re.search(self.parse, line)
                if find_parts is not None:
                    book = find_parts.group(1)
                    poem = find_parts.group(2)
                    stanza = int(find_parts.group(3))
                    ch_line = find_parts.group(4)
                    pn_line = find_parts.group(5)
                    pron = re.search(self.search_pron, pn_line)
                    if (poem == cur_poem):
                        if (stanza == cur_stanza):
                            if (pron is not None):
                                cur_ch_words.append(ch_line[-2])
                                cur_words.append([pron.group(1), num_line])
                                poem_words.append(pron.group(1))
                        else:
                            for i in range(len(cur_words)):
                                j = 1
                                while j <= 5 and i + j < len(cur_words):
                                    self.search_rhymes(book, poem, stanza, cur_ch_words, cur_words, i, j)
                                    j += 1
                            #print "Current stanza density is: %.2f" % self.density(cur_words)
                            #self.stanzas_density += self.density(cur_words)
                            cur_stanza = stanza
                            cur_words = []
                            cur_ch_words = []
                            #self.cur_rhymes = 0
                    else:
                        #print "Current poem density is: %.2f" % self.density(poem_words)
                        #self.poem_density += self.density(poem_words)
                        cur_poem = poem
                        cur_stanza = 1
                        cur_words = []
                        cur_ch_words = []
                        poem_words = []
                        #self.cur_rhymes = 0
            num_line += 1


r = Rhymes()
r.find()

all = len(r.parsed) + len(r.parsed_vowel_final) + len(r.parsed_tonal_inexact) + len(r.parsed_final_tone)

print "All: %d" % all
print "Only vowel: %s" % len(r.parsed)     # Only vowel
print "Vowel + coda: %s" % len(r.parsed_vowel_final)     # Only vowel
print "Vowel + tone: %s" % len(r.parsed_tonal_inexact) # Vowel + tone
print "Vowel + coda + tone: %s" % len(r.parsed_final_tone) # Vowel + tone
#print "Average stanza rhyme density: %.2f" % (r.stanzas_density/float(1141))
#print "Average poem rhyme density: %.2f" % (r.poem_density/float(305))
#print "Overall density: %.5f percent" % ( (all / float(26597571)) * 100)
#print "Amount of max stanza density: %d, %.2f percent" % (r.max_stanza_density, (r.max_stanza_density/float(1141)) * 100)
#print "No ending characters: %d, %.5f" % (r.no_rhyme, (r.no_rhyme/float(7294)))

