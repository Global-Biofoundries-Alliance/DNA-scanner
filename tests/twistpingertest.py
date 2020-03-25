import unittest
import json
import yaml
import uuid
import datetime
from Pinger import Twist, Entities

# Log-In Credentials
with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.BaseLoader)


email = cfg['twist']['email']
password = cfg['twist']['password']
apitoken = cfg['twist']['apitoken']
eutoken = cfg['twist']['eutoken']
username = cfg['twist']['username']
firstname = cfg['twist']['firstname']
lastname = cfg['twist']['lastname']

# Test file which can be successfully valideted by the API.
with open('./examples/twist_pingertest_sequences.json') as json_file:
    data = json.load(json_file)
example_list = []

# Create a list of 'SequenceInformation' objects where each object is a sequence form the test file.
for seq in data:
    seqInfo = Entities.SequenceInformation(seq["sequence"], seq["name"], seq["key"])
    example_list.append(seqInfo)

    

class TestTwistPinger(unittest.TestCase):
    name = "TwistPinger"
    # The configuration's parameters 
    host = "https://twist-api.twistbioscience-staging.com/"
    timeout = 60
    # Object of type TwistClient used in these tests to communicate with the API.
    twist = Twist.Twist(email, password, apitoken, eutoken, username, firstname, lastname, host = host, timeout = timeout)

        # Check the BasePinger Functions methods.
    def test_pingerFunctions(self):
        print ("Start test for the methods searchOffers, getOffers, order and clear of " + self.name + ".")
        with self.assertRaises(Entities.UnavailableError): Twist.Twist(email, password, apitoken, eutoken, username, firstname, lastname, host = "GG", timeout = 60)
        listOfSequences = example_list

        self.assertEqual(True, self.twist.offers == [])

        # Test searchOffers and getOffers
        with self.assertRaises(Entities.UnavailableError): self.twist.searchOffers([])

        self.twist.searchOffers(listOfSequences)
        offers = self.twist.getOffers()

        self.assertEqual(True, len(offers) == len(listOfSequences))
            # The Second Sequnce is not synthesizable so its price and turnover time must both be set to -1.
        self.assertEqual(Entities.MessageType.SYNTHESIS_ERROR, offers[1].offers[0].messages[0].messageType)
        self.assertEqual(-1, offers[1].offers[0].price.amount)
        self.assertEqual(-1, offers[1].offers[0].turnovertime)

        # Test order
            # Order only synthesizable sequences (In this test: the first, the fifth and the seventh sequence of the input file)
        offersToOrder = [offers[0].offers[0].key, offers[4].offers[0].key, offers[6].offers[0].key]

        with self.assertRaises(Entities.UnavailableError): self.twist.order([])

        order = self.twist.order(offersToOrder)
        print(type(order))
        assert isinstance(order, Entities.UrlRedirectOrder)

        # Test clear
        self.twist.clear()
        self.assertEqual(True, self.twist.getOffers() == [])

if __name__ == '__main__':
    unittest.main()
