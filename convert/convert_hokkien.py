# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for obtaining the Taiwanese Hokkien dialect's IPA transcriptions
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
        with codecs.open('../txt/shijing_original/characters_trad.txt', 'r', 'utf-8') as f:
            self.source = f.readlines()
        self.out = codecs.open('../txt/shijing_original/hokkien_1.txt', 'w', 'utf-8')
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
        query_text = line
        query_text = urllib.quote(query_text.encode("utf-8"))

        link = "http://twblg.dict.edu.tw/holodict_new/result_page.jsp?n_no=0&curpage=1&sample=" +\
                query_text +\
                "&radiobutton=0&querytarget=1&limit=20&pagenum=1&rowcount=2"
        print link

        req = urllib2.Request(link, headers=self.hdr)
        try:
           response = urllib2.urlopen(req)
        except:
           sleep(300)
           response = urllib2.urlopen(req)
        raw_data = response.read()
        response.close()

        sound = re.findall(u'tlsound">[\r\n\t]*(.*)[\r\n\t]*</', raw_data)
        if sound is not None:
             if len(sound) > 1:
                 result = sound[0]
                 result += '(' + sound[1]
                 if len(sound) > 2:
                     for res in sound[2:]:
                         result += ', ' + res
                 result += ')'
             if len(sound) == 1:
                 if sound is not None and len(sound) != 0:
                     result = sound[0]

        print result

        result = result.decode('utf-8')
        self.out.write(result + ' ')

c = Converter()
c.read_source()