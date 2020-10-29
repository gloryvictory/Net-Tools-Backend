# https://github.com/requests/requests-ntlm/issues/65
# !/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          : Viacheslav Zamaraev
#   email           : zamaraev@gmail.com
#   Script Name     : nslookup_db_update.py
#   Created         : 22th July 2020
#   Last Modified	: 22th July 2020
#   Version		    : 1.0
#   PIP             : pip install peewee
#   RESULT          : make database and push nslookup data
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : make database and push nslookup data


import datetime
import logging
import subprocess
import re
import csv
from datetime import datetime

import gfiletools
import cfg
import db


def do_nslookup_network(compname = ''):
    csv_dict = cfg.csv_out_dict

    str_fqdn = ''
    str_name_by_ip = ''

    # process = subprocess.Popen(["nslookup", "10.72.41.126"], stdout=subprocess.PIPE)
    process = subprocess.Popen(["nslookup", compname], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    str_output = str(output)
    len_output = len(str_output)

    for key in csv_dict:
        csv_dict[key] = ''

    csv_dict['COMPNAME'] = str(compname).upper()
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
            else:
                str_err = "DC - no comparisons found"
                print_error(str_err, cfg.errors_print)

            # ищем IP address контроллера домена
            str_temp = list_output[2].strip()
            match = re.search(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", str_temp)
            if match:
                dc_ip = match.group()
                csv_dict['DC_IP'] = dc_ip
            else:
                str_err = "dc_ip (IP address of Domain Controller) - no comparisons found"
                print_error(str_err, cfg.errors_print)
            if len_list_output > 3:
                # ищем имя компа
                str_temp = list_output[3].strip()
                match = re.search(r"[A-Za-z0-9_-]+\.tm\.novatek\.int", str_temp)
                if match:
                    fqdn_name = match.group()
                    str_fqdn = str(fqdn_name).upper()
                    csv_dict['FQDN'] = str_fqdn
                else:
                    str_err = "FQDN - no comparisons found"
                    print_error(str_err, cfg.errors_print)
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
                else:
                    str_err = "compname_ip - no comparisons found: "
                    print_error(str_err, cfg.errors_print)
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
                print(csv_dict['COMPNAME'])

            except Exception as e:
                str_err = "Exception occurred " + str(e)
                print_error(str_err, cfg.errors_print)
        else:
            # это ситуация, когда есть прямая зона, а обратной нет!!!

            str_err = 'Len list_output less than less 4 in text:' + str_output
            print_error(str_err, cfg.errors_print)
    else:
        str_err = 'Len list_output less than 4 in text:' + str_output
        print_error(str_err, cfg.errors_print)
    return csv_dict


def print_error(str_err='', flag=False):
    if flag:
        print(str_err)


def do_nslookup_by_ip_network(ip_address = ''):
    process = subprocess.Popen(["nslookup", ip_address], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    str_output = str(output)

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
            return str_err
    else:
        str_err = 'Non-existent domain'
        print_error(str_err, cfg.errors_print)
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

    csvReader = csv.reader(csvfile, delimiter=",")
    # d = dict()
    lll = list()
    for row in csvReader:
        try:
            compname = row[0] # в первой колонке ждем имя компа
            lll.append(compname)
        except:
            str_err = "COMPNAME not found in: " + compname
            print_error(str_err, cfg.errors_print)

    return lll


#
# route http://127.0.0.1:5000/nslookuptodb
# получает прямую и обратную зону и сохраняет все в базу данных
# ---------------- do main --------------------------------
def get_nslookup_to_db():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    gfiletools.do_log_file('', cfg.file_log)
    logging.info('!!!!!!!!!!!!!!!!!!!!!!!!')
    #compname = "korotenko"
    list_compnames = get_list_compname_from_csv()
    list_response = []
    if len(list_compnames) > 1:
        del list_compnames[0]  # deleting first element

    nslookup_db = db.NSLookup()
    try:
        query = nslookup_db.delete()
        n = query.execute()
        print('{} instances deleted'.format(n))
        #db.database.connect()
    except Exception as e:
        str_err = "Exception occurred " + str(e)
        print(str_err)

    for compname in list_compnames:
        dict_ad_response = dict(do_nslookup_network(compname))
        nslookup_db = db.NSLookup()
        nslookup_db.COMPNAME = dict_ad_response['COMPNAME']
        nslookup_db.DC = dict_ad_response['DC']
        nslookup_db.DC_IP = dict_ad_response['DC_IP']
        nslookup_db.FQDN = dict_ad_response['FQDN']
        nslookup_db.FQDN_IP = dict_ad_response['FQDN_IP']
        nslookup_db.NAME_BY_IP = dict_ad_response['NAME_BY_IP']
        nslookup_db.WARNING = dict_ad_response['WARNING']
        try:
            nslookup_db.save()
        except Exception as e:
            str_err = "Error to save any to database. Exception occurred " + str(e)
            print(str_err)

        list_response.append(dict_ad_response)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')
    #str_response = str(len(list_response))

    return list_response

