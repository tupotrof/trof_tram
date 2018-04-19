#!/usr/bin/env python3

from tram.routes import extract_all_stops as e


class Routes:
    def __init__(self):
        self.stops = e.get_stops()

    def get_route(self, num):
        stops_names = []
        with open("R_" + num) as f:
            for line in f:
                stops_names.append(self.stops[line[:-1]])
        return stops_names


def main():
    r = Routes()
    print(r.get_route("01"))


if __name__ == '__main__':
    main()
