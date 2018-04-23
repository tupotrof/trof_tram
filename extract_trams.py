#!/usr/bin/env python3
import sys
import io
import re
import urllib
from urllib.error import URLError
from urllib.request import urlopen
from tram.routes import extract_stops

LINK = "http://online.ettu.ru/station/"
STOPS = "routes/all_stops.kxt"

class RouteExtractor:
    def __init__(self, num):
        stops = []
        filename = "routes/number_routes/" + num + ".kxt"
        with io.open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                stops.append(line.split('|')[0])
        self.tram_d = dict()
        print(stops)
        for s in stops:
            trams = []
            try:
                page = urllib.request.urlopen(LINK + s).read().decode('utf-8', errors='ignore')
            except urllib.error.URLError:
                break
            # print(page)
            # re_list = re.findall('<div>\s+<div style="width: .*?</div>\s+</div>', page)
            re_list = re.findall('<div>\s+<div style="width: .*?<b>(.*?)</b>.*?'
                                 '</div>\s+<div style="width: .*?:right;">(.*)\sмин.*?'
                                 '</div>\s+<div style="width: .*?:right;">(.*)\sм.*?</div>\s+', page)
            # print(re_list)
            for line in re_list:
                if line[0] == num:
                    trams.append(line)
            # print(trams)
            self.tram_d[s] = trams
        print(self.tram_d)


def main():
    r = RouteExtractor('26')


if __name__ == '__main__':
    main()
