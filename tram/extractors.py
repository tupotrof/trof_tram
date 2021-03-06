#!/usr/bin/env python3
import sys
import time
import io
import re
import urllib
import http.client
from urllib.error import URLError
from urllib.request import urlopen
from .routes import extract_stops

LINK = "online.ettu.ru"
STOPS = "resources/all_stops.kxt"

RE = re.compile('<div>\s+<div style="width: .*?<b>(.*?)</b>.*?'
                '</div>\s+<div style="width: .*?:right;">(.*)\sмин.*?'
                '</div>\s+<div style="width: .*?:right;">(.*)\sм.*?</div>\s+')


class StopExtractor:
    def __init__(self, stop, upd=False):
        self.stop_number = stop
        self.closest_trams = []
        if upd:
            self.update()

    def update(self):
        try:
            conn = http.client.HTTPConnection(LINK)
            conn.request("GET", "/station/" + self.stop_number)
            r1 = conn.getresponse()
            page = r1.read().decode('utf-8', errors='ignore')
        except urllib.error.URLError:
            return
        self.closest_trams = []
        re_list = re.findall(RE, page)
        for line in re_list:
            self.closest_trams.append(line)

    def get_results(self):
        return self.closest_trams

    def __str__(self):
        return str(self.closest_trams)


class RouteExtractor:
    def __init__(self, num, upd=False):
        self.route_number = num
        self.stops = []
        self.filename = "tram/resources/number_routes/" + num + ".kxt"
        with io.open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                self.stops.append(line.split('|')[0])
        self.tram_d = dict()
        if upd:
            self.update()
        # print(self.tram_d)

    def update(self):
        self.tram_d = dict()
        for s in self.stops:
            trams = []
            # print('Processing:', s)
            try:
                conn = http.client.HTTPConnection(LINK)
                conn.request("GET", "/station/" + s)
                r1 = conn.getresponse()
                page = r1.read().decode('utf-8', errors='ignore')
            except urllib.error.URLError:
                # print("Network error")
                return False
            # print(page)
            re_list = re.findall(RE, page)
            # print(re_list)
            for line in re_list:
                if line[0] == self.route_number:
                    trams.append(line)
            # print(trams)
            self.tram_d[s] = trams
        return True

    def take_from_total(self, total):
        if not isinstance(total, TotalExtractor):
            return False
        for s in self.stops:
            trams = []
            for line in total.all_trams[s]:
                if line[0] == self.route_number:
                    trams.append(line)
            self.tram_d[s] = trams
        return True

    def get_next_stop(self, stop):
        i = self.stops.index(stop)
        if i == len(self.stops) - 1:
            return self.stops[0]
        else:
            return self.stops[i + 1]

    def __str__(self, mode='numbers'):
        if mode == 'numbers':
            return str(self.stops)
        elif mode == 'stops':
            pass
        elif mode == 'info':
            pass
        else:
            return None


class TotalExtractor:
    def __init__(self, upd=False):
        self.all_stops_numbers = extract_stops.get_stops(STOPS)[0].keys()
        self.all_trams = dict()
        if upd:
            self.update()

    def update(self):
        num = 0
        for stop in self.all_stops_numbers:
            trams = []
            # print('Processing:', stop, end="... ")
            try:
                conn = http.client.HTTPConnection(LINK)
                conn.request("GET", "/station/" + stop)
                r1 = conn.getresponse()
                page = r1.read().decode('utf-8', errors='ignore')
            except urllib.error.URLError:
                print("Network error")
                continue
            re_list = re.findall(RE, page)
            # print(re_list)
            for line in re_list:
                trams.append(line)
            # print(trams)
            self.all_trams[stop] = trams
            # print("OK")

    def __str__(self):
        return str(self.all_trams)


def main():
    print(TotalExtractor())


if __name__ == '__main__':
    main()






















