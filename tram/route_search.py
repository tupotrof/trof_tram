#!/usr/bin/env python3
import urllib.request
import http.client
import sys
import getopt
import io
from tram.extractors import *

LINK = "online.ettu.ru"

all_routes = ['1',  '2',  '3',  '4', '5', '5A', '6', '7', '8', '9', '10',
              '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
              '21', '22', '23', '24', '25', '26', '27', '32', '33', '34']


def route_s(route):
    if route not in all_routes:
        return None

    ext = RouteExtractor(route, True)

    print(ext.tram_d)
