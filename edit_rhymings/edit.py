# -*- coding: utf-8 -*-

import codecs
import re

class Editor():
    f = codecs.open('cantonese.txt', 'r', 'utf-8')
    search_all = re.compile(u'(.*?)\t(.*?)')
    search_nums = re.compile(u'([0-9]+)-([0-9]+)')

    def edit(self, line):
        res = ''
        nums = re.search(self.search_nums, line)
        if nums is not None:
            num1 = nums.group(1)
            num2 = nums.group(2)
            minus = int(num2) - int(num1)
            if minus == 1:
                res = u'paired\t' + num1 + '-' + num2
            if minus == 2:
                res = u'crossed\t' + num1 + '-' + num2
            if minus == 3:
                res = u'encircling\t' + num1 + '-' + num2
            if minus > 3:
                res = u'-\t' + num1 + '-' + num2
        print res

    def load(self):
        for line in self.f:
            self.edit(line)

ed = Editor()
ed.load()
