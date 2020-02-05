import unittest

from Pinger.Entities import *
from Pinger.Validator import entityValidator as Validator


class TestCompositePinger(unittest.TestCase):

    # Checks the isRunning() method.
    def test_vendorinformation(self):

        # Check Fals for Types that are not part of the Entities
        self.assertFalse(Validator.validate(1))
        self.assertFalse(Validator.validate("test"))

        # Check true for the valid Subject
        subject = VendorInformation(key=1, name="ABC", shortName="abc")
        self.assertTrue(Validator.validate(subject))

        # False if key is not a number
        subject = VendorInformation(key="", name="BCD", shortName="efg")
        self.assertFalse(Validator.validate(subject))

        # False if name is not type str
        subject = VendorInformation(key=1, name=1, shortName="efg")
        self.assertFalse(Validator.validate(subject))

        # False if shortName is not type str
        subject = VendorInformation(key=1, shortName=1, name="efg")
        self.assertFalse(Validator.validate(subject))


if __name__ == '__main__':
    unittest.main()
