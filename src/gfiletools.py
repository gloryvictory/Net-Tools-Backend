#import logging
#import os


from sys import platform as _platform
import os
import sys
import logging

import cfg



def do_log_file(dir_out, file_log):
    for handler in logging.root.handlers[:]:  # Remove all handlers associated with the root logger object.
        logging.root.removeHandler(handler)

    # dir_out = get_output_directory()
    file_log = str(os.path.join(dir_out, file_log))  # from cfg.file

    if os.path.isfile(file_log):  # Если выходной LOG файл существует - удаляем его
        try:
            os.remove(file_log)
        except:
            str_err = "Процесс не может получить доступ к файлу, так как этот файл занят другим процессом: : " + file_log
            print(str_err)
    logging.basicConfig(filename=file_log, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
                        filemode='w')  #
    logging.info(file_log)
    return logging


def get_input_directory_from_cfg():
    directory_in = str(os.getcwd())
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        if os.path.isdir(cfg.folder_in_linux):
            print('Input directory from a config file: ' + cfg.folder_in_linux)
            return cfg.folder_in_linux
        else:
            print(
                'Input directories from config wrong: ' + cfg.folder_in_linux + ' Using current directory: ' + directory_in)
            return directory_in
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        if os.path.isdir(cfg.folder_in_win):
            print('Input directory from a config file: ' + cfg.folder_in_win)
            return cfg.folder_in_win
        else:
            print(
                'Input directories from config wrong: ' + cfg.folder_in_win + ' Using current directory: ' + directory_in)
            return directory_in
    return directory_in


def get_input_directory():
    # get from config
    directory_in = str(os.getcwd())
    # if only run the script (1 argument)
    if len(sys.argv) == 1:  # there is no arguments in command line
        return get_input_directory_from_cfg()

    if len(sys.argv) == 2:  # there is only one argument in command line
        directory_in = str(sys.argv[1:][0])
        if os.path.isdir(directory_in):
            return directory_in
        else:
            return get_input_directory_from_cfg()

    if len(sys.argv) > 2:  # there is only one argument in command line
        print("Arguments much more than 1! Please use only path as an argument. (Script.py /mnt/some_path) ")
        print(sys.argv, len(sys.argv))
        exit(1)
    return directory_in


def get_output_directory():
    dir_out = str(os.getcwd())
    # Linux platform
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        dir_out = cfg.folder_out_linux
        print('Output directory from config file: ' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    if _platform == "win32" or _platform == "win64":  # Windows or Windows 64-bit
        dir_out = cfg.folder_out_win
        print('Output directory from config file' + dir_out)
        if os.path.exists(dir_out) and os.path.isdir(dir_out):
            return dir_out
    else:
        print(
            'Output directories from config wrong: ' + cfg.folder_out_win + ' or ' + cfg.folder_out_linux + ' Using current directory: ' + dir_out)
    print('Using Output directory: ' + dir_out)
    return dir_out