# -*- coding: utf-8 -*-

import codecs
import re

class Reconstructor():
    f = codecs.open('txt/reconstruction/mandarin_fuzhou_hokkien_cantonese_hakka.txt', 'r', 'utf-8')
    f1 = codecs.open('txt/shijing_original/characters_trad.txt', 'r', 'utf-8')
    out = codecs.open('txt/reconstruction/results.csv', 'w', 'utf-8')
    search_last = (u'(.*) (.*?)\t(.*) (.*?)\t(.*) (.*?)\t(.*) (.*?)\t(.*) (.*?)$')
    all_vowels = u'aɐeəiɨɔouãẽĩɔ̃ũɑɛyɿʅɤøœ' # Mandarin + Fuzhou ɔøœ + Cantonese ɐ
    numbers = re.compile(u'([0-9]+)')
    initials = {}
    finals = {}
    vowels = {}
    tones = {}
    vowel_final_tone = {}
    vowel_final = {}
    sum = 0
    chars = []

    def find_vowels(self, vowel1, vowel2, vowel3, vowel4, vowel5, last1, last2, last3, last4, last5):
        if vowel1 not in self.vowels:
            self.vowels[vowel1] = {}
        if vowel2 not in self.vowels[vowel1]:
            self.vowels[vowel1][vowel2] = {}
        if vowel3 not in self.vowels[vowel1][vowel2]:
            self.vowels[vowel1][vowel2][vowel3] = {}
        if vowel4 not in self.vowels[vowel1][vowel2][vowel3]:
            self.vowels[vowel1][vowel2][vowel3][vowel4] = {}
        if vowel5 not in self.vowels[vowel1][vowel2][vowel3][vowel4]:
            self.vowels[vowel1][vowel2][vowel3][vowel4][vowel5] = []
        else:
            self.vowels[vowel1][vowel2][vowel3][vowel4][vowel5].append(last1)
            self.vowels[vowel1][vowel2][vowel3][vowel4][vowel5].append(last2)
            self.vowels[vowel1][vowel2][vowel3][vowel4][vowel5].append(last3)
            self.vowels[vowel1][vowel2][vowel3][vowel4][vowel5].append(last4)
            self.vowels[vowel1][vowel2][vowel3][vowel4][vowel5].append(last5)

    def find_tones(self, last1, last2, last3, last4, last5):
        tone1 = ' '
        tone2 = ' '
        tone3 = ' '
        tone4 = ' '
        tone5 = ' '
        if u'5ʔ' in last3:
            tone3 = u'5ʔ'
        else:
            if u'3ʔ' in last3:
                tone3 = u'3ʔ'
            else:
                nums3 = re.search(self.numbers, last3)
                if nums3 is not None:
                    tone3 = nums3.group(1)
        nums1 = re.search(self.numbers, last1)
        if nums1 is not None:
            ind = last1.find(nums1.group(1))
            if last1[ind-1] == u'ʔ':
                tone1 = u'ʔ' + nums1.group(1)
            else:
                tone1 = nums1.group(1)
        nums2 = re.search(self.numbers, last2)
        if nums2 is not None:
            ind = last2.find(nums2.group(1))
            if last2[ind - 1] == u'ʔ':
                tone2 = u'ʔ' + nums2.group(1)
            else:
                tone2 = nums2.group(1)
        nums4 = re.search(self.numbers, last4)
        if nums4 is not None:
            ind = last4.find(nums4.group(1))
            if last4[ind - 1] == u'ʔ':
                tone4 = u'ʔ' + nums4.group(1)
            else:
                tone4 = nums4.group(1)
        nums5 = re.search(self.numbers, last5)
        if nums5 is not None:
            ind = last5.find(nums5.group(1))
            if last5[ind - 1] == u'ʔ':
                tone5 = u'ʔ' + nums5.group(1)
            else:
                tone5 = nums5.group(1)
        if tone1 not in self.tones:
            self.tones[tone1] = {}
        if tone2 not in self.tones[tone1]:
            self.tones[tone1][tone2] = {}
        if tone3 not in self.tones[tone1][tone2]:
            self.tones[tone1][tone2][tone3] = {}
        if tone4 not in self.tones[tone1][tone2][tone3]:
            self.tones[tone1][tone2][tone3][tone4] = {}
        if tone5 not in self.tones[tone1][tone2][tone3][tone4]:
            self.tones[tone1][tone2][tone3][tone4][tone5] = []
        else:
            self.tones[tone1][tone2][tone3][tone4][tone5].append(last1)
            self.tones[tone1][tone2][tone3][tone4][tone5].append(last2)
            self.tones[tone1][tone2][tone3][tone4][tone5].append(last3)
            self.tones[tone1][tone2][tone3][tone4][tone5].append(last4)
            self.tones[tone1][tone2][tone3][tone4][tone5].append(last5)

    def find_vowel_final_tone(self, last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5):
        ind1 = last1.find(vowel1[0])
        ind2 = last2.find(vowel2[0])
        ind3 = last3.find(vowel3[0])
        ind4 = last4.find(vowel4[0])
        ind5 = last5.find(vowel5[0])
        last1 = last1.replace(last1[0:ind1], '')
        last2 = last2.replace(last2[0:ind2], '')
        last3 = last3.replace(last3[0:ind3], '')
        last4 = last4.replace(last4[0:ind4], '')
        last5 = last5.replace(last5[0:ind5], '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        last3 = last3.replace('\r', '')
        last4 = last4.replace('\r', '')
        last5 = last5.replace('\r', '')
        if last1 not in self.vowel_final_tone:
            self.vowel_final_tone[last1] = {}
        if last2 not in self.vowel_final_tone[last1]:
            self.vowel_final_tone[last1][last2] = {}
        if last3 not in self.vowel_final_tone[last1][last2]:
            self.vowel_final_tone[last1][last2][last3] = {}
        if last4 not in self.vowel_final_tone[last1][last2][last3]:
            self.vowel_final_tone[last1][last2][last3][last4] = {}
        if last5 not in self.vowel_final_tone[last1][last2][last3][last4]:
            self.vowel_final_tone[last1][last2][last3][last4][last5] = []
        else:
            self.vowel_final_tone[last1][last2][last3][last4][last5].append(last1)
            self.vowel_final_tone[last1][last2][last3][last4][last5].append(last2)
            self.vowel_final_tone[last1][last2][last3][last4][last5].append(last3)
            self.vowel_final_tone[last1][last2][last3][last4][last5].append(last4)
            self.vowel_final_tone[last1][last2][last3][last4][last5].append(last5)

    def find_vowel_final(self, last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5):
        ind1 = last1.find(vowel1[0])
        ind2 = last2.find(vowel2[0])
        ind3 = last3.find(vowel3[0])
        ind4 = last4.find(vowel4[0])
        ind5 = last5.find(vowel5[0])
        last1 = last1.replace(last1[0:ind1], '')
        last2 = last2.replace(last2[0:ind2], '')
        last3 = last3.replace(last3[0:ind3], '')
        last4 = last4.replace(last4[0:ind4], '')
        last5 = last5.replace(last5[0:ind5], '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        last3 = last3.replace('\r', '')
        last4 = last4.replace('\r', '')
        last5 = last5.replace('\r', '')
        last3 = last3.replace(u'5ʔ', '')
        last3 = last3.replace(u'3ʔ', '')
        nums1 = re.search(self.numbers, last1)
        nums2 = re.search(self.numbers, last2)
        nums3 = re.search(self.numbers, last3)
        nums4 = re.search(self.numbers, last4)
        nums5 = re.search(self.numbers, last5)
        if nums1 is not None:
            last1 = last1.replace(nums1.group(1), '')
        if nums2 is not None:
            last2 = last2.replace(nums2.group(1), '')
        if nums3 is not None:
            last3 = last3.replace(nums3.group(1), '')
        if nums4 is not None:
            last4 = last4.replace(nums4.group(1), '')
        if nums5 is not None:
            last5 = last5.replace(nums5.group(1), '')
        if last1 not in self.vowel_final:
            self.vowel_final[last1] = {}
        if last2 not in self.vowel_final[last1]:
            self.vowel_final[last1][last2] = {}
        if last3 not in self.vowel_final[last1][last2]:
            self.vowel_final[last1][last2][last3] = {}
        if last4 not in self.vowel_final[last1][last2][last3]:
            self.vowel_final[last1][last2][last3][last4] = {}
        if last5 not in self.vowel_final[last1][last2][last3][last4]:
            self.vowel_final[last1][last2][last3][last4][last5] = []
        else:
            self.vowel_final[last1][last2][last3][last4][last5].append(last1)
            self.vowel_final[last1][last2][last3][last4][last5].append(last2)
            self.vowel_final[last1][last2][last3][last4][last5].append(last3)
            self.vowel_final[last1][last2][last3][last4][last5].append(last4)
            self.vowel_final[last1][last2][last3][last4][last5].append(last5)

    def find_initials(self, last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5):
        ind1 = last1.find(vowel1[0])
        ind2 = last2.find(vowel2[0])
        ind3 = last3.find(vowel3[0])
        ind4 = last4.find(vowel4[0])
        ind5 = last5.find(vowel5[0])
        initial1 = last1[:ind1]
        initial2 = last2[:ind2]
        initial3 = last3[:ind3]
        initial4 = last4[:ind4]
        initial5 = last5[:ind5]
        if initial1 not in self.initials:
            self.initials[initial1] = {}
        if initial2 not in self.initials[initial1]:
            self.initials[initial1][initial2] = {}
        if initial3 not in self.initials[initial1][initial2]:
            self.initials[initial1][initial2][initial3] = {}
        if initial4 not in self.initials[initial1][initial2][initial3]:
            self.initials[initial1][initial2][initial3][initial4] = {}
        if initial5 not in self.initials[initial1][initial2][initial3][initial4]:
            self.initials[initial1][initial2][initial3][initial4][initial5] = []
        else:
            self.initials[initial1][initial2][initial3][initial4][initial5].append(last1)
            self.initials[initial1][initial2][initial3][initial4][initial5].append(last2)
            self.initials[initial1][initial2][initial3][initial4][initial5].append(last3)
            self.initials[initial1][initial2][initial3][initial4][initial5].append(last4)
            self.initials[initial1][initial2][initial3][initial4][initial5].append(last5)

    def find_finals(self, last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5):
        ind1 = last1.find(vowel1[-1])
        ind2 = last2.find(vowel2[-1])
        ind3 = last3.find(vowel3[-1])
        ind4 = last4.find(vowel4[-1])
        ind5 = last5.find(vowel5[-1])
        last1 = last1.replace(last1[0:ind1+1], '')
        last2 = last2.replace(last2[0:ind2+1], '')
        last3 = last3.replace(last3[0:ind3+1], '')
        last4 = last4.replace(last4[0:ind4+1], '')
        last5 = last5.replace(last5[0:ind5+1], '')
        last1 = last1.replace('\r', '')
        last2 = last2.replace('\r', '')
        last3 = last3.replace('\r', '')
        last4 = last4.replace('\r', '')
        last5 = last5.replace('\r', '')
        last3 = last3.replace(u'5ʔ', '')
        last3 = last3.replace(u'3ʔ', '')
        nums1 = re.search(self.numbers, last1)
        nums2 = re.search(self.numbers, last2)
        nums3 = re.search(self.numbers, last3)
        nums4 = re.search(self.numbers, last4)
        nums5 = re.search(self.numbers, last5)
        if nums1 is not None:
            last1 = last1.replace(nums1.group(1), '')
        if nums2 is not None:
            last2 = last2.replace(nums2.group(1), '')
        if nums3 is not None:
            last3 = last3.replace(nums3.group(1), '')
        if nums4 is not None:
            last4 = last4.replace(nums4.group(1), '')
        if nums5 is not None:
            last5 = last5.replace(nums5.group(1), '')
        if last1 not in self.finals:
            self.finals[last1] = {}
        if last2 not in self.finals[last1]:
            self.finals[last1][last2] = {}
        if last3 not in self.finals[last1][last2]:
            self.finals[last1][last2][last3] = {}
        if last4 not in self.finals[last1][last2][last3]:
            self.finals[last1][last2][last3][last4] = {}
        if last5 not in self.finals[last1][last2][last3][last4]:
            self.finals[last1][last2][last3][last4][last5] = []
        else:
            self.finals[last1][last2][last3][last4][last5].append(last1)
            self.finals[last1][last2][last3][last4][last5].append(last2)
            self.finals[last1][last2][last3][last4][last5].append(last3)
            self.finals[last1][last2][last3][last4][last5].append(last4)
            self.finals[last1][last2][last3][last4][last5].append(last5)

    def load_chars(self):
        for line in self.f1:
            char = line[-4]
            self.chars.append(char)

    def load(self):
        # num = 1
        # all_num = 0
        # self.load_chars()
        # used = []
        for line in self.f:
            last = re.search(self.search_last, line)
            if last is not None:
                last1 = last.group(2)
                last2 = last.group(4)
                last3 = last.group(6)
                last4 = last.group(8)
                last5 = last.group(10)
                print last1, last2, last3, last4, last5
                if u'-' not in last1 and u'-' not in last2 and\
                     u'-' not in last3 and u'-' not in last4 and u'-' not in last5:
                        # char = self.chars[all_num]
                        # if char not in used:
                        #     used.append(char)
                        # s1 = str(num) + '\t' + last1 + '\tMandarin\t' + str(used.index(char)+1) + '\t' + char
                        # s2 = str(num+1) + '\t' + last2 + '\tFuzhou\t' + str(used.index(char)+1) + '\t' + char
                        # s3 = str(num+2) + '\t' + last3 + '\tHokkien\t' + str(used.index(char)+1) + '\t' + char
                        # s4 = str(num+3) + '\t' + last4 + '\tCantonese\t' + str(used.index(char)+1) + '\t' + char
                        # s5 = str(num+4) + '\t' + last5.strip('\r\n') + '\tHakka\t' + str(used.index(char)+1) + '\t' + char
                        # print s1
                        # print s2
                        # print s3
                        # print s4
                        # print s5
                        # num = num+5

                        vowel1 = self.vowel(last1)
                        vowel2 = self.vowel(last2)
                        vowel3 = self.vowel(last3)
                        vowel4 = self.vowel(last4)
                        vowel5 = self.vowel(last5)
                        self.find_initials(last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5)
                        self.find_vowels(vowel1, vowel2, vowel3, vowel4, vowel5, last1, last2, last3, last4, last5)
                        self.find_tones(last1, last2, last3, last4, last5)
                        self.find_vowel_final(last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5)
                        self.find_vowel_final_tone(last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5)
                        self.find_finals(last1, last2, last3, last4, last5, vowel1, vowel2, vowel3, vowel4, vowel5)
                        self.sum += 1
            # all_num += 1

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
            if u'ŋ̩' in s:
                seq = u'ŋ̩'
            if u'm̩' in s:
                seq = u'm̩'
        return seq

r = Reconstructor()
r.load()

print "INITIALS"
for in1 in r.initials:
    for in2 in r.initials[in1]:
        for in3 in r.initials[in1][in2]:
            for in4 in r.initials[in1][in2][in3]:
                for in5 in r.initials[in1][in2][in3][in4]:
                    print "%s\t%s\t%s\t%s\t%s\t%d" % (in1, in2, in3, in4, in5, len(r.initials[in1][in2][in3][in4][in5]))
                    for el in r.initials[in1][in2][in3][in4][in5]:
                        print el

print "\nVOWELS"
for in1 in r.vowels:
    for in2 in r.vowels[in1]:
        for in3 in r.vowels[in1][in2]:
            for in4 in r.vowels[in1][in2][in3]:
                for in5 in r.vowels[in1][in2][in3][in4]:
                    print "%s\t%s\t%s\t%s\t%s\t%d" % (in1, in2, in3, in4, in5, len(r.vowels[in1][in2][in3][in4][in5]))
                    for el in r.vowels[in1][in2][in3][in4][in5]:
                        print el

print "\nTONES"
for in1 in r.tones:
    for in2 in r.tones[in1]:
        for in3 in r.tones[in1][in2]:
            for in4 in r.tones[in1][in2][in3]:
                for in5 in r.tones[in1][in2][in3][in4]:
                    print "%s\t%s\t%s\t%s\t%s\t%d" % (in1, in2, in3, in4, in5, len(r.tones[in1][in2][in3][in4][in5]))
                    for el in r.tones[in1][in2][in3][in4][in5]:
                        print el

print "\nVOWELS + FINALS"
for in1 in r.vowel_final:
    for in2 in r.vowel_final[in1]:
        for in3 in r.vowel_final[in1][in2]:
            for in4 in r.vowel_final[in1][in2][in3]:
                for in5 in r.vowel_final[in1][in2][in3][in4]:
                    print "%s\t%s\t%s\t%s\t%s\t%d" % (in1, in2, in3, in4, in5, len(r.vowel_final[in1][in2][in3][in4][in5]))
                    for el in r.vowel_final[in1][in2][in3][in4][in5]:
                        print el

print "\nVOWELS + FINALS + TONES"
for in1 in r.vowel_final_tone:
    for in2 in r.vowel_final_tone[in1]:
        for in3 in r.vowel_final_tone[in1][in2]:
            for in4 in r.vowel_final_tone[in1][in2][in3]:
                for in5 in r.vowel_final_tone[in1][in2][in3][in4]:
                    print "%s\t%s\t%s\t%s\t%s\t%d" % (in1, in2, in3, in4, in5, len(r.vowel_final_tone[in1][in2][in3][in4][in5]))
                    for el in r.vowel_final_tone[in1][in2][in3][in4][in5]:
                        print el

print "\nFINALS"
for in1 in r.finals:
    for in2 in r.finals[in1]:
        for in3 in r.finals[in1][in2]:
            for in4 in r.finals[in1][in2][in3]:
                for in5 in r.finals[in1][in2][in3][in4]:
                    print "%s\t%s\t%s\t%s\t%s\t%d" % (in1, in2, in3, in4, in5, len(r.finals[in1][in2][in3][in4][in5]))
                    for el in r.finals[in1][in2][in3][in4][in5]:
                        print el

# print r.sum