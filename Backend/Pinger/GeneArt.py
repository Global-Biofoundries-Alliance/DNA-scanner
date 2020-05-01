'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
# pylint: disable=broad-except
# pylint: disable=invalid-name
# pylint: disable=no-self-use
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-statements
from datetime import datetime
import re

import requests

from .Entities import AuthenticationError, Currency, InvalidInputError, \
    Message, MessageType, Offer, Order, Price, SequenceInformation, \
    SequenceOffers, UnavailableError, UrlRedirectOrder
from .Pinger import BasePinger, IsRunningError
from .Validator import EntityValidator


class GeneArtClient:
    '''GeneArt client.'''

    def __init__(self, server, validate, status, addToCart, upload, username,
                 token, dnaStrings=True, hqDnaStrings=True, timeout=60):
        '''
        Constructor for a GeneArtClient.

        Takes as input the configuration's parameters
        dnaStrings and hqDnaStrings have per defualt the value True
        '''
        self.server = server
        self.validate = validate
        self.status = status
        self.addToCart = addToCart
        self.upload = upload
        self.username = username
        self.token = token
        self.dnaStrings = dnaStrings
        self.hqDnaStrings = hqDnaStrings
        self.timeout = timeout
        self.validAcc = self.authenticate()

        if not self.validAcc:
            raise AuthenticationError('User Credentials are wrong')

    def destination(self, action):
        '''Defines the destination address for the action defined in the
        parameter.'''
        if action == "validate":
            return self.server + self.validate
        if action == "status":
            return self.server + self.status
        if action == "addToCart":
            return self.server + self.addToCart
        if action == "upload":
            return self.server + self.upload

        return None

    def getAuthPart(self, projectId):
        '''Returns the authentication field which is used in several
        requests.'''
        request = {
            "authentication":
            {"username": self.username,
             "token": self.token
             },
            "projectId": projectId
        }
        return request

    def authenticate(self):
        '''Authentication Operation.

        Checks if the username and password are correct.
        Distinguishes based on the error message.'''

        result = self.statusReview("2019AAAAAX")  # Dummy projectId
        if("errortype" in result.keys() and
           result["errortype"] == "authenticationFailed"):
            return False
        # else:
        return True

    def statusReview(self, projectId):
        '''Review stored project.'''
        request = self.getAuthPart(projectId)
        dest = self.destination("status")
        resp = requests.post(dest, json=request, timeout=self.timeout)
        result = resp.json()
        return result

    def toCart(self, projectId):
        '''Add Project to Cart.'''
        request = self.getAuthPart(projectId)
        dest = self.destination("addToCart")
        resp = requests.post(dest, json=request, timeout=self.timeout)
        result = resp.json()
        return result

    def constUpload(self, listOfSequences, product):
        '''Upload Project with constructs.'''
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H_%M")
        projectname = "ect-" + str(dt_string)
        dest = self.destination("upload")
        constructsList = []
        for construct in listOfSequences:
            sequence = {
                "name": self.generateName(construct["name"]),
                "sequence": construct["sequence"],
                "product": product,
                "comment": "idN: " + construct["idN"] + " , name: " +
                construct["name"]
            }
            constructsList.append(sequence)
        request = {
            "authentication":
            {"username": self.username,
             "token": self.token
             },
            "project": {
                "name": projectname,
                "constructs": constructsList
            }
        }
        resp = requests.post(dest, json=request, timeout=self.timeout)
        result = resp.json()
        return result

    def constUploadMixedProduct(self, listOfSequences):
        '''
        Upload a list sequences with specific types (HQDnaStrings /
        DnaStrings). This creates a Project with given sequences at GeneArt.

        @param listOfSequences
            type [(dict, str)]. The dictionary in every tuple represents a
            sequence. The string in every tuples
            represents the product type, which tells if HQ or not HQDnaString.
        '''
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H_%M")
        projectname = "ect-" + str(dt_string)
        dest = self.destination("upload")

        # Create list of Constructs
        constructsList = []
        for (construct, product) in listOfSequences:
            sequence = {
                "name": self.generateName(construct["name"]),
                "sequence": construct["sequence"],
                "product": product,
                "comment": "idN: " + construct["idN"] + " , name: "
                + construct["name"]
            }
            constructsList.append(sequence)

        # Put all together to the full requests
        request = {
            "authentication":
            {"username": self.username,
             "token": self.token
             },
            "project": {
                "name": projectname,
                "constructs": constructsList
            }
        }

        # Create Request
        resp = requests.post(dest, json=request, timeout=self.timeout)

        # Return result
        result = resp.json()
        return result

    def projectValidate(self, listOfSequences, product):
        '''Validate Project.'''
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H_%M")
        projectname = "project-" + str(dt_string)
        dest = self.destination("validate")
        constructsList = []
        for construct in listOfSequences:
            sequence = {
                "name": self.generateName(construct["name"]),
                "sequence": construct["sequence"],
                "product": product,
                "comment": "idN: " + construct["idN"] + " , name: " +
                construct["name"]
            }
            constructsList.append(sequence)
        request = {
            "authentication": {
                "username": self.username,
                "token": self.token
            },
            "project": {
                "name": projectname,
                "constructs": constructsList
            }
        }
        resp = requests.post(dest, json=request, timeout=self.timeout)
        result = resp.json()
        return result

    def generateName(self, prevName):
        '''Name-Generator used to define project name if none is given and
        adjust the given name if it isn't conform the documentation.'''
        if not prevName:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y_%H:%M")
            prevName = "consname-" + str(dt_string)
        else:
            if len(prevName) > 20:
                prevName = prevName[:20]
        clean_consName = re.sub(r'[^.A-z0-9_\-]', "_", prevName)
        return clean_consName


