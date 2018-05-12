# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for disambiguating the pronunciation of the Shijing rhymes
# in the dialectal texts

import codecs
import re

class Disambiguator():
    f1 = codecs.open('txt/ipa ambiguous/hokkien_ipa.txt', 'r', 'utf-8')
    f2 = codecs.open('txt/shijing_original/mandarin/mandarin_ipa.txt', 'r', 'utf-8')
    f3 = codecs.open('csv/rhymes/rhymes_mandarin_ipa.csv', 'r', 'utf-8')
    f4 = codecs.open('txt/ipa disambiguated/hokkien_disambiguated_1.txt', 'w', 'utf-8')
    search_last = re.compile(u'([^ ]+)$')
    search_nums = re.compile(u'([0-9]+)-([0-9]+)')
    search_rhymes = re.compile(u'(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t')
    lines = {}
    lines_mandarin = []
    lines_rhymes = []
    original_dialect = []
    decisions = {}

    def no_brackets(self, line):
        last = re.search(self.search_last, line)
        if last is not None:
            if '(' not in last.group(1):
                return True
            else:
                return False

    def last_dialect(self, line):
        search = re.search(self.search_last, line)
        if search is not None:
            return search.group(1)

    def load(self):
        n = 0
        self.load_original()
        for line in self.original_dialect:
            print 'Line: %d' % n
            if self.no_brackets(line):
                if n not in self.lines:
                    self.lines[n] = line
                    if line[-1] != '\n':
                        line += '\n'
                    self.f4.write(line)
                    print 'Written %s' % line
            else:
                last_dialect = self.last_dialect(line)
                decision = self.disambiguate(n, line)
                line = line.replace(last_dialect, decision)
                if n not in self.lines:
                    self.lines[n] = line
                    if line[-1] != '\n':
                        line += '\n'
                    self.f4.write(line)
                    print 'Written %s' % line
            n += 1

    def load_original(self):
        for line in self.f1:
            self.original_dialect.append(line)

    def load_mandarin(self):
        for line in self.f2:
            self.lines_mandarin.append(line)

    def load_rhymes(self):
        for line in self.f3:
            self.lines_rhymes.append(line)

    def last_mandarin(self, n, line):
        self.load_mandarin()
        result = ''
        if not self.no_brackets(line):
            last = re.search(self.search_last, self.lines_mandarin[n])
            if last is not None:
                result = last.group(1)
        return result

    def from_rhymes(self, n, line):
        self.load_rhymes()
        result_rhymes = []
        result_nums = []
        for l in self.lines_rhymes:
            nums = re.search(self.search_nums, l)
            if nums is not None:
                if str(n+1) == nums.group(1) or str(n+1) == nums.group(2):
                    rhymes = re.search(self.search_rhymes, l)
                    if rhymes is not None:
                        result = (rhymes.group(6), rhymes.group(7))
                        result_rhymes.append(result)
                    cur_nums = re.search(self.search_nums, l)
                    if cur_nums is not None:
                        result_cur_num = (int(cur_nums.group(1))-1, int(cur_nums.group(2))-1)
                        result_nums.append(result_cur_num)
        return result_rhymes, result_nums

    def disambiguate(self, n, line):
        result = ''
        mandarin = self.last_mandarin(n, line)
        rhymes = self.from_rhymes(n, line)[0]
        last_dialect = self.last_dialect(line)
        print '\nCurrent transcriptions: %s' % last_dialect
        result += last_dialect + ' '
        if mandarin != '':
            print 'Mandarin transcription is: %s' % mandarin
            result += mandarin + ' '
        if len(rhymes) > 0:
            print 'Mandarin rhymes:'
            for rhyme in rhymes:
                for r in rhyme:
                    print r,
                    result += r + ' '
                print '\n'
            print 'Probable rhyme with current character:'
            cur_nums = self.from_rhymes(n, line)[1]
            for num in cur_nums:
                first_char = re.search(self.search_last, self.original_dialect[int(num[0])])
                second_char = re.search(self.search_last, self.original_dialect[int(num[1])])
                if first_char is not None and second_char is not None:
                    res_orig = first_char.group(1) + second_char.group(1)
                    print res_orig

        if result in self.decisions:
            decision = self.decisions[result]
            print 'Chosen from before: %s' % decision
            print '\n'
        else:
            decision = raw_input('Your decision: ')
            self.decisions[result] = decision
            print '\n'
        return decision.decode('utf-8')

d = Disambiguator()
d.load()