import unittest
import json

from Pinger import GeneArt

# Log-In Credentials
username_real = "YOUR_USERNAME_HERE"
token_real = "YOUR_TOKEN_HERE"

# Test file which can be successfully valideted by the API.
with open('./examples/projectValidate_successful.json') as json_file:
    data = json.load(json_file)

class TestGeneArtClient(unittest.TestCase):

    # The configuration's parameters 
    # dnaStrings and hqDnaStrings have per defualt the value True
    server= "https://www.thermofisher.com/order/gene-design-ordering/api"
    validate = "/validate/v1"
    status = "/status/v1"
    addToCart = "/addtocart/v1"
    upload = "/upload/v1"
    dnaStrings = True
    hqDnaStrings = True
    timeout = 60

    # Object of type GeneArtClient used in these tests to communicate with the API.
    geneArt1 = GeneArt.GeneArtClient(server, validate, status, addToCart, upload, username_real, token_real, dnaStrings, hqDnaStrings, 60)

    # Checks the authentication.
    def test_authenticate(self):
        print ("Start test for authentication method")
        # Give dummy username and token
        username_dummy = "USERNAME"
        token_dummy = "TOKEN"
        with self.assertRaises(Exception): GeneArt.GeneArtClient(TestGeneArtClient.server, TestGeneArtClient.validate, TestGeneArtClient.status, TestGeneArtClient.addToCart, TestGeneArtClient.upload, username_dummy, token_dummy, TestGeneArtClient.dnaStrings, TestGeneArtClient.hqDnaStrings, TestGeneArtClient.timeout)
        
        self.assertEqual(True, self.geneArt1.authenticate())
        
    # Check the projectValidate method by checking the keys and their values returned by the API.
    def test_projectValidate(self):
        print ("Start test for construct Validate method")
        product = "dnaStrings"
        listOfSequences = data
        response = self.geneArt1.projectValidate(listOfSequences, product)
        # Expected Response Keys
        responseKeys = ['name','constructs']
        # Expected Keys under response['constructs']
        consKeys = ['name','product','accepted','reasons']
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

    def test_other(self):
        print ("Start test for the remaining (other) methods")
        
        # Step 1.        
        product = "dnaStrings"
        listOfSequences = data
        response = self.geneArt1.constUpload(listOfSequences, product)
        projectId = response['project']['projectId']
        responseKeys = ['project']
        projectKeys =['projectId','name','constructs']
        consKeys = ['constructId','name','sequence','product','comment']
        self.assertEqual(True, responseKeys == list(response.keys()))
        self.assertEqual(True, projectKeys == list(response['project'].keys()))
        for cons in response['project']['constructs']:
            self.assertEqual(True, consKeys == list(cons.keys()))
            self.assertEqual(True, cons['product'] == 'dnaStrings')
        
        # Step 2.
        statusResponse = self.geneArt1.statusReview(projectId)
        expectedStatusResponse = {
            "projectId": projectId,
            "status": "draft"
        }
        self.assertEqual(expectedStatusResponse,statusResponse)
        
        # Step 3.
        toCartResponse = self.geneArt1.toCart(projectId)
        toCartExpectedKeys = ['projectId','cartId']
        self.assertEqual(True, toCartExpectedKeys == list(toCartResponse.keys()))
        cartId = toCartResponse['cartId']
        
        # Step 4.
        statusResponse2 = self.geneArt1.statusReview(projectId)      
        expectedStatusResponse2 = {
            "projectId": projectId,
            "status": "in the cart",
            "cartId": cartId
        }
        self.assertEqual(expectedStatusResponse2,statusResponse2)
        
        
if __name__ == '__main__':
    unittest.main()
