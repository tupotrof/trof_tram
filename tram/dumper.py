#!/usr/bin/env python3

import sys
import os
import getopt
import io
import pickle
from tram import extractors as ext
from tram import delta_searcher as d
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

PATH_LENGTHS = 'resources/lengths.pickle'


def main():
    all_routes = ['1', '2', '3', '4', '5', '5A', '6', '7', '8', '9', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                  '21', '22', '23', '24', '25', '26', '27', '32', '33', '34']
    total = ext.TotalExtractor(upd=True)
    all_deltas = dict()
    with open(PATH_LENGTHS, 'rb') as f:
        all_data = pickle.load(f)
    extractors = []
    for route in all_routes:
        extractors.append(ext.RouteExtractor(route))
    for extractor in extractors:
        extractor.take_from_total(total)
        result = d.search(extractor)
        for stop in result:
            if result[stop]:
                next_stop = extractor.get_next_stop(stop)
                kok = (stop, next_stop)
                if not all_deltas.get(kok):
                    all_deltas[kok] = []
                all_deltas[kok].append(result[stop])

    for k in all_deltas:
        if not dict.get(all_data, k):
            all_data[k] = []
        all_data[k].extend(all_deltas[k])

    print(all_data)

    with open(PATH_LENGTHS, 'wb') as f:
        pickle.dump(all_data, f)


if __name__ == '__main__':
    main()
