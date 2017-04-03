#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests

baseurl = 'http://api.statbank.dk/v1/'

def get_json(url,function, data):
    '''
     Henter JSON data fra url.
    '''

    return requests.post(url + function, data).json()


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

if __name__ == '__main__':
    # get_all_subjects()
    # get_main_subjects()
    # get_subjects(['02'])