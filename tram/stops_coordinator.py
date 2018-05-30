#!/usr/bin/env python3
from tram.extractors import *

LINK = "online.ettu.ru"

RE = re.compile('<img src="http://maps.google.com.*?alt="Карта" />')
RE2 = re.compile('&amp;markers=size:mid\|(.*?),(.*?)&amp;')

all_stops = extract_stops.get_stops("resources/all_stops.kxt")
all_routes = ['1',  '2',  '3',  '4', '5', '5A', '6', '7', '8', '9', '10',
              '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
              '21', '22', '23', '24', '25', '26', '27', '32', '33', '34']

all_data = dict()

conn = http.client.HTTPConnection(LINK)

for stop in all_stops[0]:
    conn.request("GET", "/station/" + stop)
    r1 = conn.getresponse()
    page = r1.read().decode('utf-8', errors='ignore')
    result = re.findall(RE2, page)
    print(stop, result)
    if len(result) > 0:
        all_data[stop] = result[0]
    else:
        all_data[stop] = None
