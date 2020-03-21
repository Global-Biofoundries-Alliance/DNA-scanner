import json
import re
from datetime import datetime
import requests
import time
import uuid
from .Pinger import *
from .Validator import *

    #Class to represent a TwistException.
class TwistError(Exception):

    def __init__(self, message, status_code):
        Exception.__init__(self, '{}: {}'.format(message, status_code))
        
    #Class to define client for the Twist API.
    # This implementation is based on version 1.0.10846 of the TWIST-API.
    # All documentation for the API can be found here: https://twist-api.twistbioscience-staging.com/login?next=/swagger/
class TwistClient():

    def __init__(self, email, password, apitoken, eutoken, username, firstname, lastname, host = 'https://twist-api.twistbioscience-staging.com/', timeout = 60):
        self.__email = email
        self.__password = password
        self.__apitoken = apitoken
        self.__eutoken = eutoken
        self.__username = username
        self.__firstname = firstname
        self.__lastname = lastname
        self.__host = host
        self.__timeout = timeout
        self.__session = requests.Session()
        self.__session.headers.update(
            {'Authorization': 'JWT ' + ''.join(self.__apitoken.split()),
             'X-End-User-Token': ''.join(self.__eutoken.split()),
             'Accept-Encoding': 'json'})
        addresses = self.get_addresses()
        self.address = "No_Address"
        for add in addresses:
            if(add['first_name'] == self.__firstname and add['last_name'] == self.__lastname):
                self.address = add['id']
        if(self.address == "No_Address"):
            raise AuthenticationError("The given first name and last name do not have a shipping address for this account.")

            #Check response. Throws a TwistError if the response's status code is not the expected one.
    def check_response(self, resp, target):
        if not resp.status_code == target:
            raise TwistError(resp.content, resp.status_code)

        return resp.json()

        #GET method.
    def get(self, url, params=None, timeout = 60):
        if not params:
            params = {}

        resp = self.__session.get(self.__host + url, params=params, timeout = self.__timeout)
        return self.check_response(resp, 200)
    
        #POST method.
    def post(self, url, json, target=200, timeout = 60):
        resp = self.__session.post(self.__host + url, json=json, timeout = self.__timeout)
        return self.check_response(resp, target)

        #DELETE method.
    def delete(self, url, params=None, timeout = 60):
        if not params:
            params = {}

        resp = self.__session.delete(self.__host + url, params=params, timeout = self.__timeout)
        return self.check_response(resp, 202)

        #Get email URL.
    def get_email_url(self, url):
        return url.format(self.__email)

        #Get constructs.
    def get_constructs(self, seqInf, typ='NON_CLONED_GENE'):
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
        return constructs
    
        #Get addresses.
    def get_addresses(self):
        return self.get(self.get_email_url('v1/users/{}/addresses/'))
    
        #Get payments.
    def get_payments(self):
        return self.get(self.get_email_url('v1/users/{}/payments/'))
    
        #Get accounts.
    def get_accounts(self):
        return self.get(self.get_email_url('v1/accounts/'))
    
        #Get prices.
    def get_prices(self):
        return self.get('v1/prices/')

        #Get user data.
    def get_user_data(self):
        return self.get(self.get_email_url('v1/users/{}/'))
    
        #Get vectors.
    def get_vectors(self):
        return self.get_user_data().get('vectors', [])
    
        #Submit constructs.
    def submit_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        constructs = self.get_constructs(seqInf, typ)

        return self.post(self.get_email_url('v1/users/{}/constructs/'),
                           constructs, target=201)

        #Get scores.
    def get_scores(self, ids, max_errors=8):
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
    
        #Get quote.
    def get_quote(self, construct_ids, external_id, address_id,
                  first_name, last_name,
                  typ='96_WELL_PLATE', fill_method='VERTICAL',
                  shipment_method='MULTIPLE_SHIPMENTS',
                  vectors=None, cloning_strategies=None):

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
    
        #Check quote.
    def check_quote(self, quote_id):
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
        
        #Submit order.
    def submit_order(self, quote_id, payment_id):
        return self.post(self.get_email_url('v1/users/{}/orders/'),
                           json={'quote_id': quote_id,
                                 'payment_method_id': payment_id}, target = 201)
        #Delete quote.
    def delete_quote(self, quote_id):
        resp = None

        while True:
            url = self.get_email_url('v1/users/{}/quotes/%s/') % quote_id
            resp = self.delete(url)
            return resp
