'''
(c) Global Biofoundries Alliance 2020

Licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.
'''
import unittest

from Pinger import Entities, Validator

#
#   Tests for the following files:
#       Backend/Pinger/Entities.py
#


class TestEntities(unittest.TestCase):

    name = "Validator test"

    #
    #   Desc:   Check Validation of SequenceVendorOffers
    #
    def test_sequencevendoroffers(self):

        validator = Validator.EntityValidator(printError=True)

        # SequenceInformation has wrong type
        ott = Entities.SequenceVendorOffers(
            sequenceInformation=1, vendorOffers=[])
        self.assertFalse(validator.validate(ott))

        # vendorOffers has wrong type
        ott = Entities.SequenceVendorOffers(sequenceInformation=Entities.SequenceInformation(
            key="1", name="1", sequence="ACTACG"), vendorOffers=1)
        self.assertFalse(validator.validate(ott))

        # vendorOffers has element with wrong type
        ott = Entities.SequenceVendorOffers(sequenceInformation=Entities.SequenceInformation(
            key="1", name="1", sequence="ACTACG"), vendorOffers=[1])
        self.assertFalse(validator.validate(ott))

        # success
        ott = Entities.SequenceVendorOffers(sequenceInformation=Entities.SequenceInformation(key="1", name="1", sequence="ACTACG"), vendorOffers=[
                                            Entities.VendorOffers(vendorInformation=Entities.VendorInformation(key=1, name="1", shortName="1"))])
        self.assertTrue(validator.validate(ott))

    #
    #   Desc:   Check validation of SequenceOffers
    #
    def test_sequenceoffers(self):

        validator = Validator.EntityValidator(printError=True)

        # SequenceInformation has wrong type
        ott = Entities.SequenceOffers(sequenceInformation=1, offers=[])
        self.assertFalse(validator.validate(ott))

        # offers has wrong type
        ott = Entities.SequenceOffers(sequenceInformation=Entities.SequenceInformation(
            key="1", name="1", sequence="ACTACG"), offers=1)
        self.assertFalse(validator.validate(ott))

        # vendorOffers has element with wrong type
        ott = Entities.SequenceOffers(sequenceInformation=Entities.SequenceInformation(
            key="1", name="1", sequence="ACTACG"), offers=[1])
        self.assertFalse(validator.validate(ott))

        # success
        ott = Entities.SequenceOffers(sequenceInformation=Entities.SequenceInformation(
            key="1", name="1", sequence="ACTACG"), offers=[Entities.Offer()])
        self.assertTrue(validator.validate(ott))

    #
    #   Desc:   Check validation of SequenceOffers
    #
    def test_vendoroffers(self):

        validator = Validator.EntityValidator(printError=True)

        # VendorInformation has wrong type
        ott = Entities.VendorOffers(vendorInformation=1, offers=[])
        self.assertFalse(validator.validate(ott))

        # offers has wrong type
        ott = Entities.VendorOffers(vendorInformation=Entities.VendorInformation(
            key=1, name="1", shortName="1"), offers=1)
        self.assertFalse(validator.validate(ott))

        # vendorOffers has element with wrong type
        ott = Entities.VendorOffers(vendorInformation=Entities.VendorInformation(
            key=1, name="1", shortName="1"), offers=[1])
        self.assertFalse(validator.validate(ott))

        # wrong messages type
        ott = Entities.VendorOffers(vendorInformation=Entities.VendorInformation(
            key=1, name="1", shortName="1"), offers=[], messages=1)
        self.assertFalse(validator.validate(ott))

        # wrong message in messages
        ott = Entities.VendorOffers(vendorInformation=Entities.VendorInformation(
            key=1, name="1", shortName="1"), offers=[], messages=[1])
        self.assertFalse(validator.validate(ott))

        # success
        ott = Entities.VendorOffers(vendorInformation=Entities.VendorInformation(
            key=1, name="1", shortName="1"), offers=[Entities.Offer()], messages=[Entities.Message()])
        self.assertTrue(validator.validate(ott))


if __name__ == '__main__':
    unittest.main()
