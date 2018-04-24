#!/usr/bin/env python3
import sys
import getopt
import io
from tram import extractors as ext
from tram import delta_searcher as d


def main():
    all_routes = ['1', '2', '3', '4', '5', '5A', '6', '7', '8', '9', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                  '21', '22', '23', '24', '25', '26', '27', '32', '33', '34']
    total = ext.TotalExtractor(upd=True)
    all_deltas = dict()
    extractors = []
    for route in all_routes:
        extractors.append(ext.RouteExtractor(route))
    for extractor in extractors:
        extractor.take_from_total(total)
        result = d.search(extractor)
        for stop in result:
            if result[stop]:
                next_stop = extractor.get_next_stop(stop)
                # kok = (int(stop) * 1000000) + int(next_stop)
                kok = (stop, next_stop)
                if not all_deltas.get(kok):
                    all_deltas[kok] = []
                all_deltas[kok].append(result[stop])
    print()
    print(all_deltas)


if __name__ == '__main__':
    main()
