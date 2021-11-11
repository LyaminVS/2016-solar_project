# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet


def back_to_str(num):
    e = 0
    while num >= 10:
        num *= 0.1
        e += 1
    num = round(num, 3)
    return str(num) + ("E" + str(e)) * int(e > 0)


def float_float(num):
    if "E" in num:
        return float(num.split("E")[0]) * 10 ** float(num.split("E")[1])
    else:
        return float(num)


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == "planet":
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """
    star.Star, star.R, star.color, star.m, star.x, star.y, star.Vx, star.Vy = line.split()
    list_numbers = [star.R, star.m, star.x, star.y, star.Vx, star.Vy]
    star.R, star.m, star.x, star.y, star.Vx, star.Vy = list(map(float_float, list_numbers))


def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    planet.Planet, planet.R, planet.color, planet.m, planet.x, planet.y, planet.Vx, planet.Vy = line.split()
    list_numbers = [planet.R, planet.m, planet.x, planet.y, planet.Vx, planet.Vy]
    planet.R, planet.m, planet.x, planet.y, planet.Vx, planet.Vy = list(map(float_float, list_numbers))


def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w+') as out_file:
        for obj in space_objects:
            out_file.write("%s %s %s %s %s %s %s %s\n" % (obj.type, back_to_str(obj.R), obj.color, back_to_str(obj.m),
                                                          back_to_str(obj.x), back_to_str(obj.y), back_to_str(obj.Vx),
                                                          back_to_str(obj.Vy)))


if __name__ == "__main__":
    print("This module is not for direct call!")
