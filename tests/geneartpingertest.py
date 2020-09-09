import unittest
import json
import yaml
from Pinger import Pinger, Entities, GeneArt, Validator

# Test file which can be successfully valideted by the API.
with open('./examples/seqinf_geneart.json') as json_file:
    data = json.load(json_file)
example_list = []

# Create a list of 'SequenceInformation' objects where each object is a sequence form the test file.
for seq in data:
    seqInfo = Entities.SequenceInformation(seq["sequence"], seq["name"], seq["key"])
    example_list.append(seqInfo)

# Log-In Credentials
with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)
username_real = cfg['geneart']['username']
token_real = cfg['geneart']['token']

    
class TestGeneArtPinger(unittest.TestCase):

    name = "GeneArtPinger"
    # Pinger Object used for theses tests.
    pinger_example = GeneArt.GeneArt(username = username_real, token = token_real)
    
    # Checks the authentication.
    def test_authenticate(self):
        print ("Start test for method authenticate of " + self.name + ".")
        auth_result = self.pinger_example.authenticate()
        self.assertEqual(True, auth_result)
        
        # Give dummy username and token
        with self.assertRaises(Entities.AuthenticationError): GeneArt.GeneArt("USERNAME", "TOKEN")
    
    # Check the projectValidate method by checking the keys and their values returned by the API.    
    def test_projectValidate(self):
        print ("Start test for method projectValidate method of " + self.name + ".")
        product = "dnaStrings"
        listOfSequences = example_list
        response = self.pinger_example.projectValidate(listOfSequences, product)
        # Expected Response Keys
        responseKeys = ['name','constructs']
        # Expected Keys under response['constructs']
        consKeys = ['name','product','accepted','reasons', 'eComInfo']
        self.assertEqual(True, responseKeys == list(response.keys()))
        for cons in response['constructs']:
            # Check the value of each key included in the response['constructs']
            self.assertEqual(True, consKeys == list(cons.keys()))
            self.assertEqual(True, cons['product'] == 'dnaStrings')
            self.assertEqual(True, cons['accepted'])
            self.assertEqual(True, cons['reasons'] == [])
            
    # Test the other methods in the following scenario:
    #   1. Upload a new project (the sequences from the test file are used as constructs). (--> Test 'constUpload')
    #   2. Review the status of the upload from step 1. (--> Test 'statusReview'. "status" must be "draft".)
    #   3. Add the project from step 1. to cart. (--> Test 'toCart')
    #   4. Review the status of the upload from step 1. (--> Test 'statusReview'. "status" must now be "in the cart".)
    
    def test_otherMethods(self):
        print ("Start test for the remaining methods of " + self.name + ".")
        # Step 1.
        product = "dnaStrings"
        listOfSequences = example_list
        response = self.pinger_example.constUpload(listOfSequences, product)
        projectId = response['project']['projectId']
        responseKeys = ['project']
        projectKeys =['projectId','name','constructs']
        consKeys = ['constructId','name','sequence','product','details']
        self.assertEqual(True, responseKeys == list(response.keys()))
        self.assertEqual(True, projectKeys == list(response['project'].keys()))
        for cons in response['project']['constructs']:
            self.assertEqual(True, consKeys == list(cons.keys()))
            self.assertEqual(True, cons['product'] == 'dnaStrings')
        
        # Step 2.
        statusResponse = self.pinger_example.statusReview(projectId)
        expectedStatusResponse = {
            "projectId": projectId,
            "status": "draft"
        }
        self.assertEqual(expectedStatusResponse,statusResponse)
        
        # Step 3.
        toCartResponse = self.pinger_example.toCart(projectId)
        toCartExpectedKeys = ['projectId','cartId']
        self.assertEqual(True, toCartExpectedKeys == list(toCartResponse.keys()))
        cartId = toCartResponse['cartId']
        
        # Step 4.
        statusResponse2 = self.pinger_example.statusReview(projectId)      
        expectedStatusResponse2 = {
            "projectId": projectId,
            "status": "in the cart",
            "cartId": cartId
        }
        self.assertEqual(expectedStatusResponse2,statusResponse2)

    # Check the BasePinger Functions methods.
    def test_pingerFunctions(self):
        print ("Start test for the methods searchOffers and getOffers of " + self.name + ".")

        with self.assertRaises(Entities.InvalidInputError): self.pinger_example.searchOffers([1])

        self.assertEqual([], self.pinger_example.getOffers())
        listOfSequences = example_list
        response = self.pinger_example.searchOffers(listOfSequences)
        i = 0
        while(self.pinger_example.isRunning()):
            i = i + 1
            if i == 10000000:
                raise RuntimeError('Waiting Error. API is not responding')
        print("Turns waited: " + str(i))
        offers = self.pinger_example.getOffers()
        self.assertEqual(len(offers), 4)

        sequenceOffer0 = offers[0]
        Validator.EntityValidator(raiseError=True).validate(sequenceOffer0)
        sequence0 = sequenceOffer0.sequenceInformation
        self.assertEqual(sequence0.key, listOfSequences[0].key)        
        self.assertEqual(sequence0.name, listOfSequences[0].name)
        self.assertEqual(sequence0.sequence, listOfSequences[0].sequence)
        self.assertEqual(len(sequenceOffer0.offers), 1)
        offers0 = sequenceOffer0.offers[0]
        price0 = offers0.price.amount
        self.assertEqual(price0, 182.0)
        messages0 = offers0.messages
        self.assertEqual(len(messages0), 1)
        self.assertEqual(messages0[0].messageType, Entities.MessageType.INFO)
        self.assertEqual(messages0[0].text, "dnaStrings_accepted")
        self.assertEqual(offers0.turnovertime, 6)
        
        sequenceOffer1 = offers[1]
        Validator.EntityValidator(raiseError=True).validate(sequenceOffer1)
        sequence1 = sequenceOffer1.sequenceInformation
        self.assertEqual(sequence1.key, listOfSequences[1].key)        
        self.assertEqual(sequence1.name, listOfSequences[1].name)
        self.assertEqual(sequence1.sequence, listOfSequences[1].sequence)
        self.assertEqual(len(sequenceOffer1.offers), 1)        
        offers1 = sequenceOffer1.offers[0]
        price1 = offers1.price.amount
        self.assertEqual(price1, 182.0)
        messages1 = offers1.messages
        self.assertEqual(len(messages1), 1)
        self.assertEqual(messages1[0].messageType, Entities.MessageType.INFO)
        self.assertEqual(messages1[0].text, "dnaStrings_accepted")
        self.assertEqual(offers1.turnovertime, 6)

        sequenceOffer2 = offers[2]
        Validator.EntityValidator(raiseError=True).validate(sequenceOffer2)
        sequence2 = sequenceOffer2.sequenceInformation
        self.assertEqual(sequence2.key, listOfSequences[0].key)        
        self.assertEqual(sequence2.name, listOfSequences[0].name)
        self.assertEqual(sequence2.sequence, listOfSequences[0].sequence)
        self.assertEqual(len(sequenceOffer2.offers), 1)
        offers2 = sequenceOffer2.offers[0]
        price2 = offers2.price.amount
        self.assertEqual(price2, -1)
        messages2 = offers2.messages
        self.assertEqual(len(messages2), 1)
        self.assertEqual(messages2[0].messageType, Entities.MessageType.HOMOLOGY)
        self.assertEqual(messages2[0].text, "hqDnaStrings_rejected_homology.")
        self.assertEqual(offers2.turnovertime, -1)

        sequenceOffer3 = offers[3]
        Validator.EntityValidator(raiseError=True).validate(sequenceOffer3)
        sequence3 = sequenceOffer3.sequenceInformation
        self.assertEqual(sequence3.key, listOfSequences[1].key)        
        self.assertEqual(sequence3.name, listOfSequences[1].name)
        self.assertEqual(sequence3.sequence, listOfSequences[1].sequence)
        self.assertEqual(len(sequenceOffer3.offers), 1)
        offers3 = sequenceOffer3.offers[0]
        price3 = offers3.price.amount
        self.assertEqual(price3, -1)
        messages3 = offers3.messages
        self.assertEqual(len(messages3), 1)
        self.assertEqual(messages3[0].messageType, Entities.MessageType.HOMOLOGY)
        self.assertEqual(messages3[0].text, "hqDnaStrings_rejected_homology.")
        self.assertEqual(offers3.turnovertime, -1)
    
        #
        # Test the method order
        #

        # Check Success Order with two known and unique Offer-Keys
        offer2order = [sequenceOffer1.offers[0].key, sequenceOffer0.offers[0].key]
        order = self.pinger_example.order(offer2order)
        self.assertEqual(order.orderType, Entities.OrderType.URL_REDIRECT)

        print("")
        print("Here is the redirect URL of the offer. You can open it and login to check it manually.")
        print("Redirect URL: ", order.url)
        print("")

        # Check error when using unknown offerId
        offer2order = [sequenceOffer1.offers[0].key, 12345]
        with self.assertRaises(Entities.InvalidInputError): self.pinger_example.order(offer2order)
        

if __name__ == '__main__':
    unittest.main()