#
#
#
class GeneArt(BasePinger):
    '''The GeneArt Pinger.'''

    # The configuration's parameters
    # dnaStrings and hqDnaStrings have per defualt the value True

    server_default = \
        "https://www.thermofisher.com/order/gene-design-ordering/api"
    validate_default = "/validate/v1"
    status_default = "/status/v1"
    addToCart_default = "/addtocart/v1"
    upload_default = "/upload/v1"
    dnaStrings_default = True
    hqDnaStrings_default = True
    timeout_default = 60
    cartBaseUrl_default = "https://www.thermofisher.com/order/catalog/en/" + \
        "US/direct/lt?cmd=ViewCart&ShoppingCartKey="
    currencies = {"EUR": Currency.EUR, "USD": Currency.USD}

    '''
    Constructor for a GeneArt-Pinger

    Takes as input the log-in parameters.
    '''

    def __init__(self, username, token, server=server_default,
                 validate=validate_default, status=status_default,
                 addToCart=addToCart_default, upload=upload_default,
                 dnaStrings=dnaStrings_default,
                 hqDnaStrings=hqDnaStrings_default, timeout=timeout_default,
                 cartBaseUrl=cartBaseUrl_default):
        super().__init__()
        self.running = False

        self.server = server
        self.validate = validate
        self.status = status
        self.addToCart = addToCart
        self.upload = upload
        self.username = username
        self.token = token
        self.dnaStrings = dnaStrings
        self.hqDnaStrings = hqDnaStrings
        self.timeout = timeout
        self.cartBaseUrl = cartBaseUrl

        try:
            self.client = GeneArtClient(self.server,
                                        self.validate, self.status,
                                        self.addToCart,
                                        self.upload,
                                        self.username, self.token,
                                        self.dnaStrings, self.hqDnaStrings,
                                        self.timeout)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got timeout") from err

        self.offers = []
        self.vendorMessages = []
        self.validator = EntityValidator(raiseError=True)

    def encode_sequence(self, seqInf):
        '''
        Encodes a 'SequenceInformation' object into JSON-Format with fields
        readable by the GeneArtClient.

        Returns the newly created object, if the given input is valid.
        Otherwise raises a 'TypeError'
        '''
        if isinstance(seqInf, SequenceInformation):
            if self.validator.validate(seqInf):
                return {"idN": seqInf.key, "name": seqInf.name,
                        "sequence": seqInf.sequence}
        # else:
        type_name = seqInf.__class__.__name__

        raise InvalidInputError(
            f"Parameter must be of type SequenceInformation but is of "
            f"type '{type_name}'.")

    def authenticate(self):
        '''
        Authenticates the instance

            Returns True if the authentication was successful and False
            otherwise.
        '''

        # Authenticate by calling the corresponding method.
        response = {}

        try:
            response = self.client.authenticate()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got timeout") from err
        except Exception:
            messageText = 'Wrong Credentials'
            return Message(MessageType.WRONG_CREDENTIALS, messageText)

        return response

    def searchOffers(self, seqInf):
        '''
        After:
            isRunning() -> true
            getOffers() -> [SequenceOffer(seqInf[0], self.tempOffer),
                        SequenceOffer(seqInf[1], self.tempOffer), ...
                        SequenceOffer(seqInf[n], self.tempOffer)]
        '''

        # Check pinger is not running
        if self.isRunning():
            raise IsRunningError(
                "Pinger is currently running and can not perform a other "
                "action")

        try:
            self.running = True
            offers = []  # Empty Offers List
            # Two possible Product Types.
            for product in "dnaStrings", "hqDnaStrings":
                try:
                    response = self.projectValidate(seqInf, product)
                except requests.exceptions.RequestException as err:
                    # If request timeout
                    self.running = False
                    raise UnavailableError from err

                count = 0  # Count the sequences
                for seq in seqInf:
                    # See if the API accepted the sequence
                    accepted = response["constructs"][count]["accepted"]
                    # If the sequence was accepted
                    if accepted:
                        messageText = product + "_" + "accepted"
                        message = Message(MessageType.INFO, messageText)
                        turnOverTime = response["constructs"][count][
                            "eComInfo"]["productionDaysEstimated"]
                        currencycode = response["constructs"][count][
                            "eComInfo"]["currencyIsoCode"]
                        cost = response["constructs"][count][
                            "eComInfo"]["lineItems"][0][
                                "customerSpecificPrice"]
                        # If the currencycode is known.
                        if currencycode in list(self.currencies.keys()):
                            price = Price(
                                amount=cost,
                                currency=self.currencies[currencycode],
                                customerSpecific=True)
                        # If the currencycode is unknown.
                        else:
                            price = Price(
                                amount=cost, currency=Currency.UNKNOWN,
                                customerSpecific=True)
                    # If the sequence was rejected
                    else:
                        turnOverTime = -1
                        price = Price()
                        # If there was only one reason why it got rejected.
                        # Identify the reason and costumize the message text.
                        if len(response["constructs"][count]["reasons"]) == 1:
                            reason = response["constructs"][count][
                                "reasons"][0]
                            messageText = product + "_" + \
                                "rejected_" + str(reason) + "."
                            if reason == "length":
                                message = Message(
                                    MessageType.INVALID_LENGTH, messageText)
                            elif reason == "homology":
                                message = Message(
                                    MessageType.HOMOLOGY, messageText)
                            elif reason == "problems":
                                message = Message(
                                    MessageType.INVALID_LENGTH, messageText)
                            else:
                                message = Message(
                                    MessageType.SYNTHESIS_ERROR, messageText)
                        # If there was were several reasons why it got
                        # rejected. Costumize the message text.
                        else:
                            messageText = product + "_" + "rejected_"
                            for reason in response["constructs"][count][
                                    "reasons"]:
                                messageText = messageText + str(reason) + "."
                            message = Message(
                                MessageType.SYNTHESIS_ERROR, messageText)

                    currentOffer = Offer(
                        price=price, turnovertime=turnOverTime,
                        messages=[message])
                    currentOffer.isHq = product == "hqDnaStrings"
                    seqOffer = SequenceOffers(seq, [currentOffer])
                    offers.append(seqOffer)
                    count = count + 1
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

    def constUpload(self, seqInf, product):
        '''
        Upload Project with constructs

        Takes as input a list of 'SequenceInformation' objects and the desired
        product type

        (The parameter "product" can only have the value: 'dnaStrings' or
        'hqDnaStrings')

            Returns the API-Response
        '''
        # Sequences in JSON-Format with fields readable by the GeneArtClient.
        # At first is empty.
        gaSequences = []
        for s in seqInf:
            # Encode each element in JSON-Format with fields readable by the
            # GeneArtClient and add it to the list.
            seq = self.encode_sequence(s)
            gaSequences.append(seq)
        # Upload the construct by calling the corresponding method.
        response = self.client.constUpload(gaSequences, product)
        return response

    def constUploadMixedProduct(self, seqInf):
        '''
        Upload a list sequences with specific types (HQDnaStrings /
        DnaStrings).
            1.  Encode every SequenceInformation into the API format
            2.  Construct Upload via GeneArtClient to create a project with
                    the given sequences.

        @param seqInf
            type [(Entities.SequenceInformation, str)]. The
            SequenceInformations in every tuple represents the Sequences.
            The string in every tuples represents the product type, which
            tells if HQ or not HQDnaString.
        '''
        # Sequences in JSON-Format with fields readable by the GeneArtClient.
        # At first is empty.
        gaSequences = []
        for (s, product) in seqInf:
            # Encode each element in JSON-Format with fields readable by the
            # GeneArtClient and add it to the list.
            seq = self.encode_sequence(s)
            gaSequences.append((seq, product))
        # Upload the construct by calling the corresponding method.
        response = self.client.constUploadMixedProduct(gaSequences)
        return response

    def projectValidate(self, seqInf, product):
        '''
        Validate Project

        Takes as input a list of 'SequenceInformation' objects and the desired
        product type (The parameter "product" can only have the value:
        'dnaStrings' or 'hqDnaStrings')

        Returns the API-Response
        '''
        # Sequences in JSON-Format with fields readable by the GeneArtClient.
        # At first is empty.
        gaSequences = []
        for s in seqInf:
            # Encode each element in JSON-Format with fields readable by the
            # GeneArtClient and add it to the list.
            seq = self.encode_sequence(s)
            gaSequences.append(seq)
        # Validate the project by calling the corresponding method.
        response = self.client.projectValidate(gaSequences, product)
        return response

    def isRunning(self):
        '''Checks if the Pinger is Running.'''
        return self.running

    def getOffers(self):
        '''Returns List with a  SequenceOffer for every sequence in last
        searchOffers(seqInf)-call.

        Every SequenceOffer contains the same offers. Default 1 see
        self.tempOffer and self.offers.'''
        return self.offers

    def toCart(self, projectId):
        '''
        Add to Cart
            Takes as parameter a projectId
            Returns the API-Response
        '''
        # Add the project to cart by calling the corresponding method.
        try:
            response = self.client.toCart(projectId)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got Timeout") from err

        return response

    def statusReview(self, projectId):
        '''
        Status Review
            Takes as parameter a projectId
            Returns the API-Response
        '''
        # Review the status of the project by calling the corresponding method.
        try:
            response = self.client.statusReview(projectId)
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got timeout") from err

        return response

    def clear(self):
        '''
        Resets the pinger by
            - stop searching -> isRunning() = false
            - resets the offers to a empty list -> getOffers = []
        '''
        self.running = False
        self.offers = []  # Empty Offers List
        self.vendorMessages = []

    def getVendorMessages(self):
        '''
        Returns this vendor's messages

        @result
            Type ArrayOf(str).
            Array of messages populated by the pinger. May be empty.
        '''
        return self.vendorMessages

    def addVendorMessage(self, message):
        '''
        Adds a vendor message to this vendor's message store.

        @result
            Type Message
            The message to be added
        '''
        self.vendorMessages.append(message)

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

        try:
            # List to collect tuples of type (SequenceInformation,
            # product-type)
            offersToBuy = []

            # find offers with id in given offerIds
            for sequenceOffer in self.offers:
                for offer in sequenceOffer.offers:
                    # match
                    if offer.key in offerIds:
                        product = "dnaStrings"
                        # Check if it is hq
                        if offer.isHq:
                            product = "hqDnaStrings"

                        # add to list
                        offersToBuy.append(
                            (sequenceOffer.sequenceInformation, product))

            if len(offersToBuy) != len(offerIds):
                raise InvalidInputError("Some of the offerIds are not found")

            print("Order", len(offersToBuy), "sequences at GeneArt")
            # Upload to a project at geneart
            constructUpload = self.constUploadMixedProduct(offersToBuy)
            order = Order()

            # If not all sequences are in the response?
            if len(constructUpload["project"]["constructs"]) != \
                    len(offersToBuy):
                print("Someone tried to order sequences that are not "
                      "synthesizeable")
                raise InvalidInputError(
                    "The given offers cannot be synthesised")
            # else:

            # Create Cart
            projectId = constructUpload["project"]["projectId"]
            toCartResponse = self.toCart(projectId)

            # Check Cart-Response
            expectedKeys = ["projectId", "cartId"]

            if expectedKeys == list(toCartResponse.keys()):
                order = UrlRedirectOrder(
                    url=self.cartBaseUrl + str(toCartResponse["cartId"]))
            else:
                # Failed to create Cart
                raise UnavailableError("Failed to create toCart request")

            self.running = False

            return order

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
