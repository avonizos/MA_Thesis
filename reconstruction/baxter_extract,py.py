# -*- coding: utf-8 -*-

import codecs
import re

f1 = codecs.open('../txt/shijing_original/characters_trad.txt', 'r', 'utf-8')
f2 = codecs.open('../csv/baxter.csv', 'r', 'utf-8')
chars = []
text = []

def load_chars():
    for line in f1:
        char = line[-4]
        chars.append(char)

for line in f2:
    text.append(line)

load_chars()
for char in chars:
    flag = 0
    for line in text:
        #print char, line
        if char in line:
            bs = re.search(u'(.*?)\t(.*?)$', line)
            if bs is not None:
                print char, bs.group(2)
                flag = 1
                break
    if flag == 0:
        print char, u'-'
