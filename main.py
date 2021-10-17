import os
import psutil
import sys
import time
import argparse


def create_parser():    # Функция парсинга аргументов командной строки
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--path')
    parse.add_argument('-int', '--interval', default='5')
    return parse

    # Функция поиска процессов #
    # Функцию взял с официальной документации psutil #


def find_procs_by_name(name):  # Функция поиска процесса
    # Список найденных процессов (для логов используется только первый)
    ls = []

    # Итерация по всем запущенным процессам и добавление их в список
    for p in psutil.process_iter(["name", "exe", "cmdline"]):
        if name == p.info['name'] or \
                p.info['exe'] and os.path.basename(p.info['exe']) == name or \
                p.info['cmdline'] and p.info['cmdline'][0] == name:
            ls.append(p)

    # Вернуть список
    return ls


def linux_logs(my_process, command_line_args):  # Функция для Linux

    # Cписок, который записывается в Log.txt
    log_list = []

    # Открытие файла log.txt для записи
    log = open("log.txt", "w")

    # Цикл пока запущен процесс
    while my_process:
        try:
            # Повторная запись процесса
            my_process = find_procs_by_name(command_line_args.path)[0]

            # Cбор логов
            logs = {"CPU Load": my_process.cpu_percent(),
                    "Resident Set Size": my_process.memory_info().rss,
                    "Virtual Memory Size": my_process.memory_info().vms,
                    "Num of Handles": my_process.num_fds()()}

            # Записать словарь в список
            log_list.append(logs)
            print("Log saved")

        # Если процесса больше не существует
        except IndexError:

            print("Process closed")

            # Записать в Лог файл получившийся список
            log.write(str(log_list))
            log.close()

            exit()

        # Заснуть на введенный интервал
        time.sleep(int(namespace.interval))


def windows_logs(my_process, command_line_args):  # Функция для Windows

    # Список, который записывается в LOG
    log_list = []

    # Открытие файла log.txt для записи
    log = open("log.txt", "w")

    # Цикл пока запущен процесс
    while my_process:
        try:
            # Повторная запись процесса
            my_process = find_procs_by_name(command_line_args.path)[0]

            # Cбор логов
            logs = {"CPU Load": my_process.cpu_percent(),
                    "Working set": my_process.memory_info().wset,
                    "Private bytes": my_process.memory_info().private,
                    "Num of Handles": my_process.num_handles()}

            # Записать словарь в список
            log_list.append(logs)
            print("Log saved")

        # Если процесса больше не существует
        except IndexError:
            print("Process closed")

            # Записать в Лог файл получившийся список
            log.write(str(log_list))
            log.close()

            exit()

        # Заснуть на введенный интервал
        time.sleep(int(command_line_args.interval))


def open_proc():

    # Создание пространства имен аргументов командной строки
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    # Проверка на корректность аргументов
    if namespace.interval.isnumeric() and namespace.path or namespace.path and namespace.interval == '5':

        # Открыть файл
        try:
            os.startfile(namespace.path)

        # Обработка исключения ФайлНеНайден
        except FileNotFoundError:
            print("File not found")
            exit()

        # Подождать секунду перед началом логов, не был уверен нужно ли, просто если открыть
        # какую нибудь игру из Steam, ее процесс мгновенно не появляется
        time.sleep(1)

        # Поиск процесса с дальнейшим логгированием
        try:
            # Записать в переменную первый найденный процесс
            process = find_procs_by_name(namespace.path)[0]

            # Если ОС UNIX
            if os.name == 'posix':
                linux_logs(process, namespace)

            # Если ОС Windows
            elif os.name == 'nt':
                windows_logs(process, namespace)

            # Если система не UNIX и не Windows
            else:
                print("Sorry, your operation system not supported")

        # Обработка исключения если процесс не найден
        except IndexError:
            print("Process not found")
            exit()

    # Если аргументы неверные
    else:
        print("Wrong arguments")


if __name__ == "__main__":
    open_proc()
