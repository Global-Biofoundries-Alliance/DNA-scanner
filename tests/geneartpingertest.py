import unittest
import json
from Pinger import Pinger, Entities

with open('./examples/constValidate_successful.json') as json_file:
    data = json.load(json_file)

example_list = []

for seq in data:
    seqInfo = Entities.SequenceInformation(seq["sequence"], seq["name"], seq["idN"])
    example_list.append(seqInfo)

username_real = "YOUR_USERNAME_HERE"
token_real = "YOUR_TOKEN_HERE"    
    
class TestGeneArtPinger(unittest.TestCase):

    name = "GeneArtPinger"
    pinger_example = Pinger.GeneArt(username_real, token_real)
    # Checks the isRunning() method.
    def test_authenticate(self):
        print ("Start test for method authenticate of " + TestGeneArtPinger.name + ".")
        # Create CompositePinge with 2 registered DummyPinger
        auth_result = TestGeneArtPinger.pinger_example.authenticate()
        self.assertEqual(True, auth_result)
        
        with self.assertRaises(Exception): Pinger.GeneArt("USERNAME", "TOKEN")
    
    def test_constValidate(self):
        print ("Start test for method construct Validate method of " + TestGeneArtPinger.name + ".")
        product = "dnaStrings"
        listOfSequences = example_list
        response = TestGeneArtPinger.pinger_example.constValidate(listOfSequences, product)
        responseKeys = ['name','constructs']
        consKeys = ['name','product','accepted','reasons']
        self.assertEqual(True, responseKeys == list(response.keys()))
        for cons in response['constructs']:
            self.assertEqual(True, consKeys == list(cons.keys()))
            self.assertEqual(True, cons['product'] == 'dnaStrings')
            self.assertEqual(True, cons['accepted'])
            self.assertEqual(True, cons['reasons'] == [])
            
    def test_otherMethods(self):
        print ("Start test for the remaining methods of " + TestGeneArtPinger.name + ".")
        product = "dnaStrings"
        listOfSequences = example_list
        response = TestGeneArtPinger.pinger_example.constUpload(listOfSequences, product)
        projectId = response['project']['projectId']
        responseKeys = ['project']
        projectKeys =['projectId','name','constructs']
        consKeys = ['constructId','name','sequence','product','comment']
        self.assertEqual(True, responseKeys == list(response.keys()))
        self.assertEqual(True, projectKeys == list(response['project'].keys()))
        for cons in response['project']['constructs']:
            self.assertEqual(True, consKeys == list(cons.keys()))
            self.assertEqual(True, cons['product'] == 'dnaStrings')
        
        statusResponse = TestGeneArtPinger.pinger_example.statusReview(projectId)
        expectedStatusResponse = {
            "projectId": projectId,
            "status": "draft"
        }
        self.assertEqual(expectedStatusResponse,statusResponse)
        
        toCartResponse = TestGeneArtPinger.pinger_example.toCart(projectId)
        toCartExpectedKeys = ['projectId','cartId']
        self.assertEqual(True, toCartExpectedKeys == list(toCartResponse.keys()))
        cartId = toCartResponse['cartId']
        
        statusResponse2 = TestGeneArtPinger.pinger_example.statusReview(projectId)      
        expectedStatusResponse2 = {
            "projectId": projectId,
            "status": "in the cart",
            "cartId": cartId
        }
        
        self.assertEqual(expectedStatusResponse2,statusResponse2)
  
if __name__ == '__main__':
    unittest.main()
