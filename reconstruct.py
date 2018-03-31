# -*- coding: utf-8 -*-

import codecs
import re

class Reconstructor():
    f = codecs.open('txt/reconstruction/fuzhou_hokkien.txt', 'r', 'utf-8')
    search_last = (u'(.*) (.*?)\t(.*) (.*?)$')
    all_vowels = u'aeəiouãẽĩɔ̃ũɑɛyɿʅɤøœ' # Mandarin + Fuzhou ɔøœ
    numbers = re.compile(u'([0-9]+)')
    initials = {}
    finals = {}
    vowels = {}
    tones = {}
    vowel_final_tone = {}
    vowel_final = {}

    def find_vowels(self, vowel1, vowel2):
        if vowel1 not in self.vowels:
            self.vowels[vowel1] = {}
        if vowel2 not in self.vowels[vowel1]:
            self.vowels[vowel1][vowel2] = 1
        else:
            self.vowels[vowel1][vowel2] += 1

    def find_tones(self, last1, last2):
        tone1 = ' '
        tone2 = ' '
        if u'5ʔ' in last2:
            tone2 = u'5ʔ'
        else:
            if u'3ʔ' in last2:
                tone2 = u'3ʔ'
            else:
                nums2 = re.search(self.numbers, last2)
                if nums2 is not None:
                    tone2 = nums2.group(1)
        nums1 = re.search(self.numbers, last1)
        if nums1 is not None:
            ind = last1.find(nums1.group(1))
            if last1[ind-1] == u'ʔ':
                tone1 = u'ʔ' + nums1.group(1)
            else:
                tone1 = nums1.group(1)
        if tone1 not in self.tones:
            self.tones[tone1] = {}
        if tone2 not in self.tones[tone1]:
            self.tones[tone1][tone2] = 1
        else:
            self.tones[tone1][tone2] += 1

    def find_vowel_final_tone(self, last1, last2, vowel1, vowel2):
        ind1 = last1.find(vowel1[0])
        ind2 = last2.find(vowel2[0])
        last1 = last1.replace(last1[0:ind1], '')
        last2 = last2.replace(last2[0:ind2], '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        if last1 not in self.vowel_final_tone:
            self.vowel_final_tone[last1] = {}
        if last2 not in self.vowel_final_tone[last1]:
            self.vowel_final_tone[last1][last2] = 1
        else:
            self.vowel_final_tone[last1][last2] += 1

    def find_vowel_final(self, last1, last2, vowel1, vowel2):
        ind1 = last1.find(vowel1[0])
        ind2 = last2.find(vowel2[0])
        last1 = last1.replace(last1[0:ind1], '')
        last2 = last2.replace(last2[0:ind2], '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        last2 = last2.replace(u'5ʔ', '')
        last2 = last2.replace(u'3ʔ', '')
        nums1 = re.search(self.numbers, last1)
        nums2 = re.search(self.numbers, last2)
        if nums1 is not None:
            last1 = last1.replace(nums1.group(1), '')
        if nums2 is not None:
            last2 = last2.replace(nums2.group(1), '')
        if last1 not in self.vowel_final:
            self.vowel_final[last1] = {}
        if last2 not in self.vowel_final[last1]:
            self.vowel_final[last1][last2] = 1
        else:
            self.vowel_final[last1][last2] += 1

    def find_initials(self, last1, last2, vowel1, vowel2):
        ind1 = last1.find(vowel1[0])
        ind2 = last2.find(vowel2[0])
        initial1 = last1[:ind1]
        initial2 = last2[:ind2]
        if initial1 not in self.initials:
            self.initials[initial1] = {}
        if initial2 not in self.initials[initial1]:
            self.initials[initial1][initial2] = 1
        else:
            self.initials[initial1][initial2] += 1

    def find_finals(self, last1, last2, vowel1, vowel2):
        ind1 = last1.find(vowel1[-1])
        ind2 = last2.find(vowel2[-1])
        last1 = last1.replace(last1[0:ind1+1], '')
        last2 = last2.replace(last2[0:ind2+1], '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        last2 = last2.replace(u'5ʔ', '')
        last2 = last2.replace(u'3ʔ', '')
        nums1 = re.search(self.numbers, last1)
        nums2 = re.search(self.numbers, last2)
        if nums1 is not None:
            last1 = last1.replace(nums1.group(1), '')
        if nums2 is not None:
            last2 = last2.replace(nums2.group(1), '')
        if last1 not in self.finals:
            self.finals[last1] = {}
        if last2 not in self.finals[last1]:
            self.finals[last1][last2] = 1
        else:
            self.finals[last1][last2] += 1

    def load(self):
        for line in self.f:
            last = re.search(self.search_last, line)
            if last is not None:
                last1 = last.group(2)
                last2 = last.group(4)
                if u'-' not in last1:
                    if u'-' not in last2:
                        vowel1 = self.vowel(last1)
                        vowel2 = self.vowel(last2)
                        self.find_initials(last1, last2, vowel1, vowel2)
                        self.find_vowels(vowel1, vowel2)
                        self.find_tones(last1, last2)
                        self.find_vowel_final(last1, last2, vowel1, vowel2)
                        self.find_vowel_final_tone(last1, last2, vowel1, vowel2)
                        self.find_finals(last1, last2, vowel1, vowel2)

    def vowel(self, s):
        seq = ''
        for char in s:
            if char in self.all_vowels:
                seq += char
        if seq == '':
            if u'ŋ' in s:
                seq = u'ŋ'
            if u'm' in s:
                seq = u'm'
        return seq

r = Reconstructor()
r.load()

print "INITIALS"
for in1 in r.initials:
    for in2 in r.initials[in1]:
        print "%s\t%s\t%d" % (in1, in2, r.initials[in1][in2])

print "\nVOWELS"
for v1 in r.vowels:
    for v2 in r.vowels[v1]:
        print "%s\t%s\t%d" % (v1, v2, r.vowels[v1][v2])

print "\nTONES"
for t1 in r.tones:
    for t2 in r.tones[t1]:
        print "%s\t%s\t%d" % (t1, t2, r.tones[t1][t2])

print "\nVOWELS + FINALS"
for f1 in r.vowel_final:
    for f2 in r.vowel_final[f1]:
        print "%s\t%s\t%d" % (f1, f2, r.vowel_final[f1][f2])

print "\nVOWELS + FINALS + TONES"
for f1 in r.vowel_final_tone:
    for f2 in r.vowel_final_tone[f1]:
        print "%s\t%s\t%d" % (f1, f2, r.vowel_final_tone[f1][f2])

print "\nFINALS"
for f1 in r.finals:
    for f2 in r.finals[f1]:
        print "%s\t%s\t%d" % (f1, f2, r.finals[f1][f2])