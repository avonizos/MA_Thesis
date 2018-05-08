# -*- coding: utf-8 -*-

# Author: Olga Sozinova
# Python program for obtaining the Taiwanese Hakka, Sixian dialect's IPA transcriptions
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
        with codecs.open('../txt/shijing_original/mandarin/mandarin_notones.txt', 'r', 'utf-8') as f1:
            self.notones = f1.readlines()
        self.out = codecs.open('../txt/shijing_original/dialects/hakka.txt', 'w', 'utf-8')
        self.text = ''

    def sup_convert(s, line):
        sups = {
            u'\u00B9': u'1',
            u'\u00B2': u'2',
            u'\u00B3': u'3',
            u'\u2074': u'4',
            u'\u2075': u'5'
        }
        for char in sups:
            if char.encode('utf-8') in line:
                line = line.replace(char.encode('utf-8'), sups[char].encode('utf-8'))
        return line

    def read_source(self):
        notones = []
        counter = 0
        sleep_c = 0
        for i in range(len(self.source)):
            if sleep_c % 100 == 0:
                sleep(20)
            print counter
            print self.source[i]
            self.source[i] = self.source[i].replace(u'、', u'')
            self.source[i] = self.source[i].replace(u'，', u'')
            self.source[i] = self.source[i].replace(u'。', u'')

            line = self.notones[i]
            notones = line.split()

            for j in range(len(self.source[i].strip('\n\r'))):
                if notones is not None:
                    self.make_request(self.source[i][j], notones[j])
            self.out.write('\n')
            counter += 1
            sleep_c += 1

    def make_request(self, line, notone):
        result = '-'
        query_text = line
        query_text_encode = urllib.quote(query_text.encode("utf-8"))

        link = "https://www.moedict.tw/h/" + \
               query_text_encode + \
               ".json"

        print link

        req = urllib2.Request(link, headers=self.hdr)
        try:
            response = urllib2.urlopen(req)
            raw_data = response.read()
            response.close()
            find_si = re.findall(u'p\":\"(.*?) ', raw_data)
            if len(find_si) > 0:
                if len(find_si) == 1:
                    result = self.sup_convert(find_si[0][3:])
                else:
                    if len(find_si) == 2:
                        result = self.sup_convert(find_si[0][3:])
                        result += '(' + self.sup_convert(find_si[1][3:]) + ')'
                    else:
                        result = self.sup_convert(find_si[0][3:])
                        result += '('
                        for el in find_si[1:]:
                            result += self.sup_convert(el[3:]) + ','
                        result += ')'
                        result = result.replace(',)', ')')

        except urllib2.HTTPError as e:
            if e.code == 404:
                link = "https://www.moedict.tw/lookup/pinyin/h/HanYu/" + \
                       notone + \
                       ".json"
                print link
                req = urllib2.Request(link, headers=self.hdr)
                try:
                    new_query = ''
                    response = urllib2.urlopen(req)
                    raw_data = response.read()
                    response.close()
                    raw_data = raw_data.replace('"', '')
                    raw_data = raw_data.replace('[', '')
                    raw_data = raw_data.replace(']', '')
                    possible_chars = raw_data.split(',')
                    for char in possible_chars:
                        if query_text.encode("utf-8") in char:
                            new_query = char
                            break
                    if new_query != '' and len(new_query) == 6:
                        flag = 1
                        if query_text.encode("utf-8") == new_query[3:6]:
                            flag = 2
                        link = "https://www.moedict.tw/h/" + \
                               new_query + \
                               ".json"
                        req = urllib2.Request(link, headers=self.hdr)
                        response = urllib2.urlopen(req)
                        raw_data = response.read()
                        response.close()
                        find_si = re.findall(u'p\":\"(.*?) ', raw_data)

                        if len(find_si) > 0:
                            if len(find_si) == 1:
                                raw_result = self.sup_convert(find_si[0][3:])
                                find_words = re.search(u'^(.*?[0-9]+)(.*?[0-9]+)$', raw_result)
                                if find_words is not None:
                                    result = find_words.group(flag)
                            else:
                                if len(find_si) == 2:
                                    raw_result = self.sup_convert(find_si[0][3:])
                                    find_words = re.search(u'^(.*?[0-9]+)(.*?[0-9]+)$', raw_result)
                                    if find_words is not None:
                                        result = find_words.group(flag)
                                    raw_result = self.sup_convert(find_si[1][3:])
                                    find_words = re.search(u'^(.*?[0-9]+)(.*?[0-9]+)$', raw_result)
                                    if find_words is not None:
                                        result += '(' + find_words.group(flag) + ')'
                                else:
                                    raw_result = self.sup_convert(find_si[0][3:])
                                    find_words = re.search(u'^(.*?[0-9]+)(.*?[0-9]+)$', raw_result)
                                    if find_words is not None:
                                        result = find_words.group(flag)
                                    result += '('
                                    for el in find_si[1:]:
                                        raw_result = self.sup_convert(el[3:])
                                        find_words = re.search(u'^(.*?[0-9]+)(.*?[0-9]+)$', raw_result)
                                        if find_words is not None:
                                            result += find_words.group(flag) + ','
                                    result += ')'
                                    result = result.replace(',)', ')')

                            for el in find_si:
                                new_el = self.sup_convert(el[3:])
                                find_words = re.search(u'^(.*?[0-9]+)(.*?[0-9]+)$', new_el)
                                if find_words is not None:
                                    result = find_words.group(flag)

                except urllib2.HTTPError as e:
                    if e.code == 404:
                        pass

        result = result.decode('utf-8')
        result = result.replace(u'⃞', u'')
        print result
        self.out.write(result + ' ')

c = Converter()
c.read_source()