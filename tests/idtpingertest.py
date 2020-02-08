import unittest
import json
import yaml
from Pinger import Pinger, Entities, IDT, Validator

# Test file which can be successfully validated by the API.
with open('./examples/idt_pingertest_sequence.json') as json_file:
    data = json.load(json_file)
example_list = []

# Create a list of 'SequenceInformation' objects where each object is a sequence form the test file.
for seq in data:
    seqInfo = Entities.SequenceInformation(seq["sequence"], seq["name"], seq["key"])
    example_list.append(seqInfo)

# Log-In Credentials
with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)


idt_username_real = cfg['idt']['idt_username']
idt_password_real = cfg['idt']['idt_password']
client_id_real = cfg['idt']['client_id']
client_secret_real = cfg['idt']['client_secret']
scope_real = cfg['idt']['scope']
token_real = cfg['idt']['token']


class TestIDTPinger(unittest.TestCase):

    name = "IDTPinger"
    # Pinger Object used for theses tests.
    pinger_example = IDT.IDT(idt_username = idt_username_real, idt_password = idt_password_real, client_id = client_id_real, client_secret = client_secret_real, token = token_real)
    
    # Checks the getToken method.
    def test_getToken(self):
        print ("Start test for the methods getToken and checkToken of " + self.name + ".")
        getToken_result = self.pinger_example.getToken() # The generated token
        self.assertEqual(32, len(getToken_result)) # The tokens are 32 characters long
        self.assertEqual(True, self.pinger_example.checkToken()) # Check if the token is working
       
        self.pinger_example.token = "DUMMY_TOKEN"
        self.pinger_example.client.token = "DUMMY_TOKEN"
        self.assertEqual(False, self.pinger_example.checkToken()) # Check the invalidity of a dummy token.
        self.pinger_example.token = getToken_result
        self.pinger_example.client.token = getToken_result # After checking change the token to the real token that was previously generated.
    
    # Checks the screening method.
    def test_screening(self):
        print ("Start test for the method screening of " + self.name + ".")
        listOfSequences = example_list
        response = self.pinger_example.screening(listOfSequences)
        
        # Check the response of the API-Server
        self.assertIsInstance(response, list)        
        self.assertEqual(3, len(response))
        self.assertIsInstance(response[0], list)        
        self.assertIsInstance(response[1], list)        
        self.assertIsInstance(response[2], list)        

        self.assertEqual(2, len(response[0]))
        self.assertIsInstance(response[0][0], dict)
        self.assertIsInstance(response[0][1], dict)
        self.assertEqual(True, response[0][0]["IsViolated"])
        self.assertEqual(True, response[0][1]["IsViolated"])

        self.assertEqual(0, len(response[1]))

        self.assertEqual(7, len(response[2]))
        for i in range (7):
            self.assertIsInstance(response[2][i], dict)
            self.assertEqual(True, response[2][i]["IsViolated"])

    # Check the BasePinger Functions methods.
    def test_pingerFunctions(self):
        print ("Start test for the methods searchOffers, getOffers and clear of " + self.name + ".")
        listOfSequences = example_list
        self.assertEqual([], self.pinger_example.getOffers()) # Check if the newly created pinger has an empty list of offers.
        response = self.pinger_example.searchOffers(listOfSequences) # Search offers
        i = 0
        while(self.pinger_example.isRunning()):
            i = i + 1
            if i == 10000000:
                raise RuntimeError('Waiting Error. API is not responding')
        print("Turns waited: " + str(i))
        offers = self.pinger_example.getOffers() # Get the new offers after the search.
        # Check the result if it is as expected.
        self.assertEqual(len(offers), 3)
        for i in range (3):
            Validator.EntityValidator(raiseError=True).validate(offers[i])
            self.assertEqual(offers[i].sequenceInformation.key, listOfSequences[i].key)
            self.assertEqual(offers[i].sequenceInformation.name, listOfSequences[i].name)            
            self.assertEqual(offers[i].sequenceInformation.sequence, listOfSequences[i].sequence)            
            self.assertEqual(1, len(offers[i].offers))
            self.assertEqual(1, len(offers[i].offers[0].messages))

        self.assertEqual(Entities.MessageType.SYNTHESIS_ERROR, offers[0].offers[0].messages[0].messageType)
        self.assertEqual("Example_Name_0_rejected_Overall Repeat.Repeat Length (Fragment).", offers[0].offers[0].messages[0].text)

        self.assertEqual(Entities.MessageType.INFO, offers[1].offers[0].messages[0].messageType)
        self.assertEqual("Example_Name_1_accepted", offers[1].offers[0].messages[0].text)

        self.assertEqual(Entities.MessageType.SYNTHESIS_ERROR, offers[2].offers[0].messages[0].messageType)
        self.assertEqual("Example_Name_2_rejected_Overall Repeat.Repeat Length.Single Repeat Overall Bases.Single Repeat Percentage.Windowed Repeat Percentage.SSA Repeat 3'.SSA Low GC 3'.", offers[2].offers[0].messages[0].text)
        
        self.pinger_example.clear()
        self.assertEqual([], self.pinger_example.getOffers())


if __name__ == '__main__':
    unittest.main()
