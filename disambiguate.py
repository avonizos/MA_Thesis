# -*- coding: utf-8 -*-

import codecs
import re

class Disambiguator():
    f1 = codecs.open('txt/ipa ambiguous/hakka_ipa.txt', 'r', 'utf-8')
    f2 = codecs.open('txt/shijing_original/mandarin/mandarin_ipa.txt', 'r', 'utf-8')
    f3 = codecs.open('csv/rhymes/rhymes_mandarin_ipa.csv', 'r', 'utf-8')
    f4 = codecs.open('txt/ipa disambiguated/hakka_disambiguated.txt', 'w', 'utf-8')
    search_last = re.compile(u'([^ ]+)$')
    search_nums = re.compile(u'([0-9]+)-([0-9]+)')
    search_rhymes = re.compile(u'(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t')
    lines = {}
    lines_mandarin = []
    lines_rhymes = []
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
        for line in self.f1:
            print 'Number: %d' % n
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
        for l in self.lines_rhymes:
            nums = re.search(self.search_nums, l)
            if nums is not None:
                if str(n) == nums.group(1) or str(n) == nums.group(2):
                    rhymes = re.search(self.search_rhymes, l)
                    if rhymes is not None:
                        result = (rhymes.group(6), rhymes.group(7))
                        result_rhymes.append(result)
        return result_rhymes

    def disambiguate(self, n, line):
        result = ''
        mandarin = self.last_mandarin(n, line)
        rhymes = self.from_rhymes(n, line)
        last_dialect = self.last_dialect(line)
        print 'Current characters: %s' % last_dialect
        result += last_dialect + ' '
        if mandarin != '':
            print 'Mandarin character is: %s' % mandarin
            result += mandarin + ' '
        if len(rhymes) > 0:
            print 'Mandarin rhymes:'
            for rhyme in rhymes:
                for r in rhyme:
                    print r,
                    result += r + ' '
                print '\n'
        if result in self.decisions:
            decision = self.decisions[result]
            print 'Chosen from before: %s' % decision
            print '\n'
        else:
            decision = raw_input('Choose your decision: ')
            self.decisions[result] = decision
            print '\n'
        return decision.decode('utf-8')

    # def write_lines(self):
    #     for key in self.lines:
    #         self.f4.write(self.lines[key])

d = Disambiguator()
d.load()
# d.write_lines()