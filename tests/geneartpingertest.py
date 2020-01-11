import unittest
import json
from Pinger import Pinger, Entities, GeneArt

# Test file which can be successfully valideted by the API.
with open('./examples/seqinf_geneart.json') as json_file:
    data = json.load(json_file)
example_list = []

# Create a list of 'SequenceInformation' objects where each object is a sequence form the test file.
for seq in data:
    seqInfo = Entities.SequenceInformation(seq["sequence"], seq["name"], seq["key"])
    example_list.append(seqInfo)

# Log-In Credentials
username_real = "YOUR_USERNAME_HERE"
token_real = "YOUR_TOKEN_HERE"
    
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
        with self.assertRaises(Exception): Pinger.GeneArt("USERNAME", "TOKEN")
    
    # Check the projectValidate method by checking the keys and their values returned by the API.    
    def test_projectValidate(self):
        print ("Start test for method construct Validate method of " + self.name + ".")
        product = "dnaStrings"
        listOfSequences = example_list
        response = self.pinger_example.projectValidate(listOfSequences, product)
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
    
    def test_otherMethods(self):
        print ("Start test for the remaining methods of " + self.name + ".")
        # Step 1.
        product = "dnaStrings"
        listOfSequences = example_list
        response = self.pinger_example.constUpload(listOfSequences, product)
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
  
if __name__ == '__main__':
    unittest.main()
