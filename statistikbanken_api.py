#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import json

class Statbank_api():

    url = 'http://api.statbank.dk/v1/'

    def get_json(self, url, function, data):
        '''
         Henter JSON data fra url.
        '''

        req = urllib2.Request(url + function, headers={'Content-Type': 'application/json'})
        response = urllib2.urlopen(req, json.dumps(data))
        charset = response.headers.getparam('charset')
        result = json.loads(response.read().decode(charset))

        return result

    def get_all_subjects(self):
        '''
        Henter alle emner, underemner og tabeller fra API'et.
        '''
        funktion = 'subjects'
        data = {'recursive': 'true', 'format': 'JSON'}
        return self.get_json(self.url, funktion, data)

    def get_main_subjects(self):
        '''
        Henter alle hovedemner fra API'et.
        '''

        return self.get_json(self.url, 'subjects', {})

    def get_subjects(self, subject_ids):
        '''
        Henter alle underemner fra et eller flere hovedemner.

         Tager i mod en liste af hovedemne id. F.eks. ['02', '03']
        '''

        data = {'subjects': subject_ids, 'format': 'JSON'}
        return self.get_json(self.url, 'subjects', data)

    def has_municipalities(self, subject):
        '''Returning tables within a subject with "område" as an variable,
        indicating data might hold municipality code as an geographic reference'''
        endpoint = 'tables'
        post_body = \
            {
                "subjects": [
                    subject
                ]
            }

        tables = self.get_json(self.url, endpoint, post_body)

        table_list = []

        for table in tables:
            if u'område' in table['variables']:
                table_list.append(table)

        return table_list

    def get_variables(self,table_id):
        '''
        Henter variabler og værdier for en tabel
        '''
        post_body = {
            'table': table_id,
            'format': 'JSON'
        }
        table = self.get_json(self.url, 'tableinfo', post_body)
        variables = table['variables']
        variables_lst = [{'id': i['id'], 'text': i['text'], 'values': i['values']} for i in variables]

        return variables_lst

    def get_data(self, table, variables):
        '''henter data fra API i JSONSTAT format'''
        endpoint = 'data'
        post_body = \
            {
                "table": table,
                "variables": variables,
                "format": "JSONSTAT"
            }
        return self.get_json(self.url, endpoint, post_body)