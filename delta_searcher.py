from tram import extractors as ext


def main():
    stg = ext.RouteExtractor('2')
    kxt = stg.tram_d

    prev = kxt[stg.stops[-2]]

    for stop in kxt:
        print(stop, end=": ")
        for i in prev:
            for j in kxt[stop]:
                print(int(j[2]) - int(i[2]), end=", ")
        prev = kxt[stop]
        print()


if __name__ == '__main__':
    main()
