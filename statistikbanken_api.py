#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import json

class Statbank_api():

    url = 'http://api.statbank.dk/v1/'

    def get_json(self, url, endpoint, post_body):
        '''
         Henter JSON data fra url.
        '''

        req = urllib2.Request(url + endpoint, headers={'Content-Type': 'application/json'})
        response = urllib2.urlopen(req, json.dumps(post_body))
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

        data = {'subjects': subject_ids, 'format': 'JSON', 'recursive': 'true'}
        return self.get_json(self.url, 'subjects', data)

    def get_tables(self, subject):
        '''Returning tables within a subject with "område" as a variable and "101"
        as one of the values indicating table might contain municipality code
        as an geographic reference'''

        def has_municipalitycode(table_id):
            '''Check if table holds municipality codes and return boolean'''
            endpoint = 'tableinfo'
            post_body = \
                {
                    "table": table_id
                }
            res = self.get_json(self.url, endpoint, post_body)

            if any(item['id'] == u'OMRÅDE' and any(i['id'] == '101' for i in item['values']) for item in res['variables'] ):
                return True
            else:
                return False

        #Preparing request
        endpoint = 'tables'
        post_body = \
            {
                "subjects": [
                    subject
                ]
            }

        tables = self.get_json(self.url, endpoint, post_body)

        # Filtering tables with "område" as variable and municipalitycode 101 as value
        table_list = []

        for table in tables:
            if u'område' in table['variables'] and has_municipalitycode(table['id']):
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

