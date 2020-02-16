import unittest
from itertools import combinations
from sys import maxsize

from Controller.app import app
from Controller.configurator import YmlConfigurator as Configurator
from Controller.session import InMemorySessionManager
from Pinger.Entities import VendorInformation, SequenceInformation, SequenceVendorOffers
from Pinger.Pinger import CompositePinger
from flask import json


class TestController(unittest.TestCase):
    name = "TestController"
    iterations = 100  # How many iterations to perform on iterated tests

    def setUp(self) -> None:
        app.config['TESTING'] = True

        self.config = Configurator("config.yml")

        with app.test_client() as client:
            self.client = client

        self.vendors = []
        for vendor in self.config.vendors:
            self.vendors.append(vendor.key)

    def tearDown(self) -> None:
        pass

    def test_api_prefix(self):
        print(".Testing /api/ subdomain routing")

        resp = self.client.get('/ping')
        self.assertTrue(b'The page requested does not exist' in resp.data)

        resp = self.client.get('/api/ping')
        self.assertTrue(b'The page requested does not exist' not in resp.data)

        resp = self.client.get('/upload')
        self.assertTrue(b'The page requested does not exist' in resp.data)

        resp = self.client.get('/api/upload')
        self.assertTrue(b'The page requested does not exist' not in resp.data)

        resp = self.client.get('/nonexistent')
        self.assertTrue(b'The page requested does not exist' in resp.data)

        resp = self.client.get('/api/nonexistent')
        self.assertTrue(b'The page requested does not exist' not in resp.data)

    def test_upload_endpoint(self) -> None:
        print("Testing /upload endoint")

        for i in range(self.iterations):
            handle = open('../Example_Sequence_Files/difficult_johannes.fasta', 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

    def test_filter_endpoint(self) -> None:
        print("Testing /filter endpoint")

        for i in range(self.iterations):
            # prepare session
            handle = open('../Example_Sequence_Files/difficult_johannes.fasta', 'rb')
            self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})

            response = self.client.post('/api/filter', data='{"banana": "neigh"}')
            self.assertIn("error", response.get_json())

            filter = '{filter: {}}'
            response = self.client.post('/api/filter', data={"filter": filter})
            self.assertIn(b'Invalid filter request: Data must be in JSON format', response.data)

            # test filtering vendors
            for r in range(1, len(self.vendors)):
                for vendorTuple in combinations(self.vendors, r):
                    vendors = list(vendorTuple)
                    filter = {
                        "filter": {"vendors": vendors, "price": [0, 10], "deliveryDays": 50, "preselectByPrice": True, \
                                   "preselectByDeliveryDays": False}}
                    response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
                    self.assertIn(b"filter submission successful", response.data)
                    response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                                     data={'size': 1000, 'offset': 0}).get_json()

                    for res in response_json["result"]:
                        for vendor in res["vendors"]:
                            # Data present implies relevant vendor
                            self.assertTrue(not vendor["offers"] or vendor["key"] in vendors)

                    # test filtering vendors with redundant and invalid ones
                    tainted_vendors = vendors + vendors + [-872150987209, 666, -1]
                    filter = {"filter": {"vendors": tainted_vendors, "price": [0, 10], "deliveryDays": 50,
                                         "preselectByPrice": True, \
                                         "preselectByDeliveryDays": False}}
                    response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
                    self.assertIn(b"filter submission successful", response.data)
                    response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                                     data={'size': 1000, 'offset': 0}).get_json()

                    for res in response_json["result"]:
                        for vendor in res["vendors"]:
                            # Data present implies relevant vendor
                            self.assertTrue(not vendor["offers"] or vendor["key"] in vendors,
                                            "Vendor " + str(vendor["key"]) + " not in " + str(vendors))

            # test filtering by price
            filter = {
                "filter": {"vendors": [0, 1, 2], "price": [0.2, 0.5], "deliveryDays": 50, "preselectByPrice": True, \
                           "preselectByDeliveryDays": False}}
            response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()
            for res in response_json["result"]:
                for vendor in res["vendors"]:
                    for offer in vendor["offers"]:
                        self.assertLessEqual(offer["price"], 0.5)
                        self.assertGreaterEqual(offer["price"], 0.2)

            # test filtering by delivery days
            filter = {"filter": {"vendors": [0, 1, 2], "price": [0, 10], "deliveryDays": 5, "preselectByPrice": True, \
                                 "preselectByDeliveryDays": False}}
            response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()
            for res in response_json["result"]:
                for vendor in res["vendors"]:
                    for offer in vendor["offers"]:
                        self.assertLessEqual(offer["turnoverTime"], 5)

    def test_results_endpoint(self) -> None:
        print("Testing /results endpoint")

        for i in range(self.iterations):
            handle = open('../Example_Sequence_Files/difficult_johannes.fasta', 'rb')
            self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            filter = '{"filter": {"vendors": [1],"price": [0, 10],"deliveryDays": 5,"preselectByPrice": True,"preselectByDeliveryDays": False}}'
            self.client.post('/api/filter', data=filter)
            searchResult = self.client.post('/api/results', content_type='multipart/form-data',
                                            data={'size': 1000, 'offset': 0}).get_json()
            expectedCount = 0
            self.assertIn("size", searchResult.keys())
            self.assertIn("count", searchResult.keys())
            self.assertIn("offset", searchResult.keys())
            self.assertIn("result", searchResult.keys())
            self.assertIn("globalMessage", searchResult.keys())

            for result in searchResult["result"]:
                expectedCount = expectedCount + 1

                self.assertIn("sequenceInformation", result.keys())
                self.assertIn("id", result["sequenceInformation"].keys())
                self.assertIn("name", result["sequenceInformation"].keys())
                self.assertIn("sequence", result["sequenceInformation"].keys())
                self.assertIn("length", result["sequenceInformation"].keys())

                self.assertIn("vendors", result.keys())
                for vendor in result["vendors"]:
                    self.assertIn("key", vendor.keys())
                    self.assertIn("offers", vendor.keys())
                    for offer in vendor["offers"]:
                        self.assertIn("price", offer.keys())
                        self.assertIn("turnoverTime", offer.keys())
                        self.assertIn("offerMessage", offer.keys())
                        # self.assertTrue(offer["offerMessage"])
                        for message in offer["offerMessage"]:
                            self.assertIn("text", message)
                            self.assertIn("messageType", message)

            self.assertEqual(expectedCount, searchResult["count"],
                             "Mismatch between declared and actual sequence count!")

    def test_vendor_endpoint(self) -> None:
        print("Testing /vendors endpoint")

        for i in range(self.iterations):
            resp = self.client.get("/api/vendors")
            vendors = eval(resp.data)
            expectedKey = 0
            for vendor in vendors:
                self.assertIn("name", vendor.keys())
                self.assertIn("shortName", vendor.keys())
                self.assertIn("key", vendor.keys())

                self.assertEqual(vendor["key"], expectedKey)
                expectedKey = expectedKey + 1

    # Tests if search results are consistent between queries;
    # especially in regards of changing filter settings in between.
    def test_result_consistency(self) -> None:
        print("Testing result consistency")

        for i in range(self.iterations):
            # upload file
            handle = open('../Example_Sequence_Files/difficult_johannes.fasta', 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            filter = {"filter": {"vendors": [1, 2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)

            # Test consistency between subsequent query results without filter change
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            response2 = self.client.post('/api/results', content_type='multipart/form-data',
                                         data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response2.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse2 = " + str(response2.data))

            # ...and after identical filter submission
            filter = {"filter": {"vendors": [1, 2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response2 = self.client.post('/api/results', content_type='multipart/form-data',
                                         data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response2.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse2 = " + str(response2.data))

            responseDB = {}
            for r in range(1, len(self.vendors)):
                for vendors in combinations(self.vendors, r):
                    filter = {
                        "filter": {"vendors": [1, 2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                   "preselectByDeliveryDays": False}}
                    filter_response = self.client.post('/api/filter', content_type='application/json',
                                                       data=json.dumps(filter))
                    self.assertIn(b"filter submission successful", filter_response.data)

                    # Test consistency between subsequent query results without filter change
                    response = self.client.post('/api/results', content_type='multipart/form-data',
                                                data={'size': 1000, 'offset': 0})
                    responseDB[vendors] = response.data

            # Try to confuse the server with empty, full and invalid vendor lists
            filter = {"filter": {"vendors": [], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            filter = {"filter": {"vendors": [0, 1, 2], "price": [0, 10], "deliveryDays": 100,
                                 "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            filter = {"filter": {"vendors": [666, -42, 0, 0, 0, 0], "price": [0, 10], "deliveryDays": 100,
                                 "preselectByPrice": True, "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})

            # Test if the response is still consistent to what it was before
            for r in range(1, len(self.vendors)):
                for vendors in combinations(self.vendors, r):
                    filter = {
                        "filter": {"vendors": [1, 2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                   "preselectByDeliveryDays": False}}
                    filter_response = self.client.post('/api/filter', content_type='application/json',
                                                       data=json.dumps(filter))
                    self.assertIn(b"filter submission successful", filter_response.data)

                    # Test consistency between subsequent query results without filter change
                    response = self.client.post('/api/results', content_type='multipart/form-data',
                                                data={'size': 1000, 'offset': 0})
                    self.assertEqual(responseDB[vendors], response.data,
                                     "\n\nresponse:\n" + str(response.data) + "\n\n\nresponse from before:\n" + str(
                                         responseDB[vendors]))

    def test_in_memory_session(self) -> None:
        print("Testing in-memory session management")

        binary_sequences = [SequenceVendorOffers(SequenceInformation("0", "0", "0"), []),
                            SequenceVendorOffers(SequenceInformation("1", "1", "1"), [])]

        # Set up a few sessions and store copies for later reference
        n_sessions = 32
        sessions = []
        for i in range(0, n_sessions):
            session = InMemorySessionManager(i)
            session.storePinger(CompositePinger())
            session.storeSequences([SequenceInformation(str(i), str(i), str(i))])
            session.storeFilter({"vendors": [i], "price": [0, i], "deliveryDays": i,
                                 "preselectByPrice": i % 2 == 0,
                                 "preselectByDeliveryDays": i % 2 == 1})
            seqoffers = []
            shifter = i
            while shifter:
                seqoffers.append(binary_sequences[shifter & 1])
                shifter = shifter >> 1
            session.storeResults(seqoffers)
            session.addSearchedVendors([i])
            session.addSearchedVendors([i - 1, i + 1])

            sessions.append(session)

        # Check if the session manager can correctly tell whether an ID is already taken
        for i in range(0, n_sessions):
            session = InMemorySessionManager(0)
            self.assertTrue(session.hasSession(i))
            self.assertFalse(session.hasSession(n_sessions + i + 1))

        # Check if the values stored in the sessions are still the same as in the reference sessions
        for i in range(0, n_sessions):
            ref_session = sessions[i]
            session = InMemorySessionManager(i)
            self.assertTrue(session.loadPinger())
            self.assertEqual(ref_session.loadPinger(), session.loadPinger())

            self.assertTrue(session.loadSequences())
            self.assertEqual(ref_session.loadSequences(), session.loadSequences())

            self.assertTrue(session.loadFilter())
            self.assertEqual(ref_session.loadFilter(), session.loadFilter())

            self.assertEqual(ref_session.loadResults(), session.loadResults())

            self.assertTrue(session.loadSearchedVendors())
            self.assertEqual(ref_session.loadSearchedVendors(), session.loadSearchedVendors())

        # Check if the values stored in the sessions are actually the ones intended
        for i in range(0, n_sessions):
            session = InMemorySessionManager(i)

            sequence = session.loadSequences()[0]
            self.assertEqual(sequence.key, str(i))
            self.assertEqual(sequence.name, str(i))
            self.assertEqual(sequence.sequence, str(i))


            filter = session.loadFilter()
            self.assertEqual(filter, {"vendors": [i], "price": [0, i], "deliveryDays": i,
                                 "preselectByPrice": i % 2 == 0,
                                 "preselectByDeliveryDays": i % 2 == 1})

            #The offers are a bit more elaborate since it was i encoded in binary
            seqoffers = []
            shifter = i
            while shifter:
                seqoffers.append(binary_sequences[shifter & 1])
                shifter = shifter >> 1
            self.assertEqual(session.loadResults(), seqoffers)

            searchedVendors = session.loadSearchedVendors()
            self.assertIn(i - 1, searchedVendors)
            self.assertIn(i, searchedVendors)
            self.assertIn(i + 1, searchedVendors)

        # Finally, test session freeing
        session = InMemorySessionManager(0)
        session.free()
        for i in range(0, n_sessions):
            self.assertFalse(session.hasSession(i))








if __name__ == '__main__':
    unittest.main()
