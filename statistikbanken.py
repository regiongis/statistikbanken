#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import json

baseurl = 'http://api.statbank.dk/v1/'

def get_json(url,function, data):
    '''
     Henter JSON data fra url.
    '''

    req = urllib2.Request(url + function)

    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))

    charset = response.headers.getparam('charset')
    result = response.read().decode(charset)

    return result

def get_all_subjects():
    '''
    Henter alle emner, underemner og tabeller fra API'et. 
    '''
    funktion = 'subjects'
    data = {'recursive': 'true','includetables': 'true', 'format': 'JSON'}
    return get_json(baseurl, funktion, data)

def get_main_subjects():
    '''
    Henter alle hovedemner fra API'et.
    '''

    return get_json(baseurl, 'subjects', {})

def get_subjects(subject_ids):
    '''
    Henter alle underemner fra et eller flere hovedemner.
     
     Tager i mod en liste af hovedemne id. F.eks. ['02', '03']
    '''

    data = {'subjects': subject_ids, 'format': 'JSON'}
    return get_json(baseurl, 'subjects', data)

def get_variables(table_id):
    post_body = {
	    'table': table_id,
	    'format': 'JSON'
    }
    table = get_json(baseurl, 'tableinfo', post_body)
    variables = table['variables']
    variables_lst = [{'id': i['id'], 'text': i['text']} for i in variables]

    return variables_lst

table = 'folk1a'
variables = [
    {'code': 'OMRÅDE', 'values': ["151", "169"]},
    {'code': 'TID', 'values': ["2017K1", "2016K3"]}
]

def get_data(table, variables):
    '''henter data fra API i JSONSTAT format'''
    endpoint = 'data'
    post_body = \
        {
            "table": table,
            "variables": variables,
            "format": "JSONSTAT"
        }
    return get_json(baseurl, endpoint, post_body)



if __name__ == '__main__':
    # get_all_subjects()
    # get_main_subjects()
    # get_subjects(['02'])
    #data = get_variables('FODIE')
    #data = output = get_subjects(['02'])
    #print( output )
    data = get_data(table, variables)
    print data
    #print variables[0]['values']
