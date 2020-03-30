import requests
from .Pinger import *
from .Validator import *
import json
import uuid
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

class IDTClient: 
    # Constructor for a IDTClient ()
    # Takes as input the configuration's parameters 
    def __init__(self, token_server, screening_server, idt_username, idt_password, client_id, client_secret, shared_secret, scope, token = "YOUR_TOKEN", timeout = 60):
        self.token_server = token_server
        self.screening_server = screening_server
        self.idt_username = idt_username
        self.idt_password = idt_password
        self.client_id = client_id
        self.client_secret = client_secret
        self.shared_secret = shared_secret
        self.token = token
        self.scope = scope
        self.timeout = timeout
        if(self.token == "YOUR_TOKEN"):
            self.token = self.getToken()
        else:
            if(self.checkToken() == "False"):
                self.token = self.getToken()
           
    # This method is used to check if the access is still valid.
    # The token expires in one hour.
    def checkToken(self):
        exampleList = [{"Name": "ExampleSeq", "Sequence": "ATCG"}]
        response = requests.post(self.screening_server,
                  headers={'Authorization': 'Bearer {}'.format(self.token), 
                  'Content-Type': 'application/json; charset=utf-8'}, 
                  json=exampleList, 
                  timeout = self.timeout)
        if(type(response.json()) != list and response.json()["Message"] == "Authorization has been denied for this request."):
            return False
        else:
            return True

    # This method is used to generate an access token from the API. This token is later used to access the other endpoints this API offers.
    # The token expires in one hour.
    def getToken(self):
        data = {'grant_type': 'password', 'username': self.idt_username, 'password': self.idt_password, 'scope': self.scope}
        r = requests.post(self.token_server, data, auth=requests.auth.HTTPBasicAuth(self.client_id, self.client_secret), timeout = self.timeout)
        if(not('access_token' in r.json())):
            raise AuthenticationError("Access token could not be generated. Check your credentials.")
        access_token = r.json()['access_token']
        return access_token
        
    # This method takes as input a listOfSequences and it is used to send a HTTP-Request to the API endpoint to test its complexity. 
    def screening(self, listOfSequences):
        constructsList = []
        for construct in listOfSequences:
            sequence = {
                "Name": construct["name"],
                "Sequence": construct["sequence"],
              }
            constructsList.append(sequence)
        resp = requests.post(self.screening_server,
                  headers={'Authorization': 'Bearer {}'.format(self.token), 
                  'Content-Type': 'application/json; charset=utf-8'}, 
                  json=constructsList, 
                  timeout = self.timeout)
        result = resp.json()
        return result

    # This method takes as input a listOfSequences and it is used to send a SOAP-Request to the API endpoint and complete an order.
    def postorder(self, listOfSequences):

        names = [x["name"] for x in listOfSequences]
        sequences = [x["sequence"] for x in listOfSequences]

        constructsList = list(zip(names, sequences))
        header = u"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:idt="http://www.idtdna.com/">
	<soapenv:Body>
		<idt:PostPurchaseOrder>
			<PurchaseOrder xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://schemas.modhul.com/cXML/1.2.008/OrderRequest" payloadID=""" + '"' + str(uuid.uuid4()) + '"' + u""" timestamp=""" + '"' + str(datetime.now(timezone.utc).isoformat()) + '"' + u""">
				<Header>
					<From>
						<Credential domain="GBADnaScanner">
							<Identity>DNAScannerClient</Identity>
						</Credential>
					</From>
					<To>
						<Credential domain="IDTDNA.com">
							<Identity>IDT</Identity>
						</Credential>
					</To>
					<Sender>
						<Credential domain=""" + '"' + self.idt_username + '"' + u""">
							<Identity>""" + self.client_id + u"""</Identity>
							<SharedSecret>""" + self.shared_secret + u"""</SharedSecret>
						</Credential>
					</Sender>
				</Header>
				<Request>
					<OrderRequest>
						<OrderRequestHeader orderID="21603">
							<ShipTo>
								<Address isoCountryCode="US">
									<Name>My Organization</Name>
									<PostalAddress name="My Organization">
										<DeliverTo>Mary Smith</DeliverTo>
										<Street>1234 Elm St</Street>
										<Street>220, Main Lab</Street>
										<City>Middletown</City>
										<State>Iowa</State>
										<PostalCode>50222</PostalCode>
										<Country isoCountryCode="US">US</Country>
									</PostalAddress>
									<Email name="">mary.smith@myorganization.com</Email>
									<Phone>
										<TelephoneNumber>
											<CountryCode/>
											<Number>(319) 904-8222</Number>
										</TelephoneNumber>
									</Phone>
								</Address>
							</ShipTo>
							<BillTo>
								<Address isoCountryCode="USA">
									<Name>My Organization</Name>
									<PostalAddress name="">
										<Street>999 Oak St</Street>
										<Street>Accounts Payable</Street>
										<City>Middletown</City>
										<State>IA</State>
										<PostalCode>50222</PostalCode>
										<Country isoCountryCode="USA">USA</Country>
									</PostalAddress>
									<Email name="">ap@myorganization.com</Email>
									<Phone>
										<TelephoneNumber>
											<CountryCode/>
											<Number>(319) 652-0322</Number>
										</TelephoneNumber>
									</Phone>
								</Address>
							</BillTo>
						</OrderRequestHeader>"""
        for construct in constructsList:
            seqPart = "\n" + u"""						<ItemOut quantity="1">
							<ItemDetail>
								<Extrinsic>
									<GBlockSpecification>
										<Name>""" + construct[0] + u"""</Name>
										<SequenceToManufacture>""" + construct[1] + u"""</SequenceToManufacture>
										<TermsOfUseDisclosure>
											<IsToxin>false</IsToxin>
											<ToxinDescription>Describe toxin here. </ToxinDescription>
											<IsOriginatedFromPlantOrAnimalPathogen>false</IsOriginatedFromPlantOrAnimalPathogen>
											<PlantOrAnimalPathogenDescription>Describe pathogen here. </PlantOrAnimalPathogenDescription>
											<IsInfectious>false</IsInfectious>
											<InfectiousDescription>Describe infectious info here. </InfectiousDescription>
											<IsEtiologicAgent>false</IsEtiologicAgent>
											<EtiologicAgentDescription>Describe etiologic agent here. </EtiologicAgentDescription>
											<InterferesWithBacterialHost>false</InterferesWithBacterialHost>
											<BacterialHostInterferenceDescription>Describe bacterial interference here.</BacterialHostInterferenceDescription>
											<Signature>Mary Smith</Signature>
										</TermsOfUseDisclosure>
										<Services/>
									</GBlockSpecification>
								</Extrinsic>
							</ItemDetail>
						</ItemOut>"""
            header = header + seqPart
        footer = u"""					</OrderRequest>
				</Request>
			</PurchaseOrder>
		</idt:PostPurchaseOrder>
	</soapenv:Body>
