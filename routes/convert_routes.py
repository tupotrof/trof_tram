#!/usr/bin/env python3
import sys
import getopt
import io

OUTPUT = "all_stops.kxt"


def get_stops(file=OUTPUT):
    num_dict = dict()
    nam_dict = dict()
    with io.open(file, 'r', encoding='utf=8') as f:
        for line in f:
            line = line.split('|')
            line[1] = line[1].split(' (', maxsplit=1)
            line[1][-1] = line[1][-1].strip(')\n')

            if line[1].__len__() > 1:
                if line[1][1].find('с ') != -1 or line[1][1].find('со ') != -1:
                    from_to = line[1][1].replace('со ', '').replace('с ', '').split(' на ')
                    line[1] = [line[1][0], from_to[1], from_to[0]]
                else:
                    line[1] = [line[1][0], line[1][1].replace('на ', '')]
                line[1][1] = line[1][1].split(', ')

            num_dict[line[0]] = line[1]
            if line[1][0] not in nam_dict:
                nam_dict[line[1][0]] = list()
            nam_dict[line[1][0]].append(line)
    return [num_dict, nam_dict]


def main(argv):
    inputfile = ''
    outputfile = ''
    rev = False
    try:
        opts, args = getopt.getopt(argv, "hi:o:r")
    except getopt.GetoptError:
        print('convert_routes.py <inputfile> <outputfile> [-r]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('convert_routes.py <inputfile> <outputfile> [-r]')
            sys.exit()
        elif opt == "-i":
            inputfile = arg
        elif opt == "-o":
            outputfile = arg
        elif opt == '-r':
            rev = True

    if rev:
        pass

    else:
        stops = get_stops()
        data = []
        with io.open(inputfile, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.lower().rstrip('\n')
                s = dict.get(stops[1], line)
                if s is None:
                    s = ['0000', ['NOT FOUND']]
                    print('Not found: ', line)
                data.append(s)
                # print(s)
        f.close()
        data.reverse()
        # print()
        prev_stops = []
        route = []
        number_route = []
        started = False
        for stop_name in data:
            if not started or len(stop_name) == 1:
                route.append([stop_name[0]])
                prev_stops.append(stop_name[0][1][0])
                started = True
            else:
                all_pos_sos = []
                for stop in stop_name:
                    if len(stop[1]) > 1:
                        for kok in stop[1][1]:
                            if kok in prev_stops:
                                all_pos_sos.append(stop)
                                prev_stops.append(stop[1][0])
                if all_pos_sos:
                    route.append(all_pos_sos)
                else:
                    print("\nErr\nNot connected: ", stop_name, '\n\n Tb: ', prev_stops, '\n\n', route)
                    return None
            if len(prev_stops) > 11:
                prev_stops.pop(0)
        # print(\n, route)
        number_route.append(route[0][0][0])
        for i in range(1, len(route) - 1):
            print(route[i], end=' ')
            if len(route[i]) > 1:
                dis = False
                for k in range(i + 1, len(route) - 1):
                    next_stop = route[k][0][1][0]
                    for r in route[i]:
                        if len(r[1]) > 2 and next_stop == r[1][2]:
                            print('\n', ' => ', r)
                            number_route.append(r[0])
                            dis = True
                    if dis:
                        break
            else:
                print('OK')
                number_route.append(route[i][0][0])
        number_route.append(route[len(route) - 1][0][0])
        print('\nRoute:', number_route)
        # print()
        with io.open(outputfile, 'w', encoding='utf-8') as f:
            for num in number_route:
                f.write(num + "\n")
                # print(stops[0][num])


if __name__ == '__main__':
    main(sys.argv[1:])
