import json
import re
from datetime import datetime
import requests
import time
import uuid
from .Pinger import *
from .Validator import *

class TwistError(Exception):
    #'''Class to represent a TwistException.#'''

    def __init__(self, message, status_code):
        Exception.__init__(self, '{}: {}'.format(message, status_code))
        
class TwistClient():
    #'''Class to define client for the Twist API.#'''

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
        #'''Check response.#'''
        if not resp.status_code == target:
            raise TwistError(resp.content, resp.status_code)

        return resp.json()

    def get(self, url, params=None, timeout = 60):
        #'''GET method.#'''
        if not params:
            params = {}

        resp = self.__session.get(self.__host + url, params=params, timeout = self.__timeout)
        return self.check_response(resp, 200)
    
    def post(self, url, json, target=200, timeout = 60):
        #'''POST method.#'''
        resp = self.__session.post(self.__host + url, json=json, timeout = self.__timeout)
        return self.check_response(resp, target)

    def delete(self, url, params=None, timeout = 60):
        #'''DELETE method.#'''
        if not params:
            params = {}

        resp = self.__session.delete(_HOST + url, params=params, timeout = self.__timeout)
        return self.check_response(resp, 202)

    def get_email_url(self, url):
        #'''Get email URL.#'''
        return url.format(self.__email)

    def get_constructs(self, seqInf, typ='NON_CLONED_GENE'):
    #'''Get constructs.#'''
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
        print(constructs)
        return constructs
    
    # 1
    def get_addresses(self):
        #'''Get addresses.#'''
        return self.get(self.get_email_url('v1/users/{}/addresses/'))
    
    # 2
    def get_payments(self):
        #'''Get payments.#'''
        return self.get(self.get_email_url('v1/users/{}/payments/'))
    
    # 3
    def get_accounts(self):
        #'''Get accounts.#'''
        return self.get(self.get_email_url('v1/accounts/'))
    
    # 4
    def get_prices(self):
        #'''Get prices.#'''
        return self.get('v1/prices/')

    # 5
    def get_user_data(self):
        #'''Get user data.#'''
        return self.get(self.get_email_url('v1/users/{}/'))
    
    # 6
    def get_vectors(self):
        #'''Get vectors.#'''
        return self.get_user_data().get('vectors', [])
    
    # 7
    def submit_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        #'''Submit constructs.#'''
        constructs = self.get_constructs(seqInf, typ)

        return self.post(self.get_email_url('v1/users/{}/constructs/'),
                           constructs, target=201)
    # 8
    def get_scores(self, ids, max_errors=8):
        #'''Get scores.#'''
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
        #'''Get quote.#'''
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
        #'''Check quote.#'''
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
        #'''Submit order.#'''
        return self.post(self.get_email_url('v1/users/{}/orders/'),
                           json={'quote_id': quote_id,
                                 'payment_method_id': payment_id}, target = 201)
    # 12
    def delete_quote(self, quote_id):
        #'''Delete quote.#'''
        resp = None

        while True:
            url = self.get_email_url('v1/users/{}/quotes/%s/') % quote_id
            resp = self.delete(url)
            return resp

