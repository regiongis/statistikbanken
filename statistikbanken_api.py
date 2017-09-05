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

    def data_url(self, table):
        '''preparing variables and other param for the url'''

        var = table["variables"]
        var_lst = []

        for key, value in var.iteritems():
            var_lst.append(urllib2.quote(key) + '=' + ','.join(value))

        urlvar = '&'.join(var_lst)
        endpoint = 'data'
        uri = 'CSV:/vsicurl_streaming/{0}{1}/{2}/CSV?valuePresentation=Code&delimiter=Semicolon&{3}'.format(self.url,endpoint,table['table_id'],urlvar)

        return uri

    def add_layer(self, layer_name, path):
        '''add data to layers panel (uses GET request for DST data)'''
        data = QgsVectorLayer(path, layer_name, 'ogr')
        return QgsMapLayerRegistry.instance().addMapLayer(data)



table = {
    "table_id": "folk1a",
    "variables": {
        "OMRÅDE": ["*"],
        "TID": ["2017K2", "2017K3"],
        "KØN": ['TOT']
    }
}

dst = Statbank_api()
test = dst.data_url(table)
print test
#dst.add_layer(table['table_id'], test)

## tilføj kommune lag (Denne sti skal sættes til data folderen i statistikbank plugin mappen)
#geom_path = '/home/baffioso/.qgis2/python/plugins/statistikbanken-treewidget/data/kommune.geojson'
#kom =  QgsVectorLayer(geom_path, 'kommune', 'ogr')
#QgsMapLayerRegistry.instance().addMapLayer(kom)
#
## tilføj DST data (her bruges GET request)
#uri = 'CSV:/vsicurl_streaming/http://api.statbank.dk/v1/data/folk1a/CSV?valuePresentation=Code&delimiter=Semicolon&OMR%C3%85DE=*&Tid=2017K2'
#dst = QgsVectorLayer(uri, 'folk1a', 'ogr')
#QgsMapLayerRegistry.instance().addMapLayer(dst)
#
##Lav join mellem kommunekode (Vi skal finde ud af om kommunekode altid hedder 'OMRÅDE' hos DST)
#omr = u'OMRÅDE'
#komkode = 'KOMKODE'
#joinObject = QgsVectorJoinInfo()
#joinObject.joinLayerId = dst.id()
#joinObject.joinFieldName = omr
#joinObject.targetFieldName = komkode
#joinObject.memoryCache = True
#kom.addJoin(joinObject)

