import unittest

from Pinger import Entities

#
#   Tests for the following files:
#       Backend/Pinger/Entities.py
#
class TestEntities(unittest.TestCase):

    name = "Entities test"

    #
    #   Desc:   Test the automatic generation of unique ids in the Offer-Entity.
    #
    def test_offer_id_generation(self):
        # Initialize a empty list for keys
        keys = []

        # create n offers and put their keys in the list
        # raise error if a generated key is not unique
        n = 1000
        for i in range(1, n):
            # Create a new offer
            offer = Entities.Offer()
            # assert that key is not in list
            self.assertFalse(offer.key in keys)
            # add key to list
            keys.append(offer.key)

    #
    #   Desc:   Test the automatic generation of unique ids in the SequenceInformation-Entity.
    #
    def test_sequenceinformation_id_generation(self):
        # Initialize a empty list for keys
        keys = []

        # create n ids and put them in the list
        # raise error if a generated key is not unique
        n = 1000
        for i in range(1, n):
            # Create a new key
            key = Entities.SequenceInformation.generateId()
            # assert that key is not in list
            self.assertFalse(key in keys)
            # add key to list
            keys.append(key)

if __name__ == '__main__':
    unittest.main()
