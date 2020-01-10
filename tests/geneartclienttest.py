import unittest
import json

from Pinger import GeneArtClient

username_real = "YOUR_USERNAME_HERE"
token_real = "YOUR_TOKEN_HERE"


with open('./examples/constValidate_successful.json') as json_file:
    data = json.load(json_file)

class TestGeneArtClient(unittest.TestCase):

    server= "https://www.thermofisher.com/order/gene-design-ordering/api"
    validate = "/validate/v1"
    status = "/status/v1"
    addToCart = "/addtocart/v1"
    upload = "/upload/v1"
    dnaStrings = True
    hqDnaStrings = True
    geneart1 = GeneArtClient.GeneArtClient(server, validate, status, addToCart, upload, username_real, token_real, dnaStrings, hqDnaStrings)
    # Checks the authentication.
    def test_authenticate(self):
        print ("Start test for authentication method")
        # Give dummy username and password
        username_dummy = "USERNAME"
        token_dummy = "TOKEN"
        with self.assertRaises(Exception): GeneArtClient.GeneArtClient(TestGeneArtClient.server, TestGeneArtClient.validate, TestGeneArtClient.status, TestGeneArtClient.addToCart, TestGeneArtClient.upload, username_dummy, token_dummy, TestGeneArtClient.dnaStrings, TestGeneArtClient.hqDnaStrings)
        
        self.assertEqual(True, self.geneArt1.authenticate())
        
    #Check the constValidate method
    def test_constValidate(self):
        print ("Start test for construct Validate method")
        product = "dnaStrings"
        listOfSequences = data
        response = self.geneArt1.constValidate(listOfSequences, product)
        responseKeys = ['name','constructs']
        consKeys = ['name','product','accepted','reasons']
        self.assertEqual(True, responseKeys == list(response.keys()))
        for cons in response['constructs']:
            self.assertEqual(True, consKeys == list(cons.keys()))
            self.assertEqual(True, cons['product'] == 'dnaStrings')
            self.assertEqual(True, cons['accepted'])
            self.assertEqual(True, cons['reasons'] == [])
    
    def test_other(self):
        print ("Start test for the remaining (other) methods")
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
        
        statusResponse = self.geneArt1.statusReview(projectId)
        expectedStatusResponse = {
            "projectId": projectId,
            "status": "draft"
        }
        self.assertEqual(expectedStatusResponse,statusResponse)
        
        toCartResponse = self.geneArt1.toCart(projectId)
        toCartExpectedKeys = ['projectId','cartId']
        self.assertEqual(True, toCartExpectedKeys == list(toCartResponse.keys()))
        cartId = toCartResponse['cartId']
        
        statusResponse2 = self.geneArt1.statusReview(projectId)      
        expectedStatusResponse2 = {
            "projectId": projectId,
            "status": "in the cart",
            "cartId": cartId
        }
        
        self.assertEqual(expectedStatusResponse2,statusResponse2)
        
        
if __name__ == '__main__':
    unittest.main()
