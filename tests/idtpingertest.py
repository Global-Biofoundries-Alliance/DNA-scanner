import unittest
import json
import yaml
from Pinger import IDT

# Log-In Credentials
with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)


idt_username_real = cfg['idt']['idt_username']
idt_password_real = cfg['idt']['idt_password']
client_id_real = cfg['idt']['client_id']
client_secret_real = cfg['idt']['client_secret']
scope_real = cfg['idt']['scope']
token_real = cfg['idt']['token']

# Test file which can be successfully valideted by the API.
with open('./examples/idt_test_sequence.json') as json_file:
    data = json.load(json_file)

class TestIDTPinger(unittest.TestCase):

    name = "IDTPinger"
    # Pinger Object used for theses tests.
    pinger_example = IDT.IDT(idt_username = idt_username_real, idt_password = idt_password_real, client_id = client_id_real, client_secret = client_secret_real, token = token_real)
    
    # Checks the authentication.
    def test_getToken(self):
        getToken_result = self.pinger_example.getToken()
        self.assertEqual(32, len(getToken_result))
        self.assertEqual(True, self.pinger_example.checkToken())
        
        self.pinger_example.token = "DUMMY_TOKEN"
        self.pinger_example.client.token = "DUMMY_TOKEN"
        self.assertEqual(False, self.pinger_example.checkToken())
        self.pinger_example.token = getToken_result


if __name__ == '__main__':
    unittest.main()
