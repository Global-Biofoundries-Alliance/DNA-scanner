'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
# pylint: disable=invalid-name
# pylint: disable=no-self-use
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-statements
# pylint: disable=too-many-public-methods
import time
import uuid

import requests

from .Entities import AuthenticationError, Currency, InvalidInputError, \
    Message, MessageType, Offer, Order, Price, SequenceInformation, \
    SequenceOffers, UnavailableError, UrlRedirectOrder
from .Pinger import BasePinger, IsRunningError
from .Validator import EntityValidator


class TwistError(Exception):
    '''Class to represent a TwistException.'''

    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        Exception.__init__(self, '{}: {}'.format(message, status_code))


class TwistClient():
    ''' Class to define client for the Twist API.
        This implementation is based on version 1.0.10846 of the TWIST-API.
        All documentation for the API can be found here:
        https://twist-api.twistbioscience-staging.com/login?next=/swagger/'''

    def __init__(self, email, password, apitoken, eutoken, username, firstname,
                 lastname,
                 host='https://twist-api.twistbioscience-staging.com/',
                 timeout=60):
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
            if add['first_name'] == self.__firstname \
               and add['last_name'] == self.__lastname:
                self.address = add['id']

        if self.address == "No_Address":
            raise AuthenticationError(
                "The given first name and last name do not have a shipping "
                "address for this account.")

    def check_response(self, resp, target):
        '''Check response. Throws a TwistError if the response's status code
        is not the expected one.'''
        if not resp.status_code == target:
            raise TwistError(resp.content, resp.status_code)

        return resp.json()

    def get(self, url, params=None, _=60):
        '''GET method.'''
        if not params:
            params = {}

        resp = self.__session.get(
            self.__host + url, params=params, timeout=self.__timeout)
        return self.check_response(resp, 200)

    def post(self, url, json, target=200, _=60):
        '''POST method.'''
        resp = self.__session.post(
            self.__host + url, json=json, timeout=self.__timeout)
        return self.check_response(resp, target)

    def delete(self, url, params=None, _=60):
        '''DELETE method.'''
        if not params:
            params = {}

        resp = self.__session.delete(
            self.__host + url, params=params, timeout=self.__timeout)
        return self.check_response(resp, 202)

    def get_email_url(self, url):
        '''Get email URL.'''
        return url.format(self.__email)

    def get_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        '''Get constructs.'''
        constructs = []
        sequences = [x['sequence'] for x in seqInf]
        names = [y['name'] for y in seqInf]
        for idx, (seq, name) in enumerate(zip(sequences, names)):
            construct = {'sequences': seq,
                         'name': name[:32],
                         'type': typ,
                         'insertion_point_mes_uid': 'na',
                         'vector_mes_uid': 'na',
                         'column': int(idx / 8),
                         'row': int(idx % 8),
                         'plate': int(idx / 96)}

            constructs.append(construct)
        return constructs

    def get_addresses(self):
        '''Get addresses.'''
        return self.get(self.get_email_url('v1/users/{}/addresses/'))

    def get_payments(self):
        '''Get payments.'''
        return self.get(self.get_email_url('v1/users/{}/payments/'))

    def get_accounts(self):
        '''Get accounts.'''
        return self.get(self.get_email_url('v1/accounts/'))

    def get_prices(self):
        '''Get prices.'''
        return self.get('v1/prices/')

    def get_user_data(self):
        '''Get user data.'''
        return self.get(self.get_email_url('v1/users/{}/'))

    def get_vectors(self):
        '''Get vectors.'''
        return self.get_user_data().get('vectors', [])

    def submit_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        '''Submit constructs.'''
        constructs = self.get_constructs(seqInf, typ)

        return self.post(self.get_email_url('v1/users/{}/constructs/'),
                         constructs, target=201)

    def get_scores(self, ids, max_errors=100):
        '''Get scores.'''
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

    def get_quote(self, construct_ids, external_id, address_id,
                  first_name, last_name,
                  typ='96_WELL_PLATE', fill_method='VERTICAL',
                  shipment_method='MULTIPLE_SHIPMENTS',
                  vectors=None, cloning_strategies=None):
        '''Get quote.'''

        json = {'external_id': external_id,
                'containers': [{'constructs': [
                    {'index': index + 1, 'id': id_}
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

    def check_quote(self, quote_id):
        '''Check quote. Throws ValueError if the quote couldn't be checked by
        the server.'''
        resp = None

        while True:
            url = self.get_email_url('v1/users/{}/quotes/%s/') % quote_id
            resp = self.get(url)

            if resp['status_info']['status'] != 'PENDING':
                break

            time.sleep(50)

        if resp['status_info']['status'] == 'SUCCESS':
            return resp
        raise ValueError(resp['status_info']['status'])

    def submit_order(self, quote_id, payment_id):
        '''Submit order.'''
        return self.post(self.get_email_url('v1/users/{}/orders/'),
                         json={'quote_id': quote_id,
                               'payment_method_id': payment_id}, target=201)

    def delete_quote(self, quote_id):
        '''Delete quote.'''
        # resp = None
        url = self.get_email_url('v1/users/{}/quotes/%s/') % quote_id
        resp = self.delete(url)
        return resp


class Twist(BasePinger):
    '''Class to define pinger for the Twist API.'''
    currencies = {"EUR": Currency.EUR, "USD": Currency.USD}

    def __init__(self, email, password, apitoken, eutoken, username, firstname,
                 lastname,
                 host='https://twist-api.twistbioscience-staging.com/',
                 timeout=60):
        super().__init__()
        self.running = False

        self.__email = email
        self.__password = password
        self.__apitoken = apitoken
        self.__eutoken = eutoken
        self.__timeout = timeout
        self.__host = host
        self.__username = username
        self.__firstname = firstname
        self.__lastname = lastname
        self.__timeout = timeout
        try:
            self.client = TwistClient(self.__email,
                                      self.__password,
                                      self.__apitoken,
                                      self.__eutoken,
                                      self.__username,
                                      self.__firstname,
                                      self.__lastname,
                                      self.__host, self.__timeout)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err
        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " +
                str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        self.__address = self.client.address
        self.vendorMessage = []
        self.offers = []
        self.validator = EntityValidator(raiseError=True)

    def encode_sequence(self, seqInf):
        '''Encodes a 'SequenceInformation' object into JSON-Format with fields
        readable by the GeneArtClient.
        Returns the newly created object, if the given input is valid.
        Otherwise raises a \'TypeError\'.'''
        if isinstance(seqInf, SequenceInformation):
            if self.validator.validate(seqInf):
                return {"idN": seqInf.key, "name": seqInf.name,
                        "sequence": seqInf.sequence}

            return None

        type_name = seqInf.__class__.__name__
        raise InvalidInputError(
            f"Parameter must be of type SequenceInformation but is of "
            f"type '{type_name}'.")

    def check_response(self, resp, target):
        ''' Check response. Throws a TwistError if the response's status code is
        not the expected one.'''
        try:
            response = self.client.check_response(resp, target)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err
        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get(self, url, params=None):
        '''GET method.'''
        try:
            response = self.client.get(url, params)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def post(self, url, json, target=200):
        '''POST method.'''
        try:
            response = self.client.post(url, json, target)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def delete(self, url, params=None):
        '''DELETE method.'''
        try:
            response = self.client.delete(url, params)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_email_url(self, url):
        '''Get email URL.'''
        try:
            response = self.client.get_email_url(url)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        '''Get constructs.'''
        try:
            response = self.client.get_constructs(seqInf, typ)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_addresses(self):
        '''Get addresses.'''
        try:
            response = self.client.get_addresses()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_payments(self):
        '''Get payments.'''
        try:
            response = self.client.get_payments()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_accounts(self):
        '''Get accounts.'''
        try:
            response = self.client.get_accounts()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

        #
    def get_prices(self):
        '''Get prices.'''
        try:
            response = self.client.get_prices()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_user_data(self):
        '''Get user data.'''
        try:
            response = self.client.get_user_data()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_vectors(self):
        '''Get vectors.'''
        try:
            response = self.client.get_vectors()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def submit_constructs(self, seqInf, typ='NON_CLONED_GENE'):
        '''Submit constructs.'''
        try:
            response = self.client.submit_constructs(seqInf, typ)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_scores(self, ids, max_errors=100):
        '''Get scores.'''
        try:
            response = self.client.get_scores(ids, max_errors)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def get_quote(self, construct_ids, external_id, address_id,
                  first_name, last_name,
                  typ='96_WELL_PLATE', fill_method='VERTICAL',
                  shipment_method='MULTIPLE_SHIPMENTS',
                  vectors=None, cloning_strategies=None):
        '''Get quote.'''

        json = {'external_id': external_id,
                'containers': [{'constructs': [
                    {'index': index + 1, 'id': id_}
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

    def check_quote(self, quote_id):
        '''Check quote.'''
        try:
            response = self.client.check_quote(quote_id)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        except ValueError as error:
            raise UnavailableError("Quote couldn't be checked.") from error

        return response

    def submit_order(self, quote_id, payment_id):
        '''Submit order.'''
        try:
            response = self.client.submit_order(quote_id, payment_id)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        except TwistError as exc:
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def delete_quote(self, quote_id):
        '''Delete quote.'''
        try:
            response = self.client.delete_quote(quote_id)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err
        except TwistError as exc:
            self.running = False
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc

        return response

    def searchOffers(self, seqInf):
        '''After:

            isRunning() -> true
            getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer),
                            SequenceOffer(seqInf[1], self.tempOffer), ...
                            SequenceOffer(seqInf[n], self.tempOffer)]'''
        # Check pinger is not running
        if self.isRunning():
            raise IsRunningError(
                "Pinger is currently running and can not perform a other "
                "action")
        try:
            self.running = True
            offers = []  # Empty Offers List
            twistSequences = []
            # constrcutIds = []
            self.vendorMessage = []

            for s in seqInf:
                # Encode each element in JSON-Format with fields readable by
                # the TWISTClient and add it to the list.
                self.validator.validate(s)
                seq = self.encode_sequence(s)
                twistSequences.append(seq)

            constructs = self.submit_constructs(twistSequences)

            ids = [i['id'] for i in constructs]
            scores = self.get_scores(ids)
            counter = 0
            idsforquoting = []
            for identifier in ids:
                for constructscore in scores:
                    if constructscore['id'] == identifier:
                        issues = constructscore["score_data"]["issues"]
                        # If the construct can be produced
                        if constructscore["score"] == "BUILDABLE" \
                                and len(issues) == 0:
                            messageText = constructscore["name"] + "_" + \
                                "accepted" + "->ConstructID =" + \
                                str(identifier)
                            message = Message(MessageType.INFO, messageText)
                            idsforquoting.append(identifier)

                        # If the construct can not be produced
                        if constructscore["score"] != "BUILDABLE" \
                                and len(issues) != 0:
                            messageText = constructscore["name"] + \
                                "_" + "rejected_"
                            for issue in issues:
                                messageText = messageText + \
                                    issue['title'] + "."
                            message = Message(
                                MessageType.SYNTHESIS_ERROR, messageText)
                        turnOverTime = -1
                        price = Price()
                        self.validator.validate(message)
                        currentOffer = Offer(
                            price=price, turnovertime=turnOverTime,
                            messages=[message])
                        seqOffer = SequenceOffers(
                            seqInf[counter], [currentOffer])
                        offers.append(seqOffer)
                        self.validator.validate(seqOffer)
                        counter = counter + 1

            self.offers = offers
            quoteID = self.get_quote(idsforquoting,
                                     external_id=str(uuid.uuid4()),
                                     address_id=self.__address,
                                     first_name=self.__firstname,
                                     last_name=self.__lastname)

            quote = self.check_quote(quoteID)
            turnOverTime = quote['tat']['business_days']
            amount = quote['quote']['price']
            self.delete_quote(quoteID)
            self.vendorMessage = \
                [Message(MessageType.VENDOR_INFO,
                         "Twist can only provide the total price and time of "
                         "the synthesizable sequences. Price: " + str(
                             amount) + " $ , Time: " + str(turnOverTime) +
                         " BD")]
            self.running = False

        except TwistError as exc:
            self.running = False
            raise UnavailableError(
                "Request got an error: " + str(exc.message) +
                "and status code = " + str(exc.status_code)) from exc
        except InvalidInputError as err:
            self.running = False
            raise InvalidInputError from err
        except requests.exceptions.RequestException as err:
            self.running = False
            raise UnavailableError("Request got a error") from err
        except UnavailableError as err:
            self.running = False
            raise UnavailableError(str(err))
        except Exception as err:
            self.running = False
            raise UnavailableError from err

    def isRunning(self):
        ''' Checks if the Pinger is Running.'''
        return self.running

    def getOffers(self):
        '''
        Returns List with a  SequenceOffer for every sequence in last
        searchOffers(seqInf)-call.

        Every SequenceOffer contains the same offers. Default 1 see
        self.tempOffer and self.offers.
        '''
        return self.offers

    def getVendorMessages(self):
        '''
        Returns List with a Vendor Message from the last
        searchOffers(seqInf)-call.

        The Vendor Message contains information regarding the price and
        delivery time of all the producible sequences of the seqInf list
        which was previously used in the searchOffers(seqInf)-call.
        '''
        return self.vendorMessage

    def addVendorMessage(self, message):
        '''Adds a vendor message to this vendor's message store.

        @result
            Type Message
            The message to be added
        '''
        self.vendorMessage.append(message)

    def clear(self):
        '''
        Resets the pinger by
            - stop searching -> isRunning() = false
            - resets the offers to a empty list -> getOffers = []
        '''
        self.running = False
        self.offers = []  # Empty Offers List
        self.vendorMessage = []  # Empty vendorMessage List

    def order(self, offerIds):
        '''
        Create a request to trigger an order.

        @param offerIds
            Type ArrayOf(int). Id of the Offer to Order. Ids must be unique.

        @results
            Type Entities.Order. Representation of the order.

        @throws InvalidInputError
            if input parameter are not like expected (see parameter definition
            above).

        @throws IsRunningError
            if the Pinger is already running. You have to wait until it is
            finished.

        @throws UnavailableError
            if authentication response not matches pattern or not received.
            Maybe the base url of the API is wrong? API could be only temporary
            unavailable.
        '''
        # Check pinger is not running
        if self.isRunning():
            raise IsRunningError(
                "Pinger is currently running and can not perform a other "
                "action")

        # Check type of offersIds
        if not isinstance(offerIds, list):
            raise InvalidInputError("offerIds is not a list")

        for offer_id in offerIds:
            if not isinstance(offer_id, int):
                raise InvalidInputError("offerIds contains not-integer value")

        self.running = True
        constructIDs = []
        # addresses = self.get_addresses()
        payments = self.get_payments()

        if payments:
            try:
                # List to collect tuples of type (SequenceInformation)
                offersToBuy = []

                # find offers with id in given offerIds
                for sequenceOffer in self.offers:
                    for offer in sequenceOffer.offers:
                        # match
                        if offer.key in offerIds:
                            # add to list
                            offersToBuy.append(
                                sequenceOffer.sequenceInformation)
                            messagetext = offer.messages[0].text
                            constructIDs.append(
                                messagetext[-36:len(messagetext)])

                if len(offersToBuy) != len(offerIds):
                    raise InvalidInputError(
                        "Some of the offerIds are not found")

                print("Order", len(offersToBuy), "sequences at TWIST")
                order = Order()

                quoteID = self.get_quote(constructIDs,
                                         external_id=str(uuid.uuid4()),
                                         address_id=self.__address,
                                         first_name=self.__firstname,
                                         last_name=self.__lastname)

                quote = self.check_quote(quoteID)
                redirectURL = quote['pdf_download_link']
                # Ordering is DEACTIVATED. Uncomment the next line to activate
                # the ordering operation.
                # self.submit_order(quoteID, payments[0]['id'])
                order = UrlRedirectOrder(url=redirectURL)
                self.running = False
                return order

            except TwistError as exc:
                self.running = False
                raise UnavailableError(
                    "Request got an error: " + str(
                        exc.message) + "and status code = " +
                    str(exc.status_code)) from exc
            except ValueError as error:
                raise UnavailableError("Quote couldn't be checked.") from error
            except InvalidInputError as err:
                self.running = False
                raise InvalidInputError from err
            except requests.exceptions.RequestException as err:
                self.running = False
                raise UnavailableError("Request got a error") from err
            except UnavailableError as err:
                self.running = False
                raise UnavailableError(str(err))
            except Exception as err:
                self.running = False
                raise UnavailableError from err

        return None
