#!/usr/bin/env python3
import sys
import getopt
import io
import extract_stops

OUTPUT = "../resources/all_stops.kxt"


def distance(a, b):
    """
        Расстояние Левенштейна для названий остановок
    """
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1)  # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1, n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+3, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def main(argv):
    inputfile = ''
    outputfile = ''
    rev = True
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

    stops = extract_stops.get_stops(OUTPUT)
    data = []
    with io.open(inputfile, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.lower().rstrip('\n')
            if line == '[reverse]':  # типа чтобы остановки не переставлять
                rev = False
                continue
            s = dict.get(stops[1], line)
            if s is None:  # не нашли остановку, ищем самую похожую
                best_siml = 1000000
                best_str = ''
                for stop in stops[1].keys():
                    seq = distance(line, stop)
                    if seq < best_siml:
                        best_siml = seq
                        best_str = stop
                print('<!> Item "', line, '" detected as "', best_str, '" <!>', sep='')
                s = dict.get(stops[1], best_str)
                if s is None:
                    print('Not found: ', line)  # все равно не нашли - значит попа
            data.append(s)
            # print(s)
    f.close()
    if rev:
        data.reverse()
    # print()
    prev_stops = []
    route = []
    number_route = []
    started = False  # TODO: здесь дикий костыль, надо приручить
    for stop_name in data:
        if not started or len(stop_name) == 1:  # конечная
            route.append([stop_name[0]])
            prev_stops.append(stop_name[0][1][0])
            started = True
        else:
            all_pos_sos = []  # все остановки из которых можно попасть в предыдущюю
            for stop in stop_name:
                if len(stop[1]) > 1:
                    for kok in stop[1][1]:
                        if kok in prev_stops:
                            all_pos_sos.append(stop)
                            prev_stops.append(stop[1][0])
            if all_pos_sos:
                route.append(all_pos_sos)
            else:  # если в остановку не одна не ведет, чтото пошло не так
                print("\nErr\nNot connected: ", stop_name, '\n\n Tb: ', prev_stops, '\n\n', route)
                return None
        if len(prev_stops) > 11:  # большая борода, хз как побрить
            prev_stops.pop(0)
    # print(\n, route)
    number_route.append(route[0][0][0])  # начинаем собирать маршрут
    for i in range(1, len(route) - 1):
        # print(route[i], end=' ')
        if len(route[i]) > 1:  # опа, у нас неоднозначность, ну терь мы знаем ОТКУДА мы приехали
            dis = False
            for k in range(i + 1, len(route) - 1):
                next_stop = route[k][0][1][0]
                for r in route[i]:
                    if len(r[1]) > 2 and next_stop == r[1][2]:  # ура нашли
                        # print('\n', ' => ', r)
                        number_route.append(r[0])
                        dis = True
                if dis:
                    break
        else:
            # print('OK')
            number_route.append(route[i][0][0])
    number_route.append(route[len(route) - 1][0][0])  # цепляем конечную
    number_route.reverse()
    print('\nRoute:', number_route)
    # print()
    with io.open(outputfile, 'w', encoding='utf-8') as f:
        for num in number_route:
            f.write(num + "|" + stops[0][num][0] + "\n")
            # print(stops[0][num])


if __name__ == '__main__':
    main(sys.argv[1:])
