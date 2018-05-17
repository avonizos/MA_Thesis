# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for reconstructing Old Chinese
# pronunciation based on 5 Chinese dialects

import codecs
import re

class Reconstructor():
    f = codecs.open('result_descend.csv', 'r', 'utf-8')
    out = codecs.open('reconstructed_forms.txt', 'w', 'utf-8')
    f2 = codecs.open('ending_chars.txt', 'r', 'utf-8')
    find_all = re.compile(u'(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\r\n')
    initials = []
    finals = []
    codas = []
    vowels = []
    reconstructed_init = {}
    reconstructed_fin = {}
    reconstructed_cod = {}
    reconstructed_vow = {}
    chars = {}

    def load(self):
        for line in self.f:
            amount = re.search(self.find_all, line)
            if amount is not None:
                if int(amount.group(7)) > 20:
                    if amount.group(1) == u'INITIALS':
                        self.initials.append(line)
                    if amount.group(1) == u'FINALS':
                        self.finals.append(line)
                    if amount.group(1) == u'CODAS':
                        self.codas.append(line)
                    
        n = 0
        for line in self.f2:
            self.chars[n] = line.strip()
            n += 1

    def reconstruct_type(self, dic, arr):
        n = 0
        while n <= 7293:
            dic[n] = '-'
            n += 1
        for el in arr:
            cur_lines = []
            print el
            lines = re.search(self.find_all, el)
            if lines is not None:
                cur_lines = lines.group(8).split(',')
                for num in cur_lines:
                    print self.chars[int(num)-1],
            print '\n'
            input = raw_input(u'Type your decision: ')
            for num in cur_lines:
                dic[num] = input

    def reconstruct(self):
        self.reconstruct_type(self.reconstructed_init, self.initials)
        self.reconstruct_type(self.reconstructed_fin, self.finals)
        self.reconstruct_type(self.reconstructed_cod, self.codas)

    def results(self):
        n = 0
        while n < 7294:
            res = str(n) + '\t'
            init = '-'
            fin = '-'
            vow = '-'
            cod = '-'
            if str(n) in self.reconstructed_init:
                init = self.reconstructed_init[str(n)]
            if str(n) in self.reconstructed_fin:
                fin = self.reconstructed_fin[str(n)]
            if str(n) in self.reconstructed_cod:
                cod = self.reconstructed_cod[str(n)]
            res += init + '\t' + fin + '\t' + cod
            print res
            n += 1

r = Reconstructor()
r.load()
r.reconstruct()
r.results()
