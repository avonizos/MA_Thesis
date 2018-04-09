# -*- coding: utf-8 -*-

import codecs
import re

class Patterns():
    f = codecs.open('csv/rhymes/rhymes_mandarin_ipa.csv', 'r', 'utf-8')
    search_rhymes = re.compile(u'(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)')
    rhymings = {}
    crossed = 0
    encircling = 0
    paired = 0
    noname = 0
    amount = 1961

    def count_rhymes(self, line):
        parse = re.search(self.search_rhymes, line)
        if parse is not None:
            book = parse.group(1)
            poem = parse.group(2)
            book_poem = book + ' ' + poem
            rhyming = parse.group(9)
            if book_poem not in self.rhymings:
                self.rhymings[book_poem] = {}
            if rhyming not in self.rhymings[book_poem]:
                self.rhymings[book_poem][rhyming] = 1
            else:
                self.rhymings[book_poem][rhyming] += 1

    def execute(self):
        for line in self.f:
            self.count_rhymes(line)

    def results(self):
        for poem in self.rhymings:
            for rhyming in self.rhymings[poem]:
                if rhyming == u'crossed':
                    self.crossed += self.rhymings[poem][rhyming]
                if rhyming == u'paired':
                    self.paired += self.rhymings[poem][rhyming]
                if rhyming == u'encircling':
                    self.encircling += self.rhymings[poem][rhyming]
                if rhyming == u'-':
                    self.noname += self.rhymings[poem][rhyming]
        print "Average crossed: %.2f" % (self.crossed/float(self.amount))
        print "Average paired: %.2f" % (self.paired/float(self.amount))
        print "Average encircling: %.2f" % (self.encircling/float(self.amount))
        print "Average -: %.2f" % (self.noname/float(self.amount))

        # sum = 0
        # for poem in self.rhymings:
        #     for rhyming in self.rhymings[poem]:
        #         print poem, rhyming, self.rhymings[poem][rhyming]
        #         sum += self.rhymings[poem][rhyming]
        # print sum

p = Patterns()
p.execute()
p.results()