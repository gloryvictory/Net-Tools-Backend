# https://github.com/requests/requests-ntlm/issues/65
# !/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   Author          : Viacheslav Zamaraev
#   email           : zamaraev@gmail.com
#   Script Name     : nslookup_db_get.py
#   Created         : 22th July 2020
#   Last Modified	: 22th July 2020
#   Version		    : 1.0
#   PIP             : pip install peewee
#   RESULT          : push nslookup data
# Modifications	: 1.1 -
#               : 1.2 -
#
# Description   : push nslookup data


import datetime
import logging
import re
from datetime import datetime

import cfg
import db

#
# route http://127.0.0.1:5000/nslookuptodb
# получает прямую и обратную зону и сохраняет все в базу данных
# ---------------- do main --------------------------------
def get_nslookup_from_db():
    time1 = datetime.now()
    print('Starting at :' + str(time1))

    #compname = "korotenko"
    list_response = []
    nslookup_db_all_records = db.NSLookup().select()


    for rec in nslookup_db_all_records:
        #dict_ad_response = dict(                                )
        list_response.append({
            'COMPNAME': rec.COMPNAME,
            'DC': rec.DC,
            'DC_IP': rec.DC_IP,
            'FQDN': rec.FQDN,
            'FQDN_IP': rec.FQDN_IP,
            'NAME_BY_IP': rec.NAME_BY_IP,
            'WARNING': rec.WARNING,
            'LASTUPDATE': rec.LASTUPDATE
        })

        #list_response.append(dict_ad_response)

    time2 = datetime.now()
    print('Finishing at :' + str(time2))
    print('Total time : ' + str(time2 - time1))
    print('DONE !!!!')
    #str_response = str(len(list_response))

    return list_response

