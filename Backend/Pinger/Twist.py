import json
import re
from datetime import datetime
import requests
import time
from .Pinger import *
from .Validator import *

class TwistError(Exception):
    #Class to represent a TwistException.

    def __init__(self, message, status_code):
        Exception.__init__(self, '{}: {}'.format(message, status_code))
        
class TwistClient():
    #Class to define client for the Twist API.

    def __init__(self, email, password, apitoken, eutoken, username, host = 'https://twist-api.twistbioscience-staging.com/', timeout = 60):
        self.__email = email
        self.__password = password
        self.__apitoken = apitoken
        self.__eutoken = eutoken
        self.__username = username
        self.__host = host
        self.__timeout = timeout
        self.__session = requests.Session()
        self.__session.headers.update(
            {'Authorization': 'JWT ' + ''.join(self.__apitoken.split()),
             'X-End-User-Token': ''.join(self.__eutoken.split()),
             'Accept-Encoding': 'json'})
    
    def check_response(self, resp, target):
        #Check response.
        if not resp.status_code == target:
            raise TwistError(resp.content, resp.status_code)

        return resp.json()

    def get(self, url, params=None, timeout = 60):
        #GET method.
        if not params:
            params = {}

        resp = self.__session.get(self.__host + url, params=params, timeout = self.__timeout)
        return self.check_response(resp, 200)
    
    def post(self, url, json, target=200, timeout = 60):
        #POST method.
        resp = self.__session.post(self.__host + url, json=json, timeout = self.__timeout)
        return self.check_response(resp, target)

    def delete(self, url, params=None, timeout = 60):
        #DELETE method.
        if not params:
            params = {}

        resp = self.__session.delete(self.__host + url, params=params, timeout = self.__timeout)
        return self.check_response(resp, 202)

    def get_email_url(self, url):
        #Get email URL.
        return url.format(self.__email)

    def get_constructs(self, seqInf, typ='NON_CLONED_GENE'):
    #Get constructs.
        constructs = []
        sequences = [x['sequence'] for x in seqInf]
        names = [y['name'] for y in seqInf]
        for idx, (seq, name) in enumerate(zip(sequences, names)):
            construct = {'sequences': seq,
                         'name': name,
                         'type': typ,
                         'insertion_point_mes_uid': 'na',
                         'vector_mes_uid': 'na',
                         'column': int(idx / 8),
                         'row': int(idx % 8),
                         'plate': int(idx / 96)}

            constructs.append(construct)
        #print(constructs)
        return constructs
    
    # 1
    def get_addresses(self):
        #Get addresses.
        return self.get(self.get_email_url('v1/users/{}/addresses/'))
    
    # 2
    def get_payments(self):
        #Get payments.
        return self.get(self.get_email_url('v1/users/{}/payments/'))
    
    # 3
    def get_accounts(self):
        #Get accounts.
        return self.get(self.get_email_url('v1/accounts/'))
    
    # 4
    def get_prices(self):
        #Get prices.
        return self.get('v1/prices/')

    # 5
    def get_user_data(self):
        #Get user data.
        return self.get(self.get_email_url('v1/users/{}/'))
    
    # 6
    def get_vectors(self):
        #Get vectors.
        return self.get_user_data().get('vectors', [])
    
    # 7
    def submit_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        #Submit constructs.
        constructs = self.get_constructs(seqInf, typ)

        return self.post(self.get_email_url('v1/users/{}/constructs/'),
                           constructs, target=201)
    # 8
    def get_scores(self, ids, max_errors=8):
        #Get scores.
        resp = None
        errors = 0

        while True:
            url = self.get_email_url('v1/users/{}/constructs/describe/')

            try:
                resp = self.get(url, {'scored': 'True',
                                        'id__in': ','.join(ids)})

                if {datum['id'] for datum in resp} == set(ids):
                    break
            except TwistError as exc:
                errors += 1

                if errors == max_errors:
                    raise exc

            time.sleep(1)

        return resp
    
    # 9
    def get_quote(self, construct_ids, external_id, address_id,
                  first_name, last_name,
                  typ='96_WELL_PLATE', fill_method='VERTICAL',
                  shipment_method='MULTIPLE_SHIPMENTS',
                  vectors=None, cloning_strategies=None):
        #Get quote.
        json = {'external_id': external_id,
                'containers': [{'constructs': [
                    {'index': index+1, 'id': id_}
                    for index, id_ in enumerate(construct_ids)],
                    'type': typ,
                    'fill_method': fill_method}],
                'shipment': {'recipient_address_id': address_id,
                             'first_name': first_name,
                             'last_name': last_name,
                             'preferences': {
                                 'shipment_method': shipment_method}},
                'vectors': vectors or [],
                'cloning_strategies': cloning_strategies or [],
                'advanced_options': {}}
        url = self.get_email_url('v1/users/{}/quotes/')
        resp = self.post(url, json=json, target=201)

        return resp['id']
    
    # 10
    def check_quote(self, quote_id):
        #Check quote.
        resp = None

        while True:
            url = self.get_email_url('v1/users/{}/quotes/%s/') % quote_id
            resp = self.get(url)

            if resp['status_info']['status'] != 'PENDING':
                break

            time.sleep(100)

        if resp['status_info']['status'] == 'SUCCESS':
            return resp
        raise ValueError(resp['status_info']['status'])
        
    # 11
    def submit_order(self, quote_id, payment_id):
        #Submit order.
        return self.post(self.get_email_url('v1/users/{}/orders/'),
                           json={'quote_id': quote_id,
                                 'payment_method_id': payment_id}, target = 201)
    # 12
    def delete_quote(self, quote_id):
        #Delete quote.
        resp = None

        while True:
            url = self.get_email_url('v1/users/{}/quotes/%s/') % quote_id
            resp = self.delete(url)
            return resp
