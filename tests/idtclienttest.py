import unittest
import json
import yaml
from Pinger import IDT, Entities

# Log-In Credentials
with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)


idt_username = cfg['idt']['idt_username']
idt_password = cfg['idt']['idt_password']
client_id = cfg['idt']['client_id']
client_secret = cfg['idt']['client_secret']
scope = cfg['idt']['scope']
token = cfg['idt']['token']


# Test file which can be successfully valideted by the API.
with open('./examples/idt_clienttest_sequence.json') as json_file:
    data = json.load(json_file)

class TestIDTClient(unittest.TestCase):
    name = "IDTClient"
    # The configuration's parameters 
    token_server = "https://eu.idtdna.com/Identityserver/connect/token"
    screening_server = "https://eu.idtdna.com/api/complexities/screengBlockSequences"
    timeout = 60

    # Object of type GeneArtClient used in these tests to communicate with the API.
    idt = IDT.IDTClient(token_server, screening_server, idt_username, idt_password, client_id, client_secret, scope, timeout = timeout)

    # Checks the authentication.
    def test_getToken(self):
        print ("Start test for the method getToken of " + self.name + ".")
        # Give dummy credentials
        username_dummy = "USERNAME"
        password_dummy = "PASSWORD"
        client_id_dummy = "ID"
        client_secret = "SECRET"
        scope = "SCOPE"
        with self.assertRaises(Entities.AuthenticationError): IDT.IDTClient(TestIDTClient.token_server, TestIDTClient.screening_server, username_dummy, password_dummy, client_id, client_secret, scope)
        
        self.assertEqual(32, len(self.idt.token))
        
    # Check the screening method by checking the length of the response parts
    def test_screening(self):
        print ("Start test for the method screening of " + self.name + ".")
        listOfSequences = data
        response = self.idt.screening(listOfSequences)
        # Expected Response Lengths
        self.assertEqual(1, len(response))
        self.assertEqual(2, len(response[0]))
        
if __name__ == '__main__':
    unittest.main()
        
