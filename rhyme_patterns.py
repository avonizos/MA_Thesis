# -*- coding: utf-8 -*-

import codecs
import re

class Patterns():
    f = codecs.open('csv/rhymes/rhymes_cantonese_ipa.csv', 'r', 'utf-8')
    search_rhymes = re.compile(u'(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)')
    rhymings = {}
    crossed = 0
    encircling = 0
    paired = 0
    noname = 0
    amount = 2444

    def count_rhymes(self, line):
        parse = re.search(self.search_rhymes, line)
        if parse is not None:
            poem = parse.group(2)
            rhyming = parse.group(9)
            if poem not in self.rhymings:
                self.rhymings[poem] = {}
            else:
                if rhyming not in self.rhymings[poem]:
                    self.rhymings[poem][rhyming] = 1
                else:
                    self.rhymings[poem][rhyming] += 1

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

p = Patterns()
p.execute()
p.results()