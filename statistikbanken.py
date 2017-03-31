#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json

baseurl = 'http://api.statbank.dk/v1/'

def getjson(url):
    response = urllib \
        .request \
        .urlopen(url) \
        .read() \
        .decode('utf8')
    return json.loads(response)


###########################
##          EMNER        ##
###########################

def getallsubjects():
    """Henter alle emner, underemer og tabeller"""
    json_obj = getjson(baseurl + 'subjects?recursive=true&includeTables=true')
    return json_obj

def getmainsubjects():
    """hent alle hovedemner"""
    json_obj = getjson(baseurl + 'subjects')
    for i in range(len(json_obj)):
        print(json_obj[i]['id'], json_obj[i]['description'])

def getsubjects(subject_id):
    """hent underemner for et emne"""
    json_obj = getjson(baseurl + 'subjects/' + subject_id)
    if json_obj[0]['hasSubjects'] == True:
        for i in range(len(json_obj[0]['subjects'])):
            print(json_obj[0]['subjects'][i]['id'], json_obj[0]['subjects'][i]['description'])
    else:
        print('Har ingen underemner')


#getmainsubjects()
#print(getallsubjects())
getsubjects('02')