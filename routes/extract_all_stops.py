#!/usr/bin/env python3
import urllib
from urllib.error import URLError, HTTPError
from urllib.parse import quote
import io
import re
from urllib.request import urlopen

LINK = "http://online.ettu.ru"
OUTPUT = "all_stops_raw.kxt"

stops_request = re.compile('<a href="/station/.*?</a>')
stop_numbers = dict()


def get_content_main():
    try:
        page = urllib.request.urlopen(LINK)
    except urllib.error.URLError:
        print("KOK")  # TODO: придумать ошибку
        return None
    return page.read().decode('utf-8', errors='ignore')


def get_letter_links(page):
    links = set()
    re_list = re.findall('a class="letter-link".*?</a>', page)
    for l in re_list:
        links.add(l[28:-7])  # TODO: сделать код не прибитый гвоздями к полу
    return links


def get_content(link):
    try:
        page = urllib.request.urlopen(LINK + link)
    except urllib.error.URLError:
        print("KOK")  # TODO: придумать ошибку
        return None
    return page.read().decode('utf-8', errors='ignore')


def extract_stops(page):
    begin = page.find('<h3>Трамваи</h3>')
    end = page.find('<h3>Троллейбусы</h3>', begin)
    if begin < 0:
        return None
    if end < 0:
        re_list = re.findall(stops_request, page)
    else:
        re_list = re.findall(stops_request, page[begin:end])
    for stop in re_list:
        if str.find(stop, '/station/96') != -1:
            stop_numbers[stop[18:24]] = str.lower(stop[26:-4])
        else:
            stop_numbers[stop[18:22]] = str.lower(stop[24:-4])


def main():
    main_page = get_content_main()
    letter_links = get_letter_links(main_page)
    for letter in letter_links:
        page = get_content(letter)
        extract_stops(page)
    with io.open(OUTPUT, 'w', encoding="utf-8") as f:
        for stop in stop_numbers:
            f.write(stop + '|' + stop_numbers[stop] + "\n")
    f.close()


if __name__ == '__main__':
    main()
