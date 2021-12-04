# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *


class Params:
    def __init__(self):
        self.physical_time = 0
        """Физическое время от начала расчёта.
            Тип: float"""

        self.displayed_time = None
        """Отображаемое на экране время.
            Тип: переменная tkinter"""

        self.time_step = None
        """Шаг по времени при моделировании.
            Тип: float"""

        self.time_speed = None
        """частота расчёта изменений в симуляции"""

        self.space = None
        """Холст для рисования"""

        self.start_button = None
        """кнопка запуска / остановки симуляции"""

        self.perform_execution = False
        """Флаг цикличности выполнения расчёта"""

        self.space_objects = []
        """Список космических объектов."""

        self.scale_factor = None
        """Масштабирование экранных координат по отношению к физическим.
        Тип: float
        Мера: количество пикселей на один метр."""


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    recalculate_space_objects_positions(params.space_objects, float(params.time_step.get()))
    for body in params.space_objects:
        update_object_position(params.space, body, params.scale_factor)
    params.physical_time += params.time_step.get()
    params.displayed_time.set("%.1f" % params.physical_time + " seconds gone")

    if params.perform_execution:
        params.space.after(101 - int(params.time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    params.perform_execution = True
    params.start_button['text'] = "Pause"
    params.start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    params.perform_execution = False
    params.start_button['text'] = "Start"
    params.start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    params.perform_execution = False
    for obj in params.space_objects:
        params.space.delete(obj.image)  # удаление старых изображений планет

    # считывание и обработка данных из файла
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    if in_filename:
        params.space_objects = read_space_objects_data_from_file(in_filename)
        max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in params.space_objects])
        params.scale_factor = calculate_scale_factor(max_distance)

        # изображение объектов
        for obj in params.space_objects:
            if obj.type == 'star':

                create_star_image(params.space, obj, params.scale_factor)
            elif obj.type == 'planet':
                create_planet_image(params.space, obj, params.scale_factor)
            else:
                raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    if out_filename:
        write_space_objects_data_to_file(out_filename, params.space_objects)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    print('Modelling started!')
    params.physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    params.space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    params.space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    params.start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    params.start_button.pack(side=tkinter.LEFT)

    params.time_step = tkinter.DoubleVar()
    params.time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=params.time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    params.time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=params.time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    params.displayed_time = tkinter.StringVar()
    params.displayed_time.set(str(params.physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=params.displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')


if __name__ == "__main__":
    params = Params()
    main()
