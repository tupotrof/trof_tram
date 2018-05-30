#!/usr/bin/env python3
import urllib.request
import http.client
import sys
import getopt
import io
from tram.routes import convert_routes
from tram.extractors import *

LINK = "online.ettu.ru"

all_routes = ['1',  '2',  '3',  '4', '5', '5A', '6', '7', '8', '9', '10',
              '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
              '21', '22', '23', '24', '25', '26', '27', '32', '33', '34']


def stop_s(stop_input):

    all_stops = extract_stops.get_stops("tram/resources/all_stops.kxt")

    stop_detect = convert_routes.detect_stop(all_stops, stop_input)

    all_extractors = dict()

    for t in all_routes:
        all_extractors[t] = RouteExtractor(t)

    p = 1
    for i in stop_detect:
        print(str(p) + ": НА ост. ", end="")
        for o in i[1][1]:
            print(o.upper(), end="; ")
        if len(i[1]) > 2:
            print("ОТ ост. " + str(i[1][2]).upper(), end="")
        print()
        p += 1

    stop_number = stop_detect[int(input()) - 1][0]
    print(stop_number)

    se = StopExtractor(stop_number, True)
    t = se.get_results()
    print("РЯДОМ:")
    for tram in t:
        print("    " + tram[0] + ":  ~" + tram[1] + " мин.")

    stop_routes = []
    for t in all_routes:
        p = all_extractors[t].stops
        if stop_number in p:
            stop_routes.append(t)

    print(stop_routes)
    route_number = input()

    if route_number in stop_routes:
        ext = all_extractors[route_number]
        ext.update()
        print(ext.tram_d)