class Twist(BasePinger):
    #'''Class to define client for the Twist API.#'''

    def __init__(self, email, password, apitoken, eutoken, username, host = 'https://twist-api.twistbioscience-staging.com/', timeout = 60):
        self.running = False        
    
        self.__email = email
        self.__password = password
        self.__apitoken = apitoken
        self.__eutoken = eutoken
        self.__timeout = timeout
        self.__host = host
        self.__username = username
        self.__timeout = timeout
        self.__session = requests.Session()
        self.__session.headers.update(
            {'Authorization': 'JWT ' + ''.join(self.__apitoken.split()),
             'X-End-User-Token': ''.join(self.__eutoken.split()),
             'Accept-Encoding': 'json'})

        self.client = TwistClient(self.__email, 
                      self.__password, self.__apitoken, self.__eutoken,
                      self.__username,
                      self.__host, self.__timeout)

        self.offers = []
        self.validator = EntityValidator(raiseError=True)

    #
    #   Encodes a 'SequenceInformation' object into JSON-Format with fields readable by the GeneArtClient.
    #       Returns the newly created object, if the given input is valid. Otherwise raises a 'TypeError'
    #
    def encode_sequence(self, seqInf):
        if isinstance(seqInf, SequenceInformation):
            if self.validator.validate(seqInf):
                return { "idN": seqInf.key, "name": seqInf.name, "sequence": seqInf.sequence}
        else:
            type_name = seqInf.__class__.__name__
            raise InvalidInputError(f"Parameter must be of type SequenceInformation but is of type '{type_name}'.")

    def check_response(self, resp, target):
        #'''Check response.#'''
        try:
            response = self.client.check_response(resp,target)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    def get(self, url, params=None):
        #'''GET method.#'''
        try:
            response = self.client.get(url, params)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    def post(self, url, json, target=200):
        #'''POST method.#'''
        try:
            response = self.client.post(url, json, target)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response


    def delete(self, url, params=None):
        #'''DELETE method.#'''
        try:
            response = self.client.delete(url, params)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    def get_email_url(self, url):
        #'''Get email URL.#'''
        try:
            response = self.client.get_email_url(url)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    def get_constructs(self, seqInf, typ='NON_CLONED_GENE'):
    #'''Get constructs.#'''
        try:
            response = self.client.get_constructs(seqInf, typ)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    # 1
    def get_addresses(self):
        #'''Get addresses.#'''
        try:
            response = self.client.get_addresses()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    
    # 2
    def get_payments(self):
        #'''Get payments.#'''
        try:
            response = self.client.get_payments()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    # 3
    def get_accounts(self):
        #'''Get accounts.#'''
        try:
            response = self.client.get_accounts()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    # 4
    def get_prices(self):
        #'''Get prices.#'''
        try:
            response = self.client.get_prices()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    # 5
    def get_user_data(self):
        #'''Get user data.#'''
        try:
            response = self.client.get_user_data()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    # 6
    def get_vectors(self):
        #'''Get vectors.#'''
        try:
            response = self.client.get_vectors()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    
    # 7
    def submit_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        #'''Submit constructs.#'''
        try:
            response = self.client.submit_constructs(seqInf, typ)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    # 8
    def get_scores(self, ids, max_errors=8):
        #'''Get scores.#'''
        try:
            response = self.client.get_scores(ids, max_errors)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    
    # 9
    def get_quote(self, construct_ids, external_id, address_id,
                  first_name, last_name,
                  typ='96_WELL_PLATE', fill_method='VERTICAL',
                  shipment_method='MULTIPLE_SHIPMENTS',
                  vectors=None, cloning_strategies=None):
        #'''Get quote.#'''
        try:
            response = self.client.get_quote(construct_ids, external_id, address_id,
                  first_name, last_name,
                  typ, fill_method,
                  shipment_method,
                  vectors, cloning_strategies)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    
    # 10
    def check_quote(self, quote_id):
        #'''Check quote.#'''
        try:
            response = self.client.check_quote(quote_id)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
        
    # 11
    def submit_order(self, quote_id, payment_id):
        #'''Submit order.#'''
        try:
            response = self.client.submit_order(quote_id, payment_id)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    # 12
    def delete_quote(self, quote_id):
        #'''Delete quote.#'''
        try:
            response = self.client.delete_quote(quote_id)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response
    

    #
    #   After:
    #       isRunning() -> true
    #       getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer), SequenceOffer(seqInf[1], self.tempOffer), ...
    #                           SequenceOffer(seqInf[n], self.tempOffer)]
    #
    def searchOffers(self, seqInf):
        # Check pinger is not running
        if(self.isRunning()):
            raise IsRunningError("Pinger is currently running and can not perform a other action")
        try:
            self.running = True
            offers = [] # Empty Offers List
            twistSequences  = []
            constrcutIds = []
            
            for s in seqInf:
                # Encode each element in JSON-Format with fields readable by the TWISTClient and add it to the list.
                seq = self.encode_sequence(s)
                twistSequences.append(seq)
            
            sequences = [x['sequence'] for x in twistSequences]
            names = [y['name'] for y in twistSequences]

            constructs = self.submit_constructs(twistSequences)

            ids = [i['id'] for i in constructs]
            scores = self.get_scores(ids)
            counter = 0

            for identifier in ids:
                for constructscore in scores:
                    if(constructscore['id'] == identifier):
                        issues = constructscore["score_data"]["issues"]
                        if (constructscore["score"] == "BUILDABLE" and len(issues) == 0):
                            messageText = constructscore["name"] + "_" + "accepted"
                            message = Message(MessageType.INFO, messageText)
                        if (constructscore["score"] != "BUILDABLE" and len(issue) != 0):
                            messageText = constructscore["name"] + "_" + "rejected_"
                            for issue in issues:
                                messageText = messageText + issue + "."                            
                            message = Message(MessageType.SYNTHESIS_ERROR, messageText)
                        self.validator.validate(message)
                    seqOffer = SequenceOffers(twistSequences[counter], [Offer(messages = [message])])
                    self.validator.validate(seqOffer)
                counter = counter + 1 
            
            self.offers = offers
            self.running = False
        except InvalidInputError as err:
            self.running = False
            raise InvalidInputError from err
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got a error") from err
        except UnavailableError as err:
            self.running = False
            raise UnavailableError from err
        except Exception as err:
            self.running = False
            raise UnavailableError from err

    #
    #   Checks if the Pinger is Running.
    #
    def isRunning(self):
        return self.running

    #
    #   Returns List with a  SequenceOffer for every sequence in last searchOffers(seqInf)-call.
    #   Every SequenceOffer contains the same offers. Default 1 see self.tempOffer and self.offers.
    #
    def getOffers(self):
        return self.offers

    #
    #   Desc:   Resets the pinger by
    #               - stop searching -> isRunning() = false
    #               - resets the offers to a empty list -> getOffers = []
    #
    def clear(self):
        self.running = False
        self.offers = [] # Empty Offers List



    #
    #   Desc:   Create a request to trigger an order.
    #
    #   @param offerIds
    #           Type ArrayOf(int). Id of the Offer to Order. Ids must be unique.
    #
    #   @results
    #           Type Entities.Order. Representation of the order.
    #
    #   @throws InvalidInputError
    #           if input parameter are not like expected (see parameter definition above).
    #
    #   @throws IsRunningError
    #           if the Pinger is already running. You have to wait until it is finished.
    #
    #   @throws UnavailableError
    #           if authentication response not matches pattern or not received.
    #           Maybe the base url of the API is wrong? API could be only temporary
    #           unavailable.
    #
#    def order(self, offerIds):