</soapenv:Envelope>"""
        request = header + "\n" + footer
        print(request)
        encoded_request = request.encode('utf-8')

        headers = {"Content-Type": "text/xml; charset=UTF-8",
           "SOAPAction": "http://www.idtdna.com/PostPurchaseOrder"}

        resp = requests.post(url="http://stage.idtdna.com/orderintegration/cxml/service.asmx",
                     headers = headers,
                     data = encoded_request,
                     verify=False)


        result = resp.text
        print(result)
        return result

#
#   The IDT Pinger
#
class IDT(BasePinger):
    # The configuration's parameters 
    token_server_default = "https://eu.idtdna.com/Identityserver/connect/token"
    screening_server_default = "https://eu.idtdna.com/api/complexities/screengBlockSequences"
    token_default = "YOUR_TOKEN"
    scope_default = "test"
    timeout_default = 60
    #
    # Constructur for an IDT-Pinger
    # Takes as input the log-in parameters.
    #
    def __init__(self, idt_username, idt_password, client_id, client_secret, shared_secret, token_server = token_server_default, screening_server = screening_server_default, token = token_default, scope = scope_default, timeout = timeout_default):
        self.running = False
        self.token_server = token_server
        self.screening_server = screening_server
        self.idt_username = idt_username
        self.idt_password = idt_password
        self.client_id = client_id
        self.client_secret = client_secret
        self.shared_secret = shared_secret
        self.scope = scope
        self.timeout = timeout
        self.token = token # Set the token (Token may or may not be valid)
        self.client = IDTClient(self.token_server, 
                      self.screening_server, self.idt_username, self.idt_password,
                      self.client_id, 
                      self.client_secret, self.shared_secret, self.scope, 
                      self.token, self.timeout)
        self.token = self.client.token # Set the token (Token is now valid because it was generated using the client)
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
    
    #
    #   Sends a request to the server to generate a token
    #       Returns the token
    #
    def getToken(self):

        # Authenticate by calling the corresponding method.
        try:
            access_token = self.client.getToken()
        except requests.exceptions.RequestException as err:
            raise UnavailableError("Request got timeout") from err
        except:
            raise AuthenticationError("Wrong Credentials")
        return access_token

    #
    #   Checks if the token is valid.
    #
    #
    def checkToken(self):
        if(self.client.checkToken() == False):
            return False
        else:
            return True
        
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
            response = self.screening(seqInf)
            for i in range(len(seqInf)):
                if len(response[i]) == 0: # Empty List, means there are no problems found
                    messageText = seqInf[i].name + "_" + "accepted"
                    message = Message(MessageType.INFO, messageText)
                if len(response[i]) != 0: # Not an empty List, means there are some problems
                    messageText = seqInf[i].name + "_" + "rejected_"
                    for j in range(len(response[i])):
                        messageText = messageText + response[i][j]["Name"] + "."
                    message = Message(MessageType.SYNTHESIS_ERROR, messageText)
                self.validator.validate(message)           
                seqOffer = SequenceOffers(seqInf[i], [Offer(messages = [message])])
                self.validator.validate(seqOffer)
                offers.append(seqOffer)
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
    def order(self, offerIds):
        
        # Check pinger is not running
        if(self.isRunning()):
            raise IsRunningError("Pinger is currently running and can not perform a other action")
        
        # Check type of offersIds
        if (not isinstance(offerIds, list)):
            raise InvalidInputError("offerIds is not a list")
        for id in offerIds:
            if (not isinstance(id, int)):
                raise InvalidInputError("offerIds contains not-integer value")

        self.running = True

        try:
            # List to collect tuples of type (SequenceInformation)
            offersToBuy = []

            # find offers with id in given offerIds
            for sequenceOffer in self.offers:
                for offer in sequenceOffer.offers:
                    # match
                    if offer.key in offerIds:
                        # add to list
                        offersToBuy.append(sequenceOffer.sequenceInformation)

            if len(offersToBuy) != len(offerIds):
                raise InvalidInputError("Some of the offerIds are not found")
            
            print("Order", len(offersToBuy), "sequences at IDT")
            order = Order(orderType = OrderType.MESSAGE)

            constructsList = []
            for construct in offersToBuy:
                sequence = {
                    "name": construct.name,
                    "sequence": construct.sequence,
                  }
                constructsList.append(sequence)

            orderResult = self.client.postorder(constructsList)
            dom = ET.fromstring(orderResult)
            returntext = dom.find('.//{http://www.idtdna.com/}ReturnText').text
            returncode = dom.find('.//{http://www.idtdna.com/}ReturnCode').text
            ordernumber = dom.find('.//{http://www.idtdna.com/}OrderNumber').text
            
            if(returncode != str(200)):
                raise UnavailableError
            message = "Return Text = {}. Return Code = {}. Order Number = {}.".format(returntext, returncode, ordernumber)

            messageorder = MessageOrder(message = message)
            self.running = False
            return messageorder

        except InvalidInputError as err:
            self.running = False
            raise InvalidInputError from err
        except requests.exceptions.RequestException as err:
            self.running = False
            raise UnavailableError("Request got a error") from err
        except UnavailableError as err:
            self.running = False
            raise UnavailableError from err
        except AttributeError as err:
            self.running = False
            raise UnavailableError("Ordering went wrong.") from err
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
    #   Screening-API
    #       Takes as input a list of 'SequenceInformation' objects
    #       Returns the API-Response     
    #
    def screening(self, seqInf):
        # Sequences in JSON-Format with fields readable by the GeneArtClient. At first is empty.
        idtSequences  = []
        for s in seqInf:
            # Encode each element in JSON-Format with fields readable by the GeneArtClient and add it to the list.
            seq = self.encode_sequence(s)
            idtSequences.append(seq)
        # Validate the project by calling the corresponding method.
        response = self.client.screening(idtSequences)
        return response
        

