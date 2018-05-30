#!/usr/bin/env python3
import io


def get_stops(file):
    """
        Позволяет извлечь информацию об остановках из файла
        TODO: починить импорты и вынести её в отдельный файл
    """
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