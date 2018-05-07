# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for obtaining the Fuzhou dialect's IPA transcriptions
# from the online dictionary for the Shijing text

import codecs
import urllib
import urllib2
import re
from time import sleep

class Converter:
    def __init__(self):
        self.hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        with codecs.open('../txt/shijing_original/characters.txt', 'r', 'utf-8') as f:
            self.source = f.readlines()
        self.out = codecs.open('../txt/shijing_original/fuzhou.txt', 'w', 'utf-8')
        self.text = ''

    def read_source(self):
        counter = 0
        sleep_c = 0
        for line in self.source:
            if sleep_c % 100 == 0:
                sleep(20)
            print counter
            print line
            line = line.replace(u'、', u'')
            line = line.replace(u'，', u'')
            line = line.replace(u'。', u'')
            for character in line.strip('\n\r'):
                self.make_request(character)
            self.out.write('\n')
            counter += 1
            sleep_c += 1

    def make_request(self, line):
        result = '-'
        result_ipa = '-'
        query_text = line
        query_text = urllib.quote(query_text.encode("utf-8"))
        link = "http://120.25.72.164/fzhDictionary/index.php?s=/Home/Dictionary/getWordInfo&word=" +\
               query_text
        print link

        req = urllib2.Request(link, headers=self.hdr)
        try:
            response = urllib2.urlopen(req)
        except:
            sleep(300)
            response = urllib2.urlopen(req)
        raw_data = response.read()
        response.close()

        ipa_pronounce = re.findall(u'f_gjybstr":"(.*?)"', raw_data)
        ipa_tone = re.findall(u'f_gjybyd":"(.*?)"', raw_data)

        if ipa_pronounce is not None and ipa_tone is not None:
            if len(ipa_pronounce) > 1:
                result_ipa = ipa_pronounce[0].decode("unicode_escape") + ipa_tone[0]
                result_ipa += '(' + ipa_pronounce[1].decode("unicode_escape") + ipa_tone[1]
                if len(ipa_pronounce) > 2:
                    i = 2
                    for res in ipa_pronounce[2:]:
                        result_ipa += ', ' + res.decode("unicode_escape") + ipa_tone[i]
                        i += 1
                result_ipa += ')'
            if len(ipa_pronounce) == 1:
                if ipa_pronounce is not None and len(ipa_pronounce) != 0:
                    result_ipa = ipa_pronounce[0].decode("unicode_escape") + ipa_tone[0]
        print result_ipa
        self.out.write(result_ipa + ' ')

c = Converter()
c.read_source()