import unittest

from Pinger import Pinger, Entities


class TestCompositePinger(unittest.TestCase):

    name = "CompositePinger"

    # Checks the isRunning() method.
    def test_is_running(self):
        print ("Start test for: " + TestCompositePinger.name + " - isRunning()")
        # Create CompositePinge with 2 registered DummyPinger
        pingerDummy1 = Pinger.DummyPinger()
        pingerDummy2 = Pinger.DummyPinger()
        p = Pinger.CompositePinger()
        p.registerVendor(Entities.VendorInformation("Dummy", "Dummy", "D1"), pingerDummy1)
        p.registerVendor(Entities.VendorInformation("Dummy", "Dummy", "D2"), pingerDummy2)

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
        print ("Start test for: " + TestCompositePinger.name + " - getVendor")
        # Create Dummy Pinger
        pingerDummy1 = Pinger.DummyPinger()
        pingerDummy2 = Pinger.DummyPinger()

        # Without registered vendor/vendorpinger
        p = Pinger.CompositePinger()
        self.assertEqual(0, len(p.getVendors()))

        # With 1 registered vendor
        p.registerVendor(Entities.VendorInformation("Dummy", "Dummy", "D1"), pingerDummy1)
        self.assertEqual(1, len(p.getVendors()))
        vendor = p.getVendors()[0]
        self.assertEqual(vendor.name, "Dummy")
        self.assertEqual(vendor.shortName, "Dummy")
        self.assertEqual(vendor.key, "D1")

        # with 2 registered vendor
        p.registerVendor(Entities.VendorInformation("Dummy", "Dummy", "D2"), pingerDummy2)
        self.assertEqual(2, len(p.getVendors()))
        vendor = p.getVendors()[1]
        self.assertEqual(vendor.name, "Dummy")
        self.assertEqual(vendor.shortName, "Dummy")
        self.assertEqual(vendor.key, "D2")

        # TODO Test with duplicate of keys

    # Checks the getorders method
    def test_getorders(self):
        print ("Start test for: " + TestCompositePinger.name + " - getVendors")

        # Intitialize Pinger and DummyPinger
        pingerDummy1 = Pinger.DummyPinger()
        pingerDummy2 = Pinger.DummyPinger()
        p = Pinger.CompositePinger()

        # Start search with 1 Sequence and without vendors
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1")])
        self.assertEqual(1, len(p.getOffers()))
        self.assertEqual(0, len(p.getOffers()[0].offers))

        # search with 2 sequences and 1 vendor
        p.registerVendor(Entities.VendorInformation("Dummy", "Dummy", "D1"), pingerDummy1)
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1"),
                        Entities.SequenceInformation("ACTG", "TestSequence", "ts2")])
        self.assertEqual(2, len(p.getOffers()))
        self.assertEqual(1, len(p.getOffers()[0].offers))
        self.assertEqual(1, len(p.getOffers()[1].offers))

        # search with 1 sequence and 2 vendors
        p.registerVendor(Entities.VendorInformation("Dummy", "Dummy", "D2"), pingerDummy2)
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1")])
        self.assertEqual(1, len(p.getOffers()))
        self.assertEqual(2, len(p.getOffers()[0].offers))

        # search with 2 sequences, 1 vendor with orders and 1 vendor without orders
        p.searchOffers([Entities.SequenceInformation("ACTG", "TestSequence", "ts1"),
                        Entities.SequenceInformation("ACTG", "TestSequence", "ts2")])
        pingerDummy2.offers = []
        self.assertEqual(2, len(p.getOffers()))
        self.assertEqual(1, len(p.getOffers()[0].offers))
        self.assertEqual(1, len(p.getOffers()[1].offers))

if __name__ == '__main__':
    unittest.main()
