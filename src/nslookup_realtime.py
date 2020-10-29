# https://github.com/requests/requests-ntlm/issues/65
# !/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          : Viacheslav Zamaraev
#   email           : zamaraev@gmail.com
#   Script Name     : 01_get_table_from_sc_portal.py
#   Created         : 22th July 2020
#   Last Modified	: 22th July 2020
#   Version		    : 1.0
#   PIP             : pip install
#   RESULT          : csv file with columns: FILENAME;...LASTACCESS
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : get data to csv


from datetime import datetime
from time import strftime   # Load just the strftime Module from Time
import logging
import subprocess
import re
import csv
import os


import gfiletools
import cfg

try:
    import pandas as pd
except:
    print("we need pands. try: pip install pandas")




def do_nslookup_network(compname = ''):
    csv_dict = cfg.csv_out_dict

    str_fqdn = ''
    str_name_by_ip = ''

    # process = subprocess.Popen(["nslookup", "10.72.41.126"], stdout=subprocess.PIPE)
    process = subprocess.Popen(["nslookup", compname], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    str_output = str(output)
    len_output = len(str_output)
    #print(str(output))

    for key in csv_dict:
        csv_dict[key] = ''
        # csv_dict['DATA_SCRIPT_RUN'] = str(time.strftime("%Y-%m-%d"))

    csv_dict['COMPNAME'] = str(compname).upper()

    with open(cfg.file_csv, 'a', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, cfg.csv_out_dict.keys(), delimiter=cfg.csv_delimiter)
        if len_output:
            str_fqdn =''
            str_name_by_ip = ''
            list_output = str_output.split(":")
            len_list_output = len(list_output)
            if len_list_output > 2:
                #ищем контроллер домена
                str_temp = list_output[1].strip()
                str_temp = str_temp.split("Address")[0]
                match = re.search(r"[A-Za-z0-9_-]+\.tm\.novatek\.int", str_temp) # ^dc\d\d?-tm.tm.novatek.int
                if match:
                    dc = match.group()
                    csv_dict['DC'] = str(dc).upper()
                    #print(dc)
                else:
                    str_err = "DC - no comparisons found"
                    print_error(str_err, cfg.errors_print)
                    log_error(str_err, cfg.errors_log)

                # ищем IP address контроллера домена
                str_temp = list_output[2].strip()
                match = re.search(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", str_temp)
                if match:
                    dc_ip = match.group()
                    csv_dict['DC_IP'] = dc_ip
                    #print(dc_ip)
                else:
                    str_err = "dc_ip (IP address of Domain Controller) - no comparisons found"
                    print_error(str_err, cfg.errors_print)
                    log_error(str_err, cfg.errors_log)

                if len_list_output > 3:
                    # ищем имя компа
                    str_temp = list_output[3].strip()
                    match = re.search(r"[A-Za-z0-9_-]+\.tm\.novatek\.int", str_temp)
                    if match:
                        fqdn_name = match.group()

                        str_fqdn = str(fqdn_name).upper()
                        csv_dict['FQDN'] = str_fqdn

                        #print(compname)
                    else:
                        str_err = "FQDN - no comparisons found"
                        print_error(str_err, cfg.errors_print)
                        log_error(str_err, cfg.errors_log)
                else:
                # это ситуация, когда есть прямая зона, а обратной нет!!!
                    str_name_by_ip = 'Secondary Zone is absent OR Computer is down '
                    csv_dict['NAME_BY_IP'] = str_name_by_ip
                    csv_dict['LASTUPDATE'] = str(datetime.now())

                if len_list_output > 4:
                    # ищем IP address компа
                    str_temp = list_output[4].strip()
                    match = re.search(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", str_temp)
                    if match:
                        compname_ip = match.group()
                        csv_dict['FQDN_IP'] = str(compname_ip).upper()

                        str_name_by_ip = str(do_nslookup_by_ip_network(compname_ip)).upper()  # test '10.72.50.7'

                        csv_dict['NAME_BY_IP'] = str_name_by_ip
                        csv_dict['LASTUPDATE'] = str(datetime.now())
                        #print(compname_ip)
                    else:
                        str_err = "compname_ip - no comparisons found: "
                        print_error(str_err, cfg.errors_print)
                        log_error(str_err, cfg.errors_log)

                if str_fqdn in str_name_by_ip:
                    if 'down' in str_name_by_ip:
                        csv_dict['WARNING'] = 'DOWN'
                    else:
                        csv_dict['WARNING'] = 'OK'
                else:
                    if 'NON-EXISTENT' in str_name_by_ip:
                        csv_dict['WARNING'] = 'LOW'
                    else:
                        csv_dict['WARNING'] = 'HIGH'

                try:
                    #print(csv_dict['COMPNAME'])
                    csv_file_open.writerow(csv_dict)

                except Exception as e:
                    str_err = "Exception occurred " + str(e)
                    print_error(str_err, cfg.errors_print)
                    log_error(str_err, cfg.errors_log)
            else:
                # это ситуация, когда есть прямая зона, а обратной нет!!!


                str_err = 'Len list_output less than less 4 in text:' + str_output
                print_error(str_err, cfg.errors_print)
                log_error(str_err, cfg.errors_log)
        else:
            str_err = 'Len list_output less than 4 in text:' + str_output
            print_error(str_err, cfg.errors_print)
            log_error(str_err, cfg.errors_log)
    return csv_dict


def print_error(str_err='', flag=False):
    if flag:
        print(str_err)


def log_error(str_err='', flag=False):
    if flag:
        logging.error(str_err)


def do_nslookup_by_ip_network(ip_address = ''):
    process = subprocess.Popen(["nslookup", ip_address], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    str_output = str(output)
    #len_output = len(str_output)
    #print(str(output))

    list_output = str_output.split(":")
    if len(list_output) > 4:
        str_temp = list_output[3].strip()
        match = re.search(r"[A-Za-z0-9_-]+\.tm\.novatek\.int", str_temp)
        if match:
            fqdn_name = match.group()
            return fqdn_name
        else:
            str_err = "FQDN - no comparisons found"
            print_error(str_err, cfg.errors_print)
            log_error(str_err, cfg.errors_log)
            return str_err
    else:
        str_err = 'Non-existent domain'
        print_error(str_err, cfg.errors_print)
        log_error(str_err, cfg.errors_log)
        return str_err



def get_list_compname_from_csv(filename_in=''):
    if len(filename_in):
        file_name = filename_in
    else:
        file_name = cfg.file_csv_compnames
    try:
        csvfile = open(file_name, 'rt')
    except:
        str_err = "File not found: " + file_name
        print_error(str_err, cfg.errors_print)
        log_error(str_err, cfg.errors_log)

    csvReader = csv.reader(csvfile, delimiter=",")
    # d = dict()
    lll = list()
    for row in csvReader:
        try:
            compname = row[0]
            # username = row[1]
            # d[compname] = username
            # l.append((row[0], row[1]))
            lll.append(compname)
        except:
            str_err = "COMPNAME not found in: " + compname
            print_error(str_err, cfg.errors_print)
            log_error(str_err, cfg.errors_log)

    # print(d)
    # print(l)
    return lll


def csv2xls(filename=''):
    if os.path.exists(filename) and os.path.isfile(filename):
        file_excel = filename.split('.')[0] + '.xlsx'
        df_new = pd.read_csv(filename, sep=cfg.csv_delimiter)
        writer = pd.ExcelWriter(file_excel)
        df_new.to_excel(writer, index=False)
        writer.save()
    else:

        print('ERROR! can\'t read a file OR file does not exist. File: ' + filename)


# ---------------- do main --------------------------------
def get_nslookup():
    time1 = datetime.now()
    file_excel = ''

    try:
        if os.path.isfile(cfg.file_log):
            os.remove(cfg.file_log)
    except:
        str_err = "Процесс не может получить доступ к файлу, так как этот файл занят другим процессом: : " \
                  + cfg.file_log
        print_error(str_err, cfg.errors_print)
        log_error(str_err, cfg.errors_log)

    try:
        if os.path.isfile(cfg.file_csv):
            os.remove(cfg.file_csv)
            file_excel = cfg.file_csv.split('.')[0] + '.xlsx'
            if os.path.isfile(file_excel):
                os.remove(file_excel)
    except:
        str_err = "Процесс не может получить доступ к файлу, так как этот файл занят другим процессом: : " +\
                  cfg.file_csv + " или " + file_excel
        print_error(str_err, cfg.errors_print)
        log_error(str_err, cfg.errors_log)

    print('Starting at :' + str(time1))

    with open(cfg.file_csv, 'a', newline='', encoding='utf-8') as csv_file:  # Just use 'w' mode in 3.x
        csv_file_open = csv.DictWriter(csv_file, cfg.csv_out_dict.keys(), delimiter=cfg.csv_delimiter)
        csv_file_open.writeheader()

    #dir_out_log = gfiletools.get_output_directory()


    gfiletools.do_log_file('', cfg.file_log)


    logging.info('!!!!!!!!!!!!!!!!!!!!!!!!')
    #compname = "korotenko"
    list_compnames = get_list_compname_from_csv()
    list_response = []
    if len(list_compnames) > 1:
        del list_compnames[0]  # deleting first element

    for compname in list_compnames:
       dict_ad_response = dict(do_nslookup_network(compname))
       list_response.append(dict_ad_response)



    csv2xls(cfg.file_csv)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')
    return list_response

# if __name__ == '__main__':
#     main()

