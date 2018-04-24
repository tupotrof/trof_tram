from tram import extractors as ext


def search(stg):
    if isinstance(stg, ext.RouteExtractor):
        stop_pool = stg.tram_d
        prev = stop_pool[stg.stops[-2]]
        result = dict()
        print(stg.route_number, end=" : ")
        for stop in stop_pool:
            trams = []
            for i in prev:
                for j in stop_pool[stop]:
                    trams.append(int(j[2]) - int(i[2]))
            max_time = 100000
            print(trams, end="; ")
            for f in trams:
                if max_time > f > 0:
                    max_time = f
            if max_time < 100000:
                result[stop] = max_time
            else:
                result[stop] = None
            prev = stop_pool[stop]
        print()
        return result
    else:
        return None


def main():
    all_routes = ['2', '18', '19', '26']
    all_deltas = dict()
    extractors = []
    for route in all_routes:
        extractors.append(ext.RouteExtractor(route))
    for extractor in extractors:
        result = search(extractor)
        for stop in result:
            if result[stop]:
                next_stop = extractor.get_next_stop(stop)
                # kok = (int(stop) * 1000000) + int(next_stop)
                kok = (stop, next_stop)
                if not all_deltas.get(kok):
                    all_deltas[kok] = []
                all_deltas[kok].append(result[stop])
    print(all_deltas)



if __name__ == '__main__':
    main()
