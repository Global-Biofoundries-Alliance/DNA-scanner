import unittest

from Pinger import Pinger, Entities
from dummy.pinger import DummyPinger
from dummy.pinger import NotAvailablePinger
from dummy.pinger import AlwaysRunningPinger

class TestCompositePinger(unittest.TestCase):

    name = "CompositePinger"

    # Checks the isRunning() method.
    def test_is_running(self):
        print ("--->>> Start test for: " + TestCompositePinger.name + " - isRunning()")
        # Create CompositePinge with 2 registered DummyPinger
        pingerDummy1 = DummyPinger()
        pingerDummy2 = DummyPinger()
        p = Pinger.CompositePinger()
        p.registerVendor(Entities.VendorInformation(name="Dummy", shortName="Dummy", key=1), pingerDummy1)
        p.registerVendor(Entities.VendorInformation(name="Dummy", shortName="Dummy", key=2), pingerDummy2)

        # No Pinger is Running
        pingerDummy1.running = False
        pingerDummy2.running = False
        self.assertFalse(p.isRunning())

        # DummyPinger1 is running
        pingerDummy1.running = True
        pingerDummy2.running = False
        self.assertTrue(p.isRunning())

        # DummyPinger2 is running
        pingerDummy1.running = False
        pingerDummy2.running = True
        self.assertTrue(p.isRunning())

        # Both DummyPinger are running
        pingerDummy1.running = True
        pingerDummy2.running = True
        self.assertTrue(p.isRunning())

    # Check the getVendor method
    def test_get_vendor(self):
        print ("--->>> Start test for: " + TestCompositePinger.name + " - getVendor")
        # Create Dummy Pinger
        pingerDummy1 = DummyPinger()
        pingerDummy2 = DummyPinger()

        # Without registered vendor/vendorpinger
        p = Pinger.CompositePinger()
        self.assertEqual(0, len(p.getVendors()))

        # With 1 registered vendor
        p.registerVendor(Entities.VendorInformation(name="Dummy", shortName="Dummy", key=1), pingerDummy1)
        self.assertEqual(1, len(p.getVendors()))
        vendor = p.getVendors()[0]
        self.assertEqual(vendor.name, "Dummy")
        self.assertEqual(vendor.shortName, "Dummy")
        self.assertEqual(vendor.key, 1)

        # with 2 registered vendor
        p.registerVendor(Entities.VendorInformation(name="Dummy", shortName="Dummy", key=2), pingerDummy2)
        self.assertEqual(2, len(p.getVendors()))
        vendor = p.getVendors()[1]
        self.assertEqual(vendor.name, "Dummy")
        self.assertEqual(vendor.shortName, "Dummy")
        self.assertEqual(vendor.key, 2)

        # Test with duplicate key. Old one should be replaced with the new one
        p.registerVendor(Entities.VendorInformation(name="DummyDuplicate", shortName="DummyDuplicate", key=2), pingerDummy2)
        self.assertEqual(2, len(p.getVendors()))
        vendor = p.getVendors()[1]
        self.assertEqual(vendor.name, "DummyDuplicate")
        self.assertEqual(vendor.shortName, "DummyDuplicate")
        self.assertEqual(vendor.key, 2)


    # Checks the getorders method
    def test_getorders(self):
        print ("--->>> Start test for: " + TestCompositePinger.name + " - getOrders")

        # Intitialize Pinger and DummyPinger
        pingerDummy1 = DummyPinger()
        pingerDummy2 = DummyPinger()
        p = Pinger.CompositePinger()

        # Without search it should return a empty list
        self.assertEqual(0, len(p.getOffers()))
        self.assertFalse(p.isRunning())

        # Start search with 1 Sequence and without vendors
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1")])
        self.assertEqual(1, len(p.getOffers()))
        self.assertEqual(0, len(p.getOffers()[0].vendorOffers))

        # search with 2 sequences and 1 vendor
        p.registerVendor(Entities.VendorInformation(name="Dummy", shortName="Dummy", key=1), pingerDummy1)
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1"),
                        Entities.SequenceInformation("ACTG", "TestSequence", "ts2")])
        self.assertEqual(2, len(p.getOffers()))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers[0].offers))

        # Create a correct order
        order = p.order(vendor = 1, offerIds = [p.getOffers()[0].vendorOffers[0].offers[0].key])
        self.assertEqual(Entities.OrderType.NOT_SUPPORTED, order.getType())

        # search with 1 sequence and 2 vendors
        p.registerVendor(Entities.VendorInformation(name="Dummy", shortName="Dummy", key=2), pingerDummy2)
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1")])
        self.assertEqual(1, len(p.getOffers()))
        self.assertEqual(2, len(p.getOffers()[0].vendorOffers))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers[0].offers))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers[1].offers))

        # Filter Vendor 1
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1")], vendors=[1])
        self.assertEqual(1, len(p.getOffers()))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers))
        self.assertEqual(1, p.getOffers()[0].vendorOffers[0].vendorInformation.key)
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers[0].offers))

        # Filter Vendor 2
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1")], vendors=[2])
        self.assertEqual(1, len(p.getOffers()))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers))
        self.assertEqual(2, p.getOffers()[0].vendorOffers[0].vendorInformation.key)
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers[0].offers))

        # search with 2 sequences, 1 vendor with orders and 1 vendor without orders
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1"),
                        Entities.SequenceInformation("ACTG", "TestSequence", "ts2")])
        pingerDummy2.offers = []
        self.assertEqual(2, len(p.getOffers()))
        self.assertEqual(2, len(p.getOffers()[0].vendorOffers))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers[0].offers))
        self.assertEqual(0, len(p.getOffers()[0].vendorOffers[1].offers))

        # Test that CompositePinger ignores output of a VendorPinger, if invalid
        pingerDummy1.offers = [1,2,3]
        self.assertEqual(2, len(p.getOffers()))
        self.assertEqual(1, len(p.getOffers()[0].vendorOffers))


    #
    #   Desc:   Test the following szenarios:
    #           -   VendorPinger are temporary Unavailable
    #           -   Try to search while Pinger is running
    #
    def testVendorOffers(self):
        # Define Sequences for searchOffers call
        sequences = [
                Entities.SequenceInformation("ACTG", "TestSequence", "ts1")
            ]

        # Define CompositePinger (Object to test)
        p = Pinger.CompositePinger()

        # Pinger with success response
        successPinger = DummyPinger()
        p.registerVendor(Entities.VendorInformation(name="DummySuccess", shortName="DummySucc", key=1), successPinger)

        p.searchOffers(sequences)
        res = p.getOffers()
        # 1 Sequence ...
        self.assertEqual(1, len(res))
        #   with 1 vendor ...
        self.assertEqual(1, len(res[0].vendorOffers))
        #       with 1 offer
        self.assertEqual(1, len(res[0].vendorOffers[0].offers))
        #       and 0 messages
        self.assertEqual(0, len(res[0].vendorOffers[0].messages))

        # register Pinger who is unavailable
        unavailablePinger = NotAvailablePinger()
        p.registerVendor(Entities.VendorInformation(name="DummyNotAvailable", shortName="DummyNA", key=2), unavailablePinger)

        p.searchOffers(sequences)
        res = p.getOffers()
        # 1 Sequence ...
        self.assertEqual(1, len(res))
        #   with 2 vendor ...
        self.assertEqual(2, len(res[0].vendorOffers))

        # 1 vendor ...
        #       with 1 offer
        self.assertEqual(1, len(res[0].vendorOffers[0].offers))
        #       and 0 messages
        self.assertEqual(0, len(res[0].vendorOffers[0].messages))

        # 1 vendor ...
        #       with 0 offer
        self.assertEqual(1, len(res[0].vendorOffers[0].offers))
        #       and 1 messages
        self.assertEqual(1, len(res[0].vendorOffers[1].messages))
        self.assertEqual(Entities.MessageType.API_CURRENTLY_UNAVAILABLE, res[0].vendorOffers[1].messages[0].messageType)
        
        # register Pinger who is always running
        runningPinger = AlwaysRunningPinger()
        p.registerVendor(Entities.VendorInformation(name="DummyRunning", shortName="DummyRunning", key=3), runningPinger)

        # Expect IsRunningError
        with self.assertRaises(Entities.IsRunningError): p.searchOffers(sequences)

    #
    #   Desc:   Test the following scenarios:
    #           -   Try to search with different keys with equal keys
    #
    def testDuplicatedSequences(self):
        # Define Sequences for searchOffers call
        sequences = [
                Entities.SequenceInformation("ACTG", "TestSequence", "ts1"),
                Entities.SequenceInformation("ACTG2", "TestSequence2", "ts1")
            ]

        # Define CompositePinger (Object to test)
        p = Pinger.CompositePinger()

        # Pinger with success response
        successPinger = DummyPinger()
        p.registerVendor(Entities.VendorInformation(name="DummySuccess", shortName="DummySucc", key=1), successPinger)

        # Expect error because auf duplicated keys of sequences
        with self.assertRaises(Entities.InvalidInputError): p.searchOffers(sequences)

if __name__ == '__main__':
    unittest.main()
