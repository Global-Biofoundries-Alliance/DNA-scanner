import unittest
from itertools import combinations
from sys import maxsize

from Controller.app import app
from Controller.configurator import YmlConfigurator as Configurator
from Controller.session import InMemorySessionManager
from Pinger.Entities import SequenceInformation, SequenceVendorOffers, Currency
from Pinger.Pinger import CompositePinger
from flask import json
from random import random
import random as rand


class TestController(unittest.TestCase):
    name = "TestController"
    iterations = 100  # How many iterations to perform on iterated tests

    def setUp(self) -> None:
        app.config['TESTING'] = True
        self.sequence_path = 'examples/ComponentDefinitionOutput_gl.xml'

        self.config = Configurator("config.yml")

        with app.test_client() as client:
            self.client = client

        self.vendors = []
        for vendor in self.config.vendors:
            self.vendors.append(vendor.key)

    def tearDown(self) -> None:
        pass

    def test_api_prefix(self):
        print("\nTesting /api/ subdomain routing")

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
        print("\nTesting /upload endoint")

        for i in range(self.iterations):
            handle = open(self.sequence_path, 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

    def test_filter_endpoint(self) -> None:
        print("\nTesting /filter endpoint")

        for i in range(self.iterations):
            # prepare session
            handle = open(self.sequence_path, 'rb')
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
                        "filter": {"vendors": vendors, "price": [0, 100], "deliveryDays": 50, "preselectByPrice": True, \
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
                    filter = {"filter": {"vendors": tainted_vendors, "price": [0, 100], "deliveryDays": 50,
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
                "filter": {"vendors": [0, 1, 2], "price": [20, 50], "deliveryDays": 50, "preselectByPrice": True, \
                           "preselectByDeliveryDays": False}}
            response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()
            for res in response_json["result"]:
                for vendor in res["vendors"]:
                    for offer in vendor["offers"]:
                        if (offer["price"] >= 0.0):  # negative values are placeholders and must stay in
                            self.assertLessEqual(offer["price"], 50)
                            self.assertGreaterEqual(offer["price"], 20)

            # test filtering by delivery days
            filter = {"filter": {"vendors": [0, 1, 2], "price": [0, 100], "deliveryDays": 5, "preselectByPrice": True, \
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
        print("\nTesting /results endpoint")

        # Sequence names and IDs that have already occured; Used to ensure unique names IDs
        sequenceNames = []
        sequenceIDs = []

        for i in range(self.iterations):
            handle = open(self.sequence_path, 'rb')
            self.client.post('/api/upload', content_type='multipart/form-data',
                             data={'seqfile': handle, 'prefix': "Zucchini" + str(i)})
            filter = '{"filter": {"vendors": [1],"price": [0, 100],"deliveryDays": 5,"preselectByPrice": True,"preselectByDeliveryDays": False}}'
            self.client.post('/api/filter', data=filter)
            searchResult = self.client.post('/api/results', content_type='multipart/form-data',
                                            data={'size': 1000, 'offset': 0}).get_json()

            self.assertNotIn("error", searchResult, "Results endpoint returned error: " + str(searchResult))

            expectedCount = 0
            self.assertIn("size", searchResult.keys())
            self.assertIn("count", searchResult.keys())
            self.assertIn("offset", searchResult.keys())
            self.assertIn("result", searchResult.keys())
            self.assertIn("globalMessage", searchResult.keys())

            # AdvancedMockPingers are used for testing so there should be warning messages present.
            self.assertTrue(searchResult["globalMessage"])

            for result in searchResult["result"]:
                expectedCount = expectedCount + 1

                self.assertIn("sequenceInformation", result.keys())
                self.assertIn("id", result["sequenceInformation"].keys())
                self.assertIn("name", result["sequenceInformation"].keys())
                self.assertIn("sequence", result["sequenceInformation"].keys())
                self.assertIn("length", result["sequenceInformation"].keys())

                # Test uniqueness of names and IDs
                self.assertNotIn(result["sequenceInformation"]["name"], sequenceNames)
                self.assertNotIn(result["sequenceInformation"]["id"], sequenceIDs)
                sequenceNames.append(result["sequenceInformation"]["name"])
                sequenceNames.append(result["sequenceInformation"]["name"])
                sequenceIDs.append(result["sequenceInformation"]["id"])

                self.assertTrue(result["sequenceInformation"]["name"].startswith(
                    str(result["sequenceInformation"]["id"]) + "_Zucchini" + str(i) + "_"))

                self.assertIn("vendors", result.keys())
                for vendor in result["vendors"]:
                    self.assertIn("key", vendor.keys())
                    self.assertIn("offers", vendor.keys())
                    for offer in vendor["offers"]:
                        self.assertIn("price", offer.keys())
                        self.assertIn("currency", offer.keys())
                        self.assertIn(offer["currency"], ["$", "€", "?"])
                        self.assertIn("turnoverTime", offer.keys())
                        self.assertIn("offerMessage", offer.keys())
                        for message in offer["offerMessage"]:
                            self.assertIn("text", message)
                            self.assertIn("messageType", message)

                self.assertIn("vendorMessage", result.keys())
                messageVendors = []     # tracks the vendors for which messages have already been encountered
                for vendor in result["vendorMessage"]:
                    self.assertIn("vendorKey", vendor.keys)
                    self.assertIn("messages", vendor.keys)
                    self.assertFalse(vendor["vendorKey"] in messageVendors)
                    messageVendors.append(vendor["vendorKey"])


            self.assertEqual(expectedCount, searchResult["count"],
                             "Mismatch between declared and actual sequence count!")

    def test_vendor_endpoint(self) -> None:
        print("\nTesting /vendors endpoint")

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
        print("\nTesting result consistency")

        for i in range(self.iterations):
            # upload file
            handle = open(self.sequence_path, 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            filter = {"filter": {"vendors": [1, 2], "price": [0, 100], "deliveryDays": 100, "preselectByPrice": True,
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
            filter = {"filter": {"vendors": [1, 2], "price": [0, 100], "deliveryDays": 100, "preselectByPrice": True,
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
                        "filter": {"vendors": [1, 2], "price": [0, 100], "deliveryDays": 100, "preselectByPrice": True,
                                   "preselectByDeliveryDays": False}}
                    filter_response = self.client.post('/api/filter', content_type='application/json',
                                                       data=json.dumps(filter))
                    self.assertIn(b"filter submission successful", filter_response.data)

                    # Test consistency between subsequent query results without filter change
                    response = self.client.post('/api/results', content_type='multipart/form-data',
                                                data={'size': 1000, 'offset': 0})
                    responseDB[vendors] = response.data

            # Try to confuse the server with empty, full and invalid vendor lists
            filter = {"filter": {"vendors": [], "price": [0, 100], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            filter = {"filter": {"vendors": [0, 1, 2], "price": [0, 100], "deliveryDays": 100,
                                 "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            filter = {"filter": {"vendors": [666, -42, 0, 0, 0, 0], "price": [0, 100], "deliveryDays": 100,
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
                        "filter": {"vendors": [1, 2], "price": [0, 100], "deliveryDays": 100, "preselectByPrice": True,
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

    def test_sorting(self) -> None:
        print("\nTesting offer sorting")

        for i in range(self.iterations):
            # upload file
            handle = open(self.sequence_path, 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            # test sorting by price
            filter = {
                "filter": {"vendors": [0, 1, 2], "price": [0, 100], "deliveryDays": 100,
                           "preselectByPrice": True,
                           "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)

            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            # selection criteria by precedence
            selector = ("price", "turnoverTime")

            for seqoffer in response_json["result"]:
                # First create a starting condition that will cause a fail and will be overwritten in any sane scenario
                for vendoffers in seqoffer["vendors"]:
                    prev_offer = (0, 0)
                    for offer in vendoffers["offers"]:
                        offer_criteria = (offer[selector[0]] % maxsize, offer[selector[1]] % maxsize)
                        if offer["offerMessage"]:
                            offer_criteria = (maxsize, maxsize)
                        self.assertLessEqual(prev_offer, offer_criteria,
                                             "\n\nSorting failed for: \n" + str(vendoffers["offers"]))
                        prev_offer = offer_criteria

            # Test sorting by delivery days
            filter = {
                "filter": {"vendors": [0, 1, 2], "price": [0, 100], "deliveryDays": 100,
                           "preselectByPrice": False,
                           "preselectByDeliveryDays": True}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            # selection criteria by precedence
            selector = ("turnoverTime", "price")

            for seqoffer in response_json["result"]:
                # First create a starting condition that will cause a fail and will be overwritten in any sane scenario
                for vendoffers in seqoffer["vendors"]:
                    prev_offer = (0, 0)
                    for offer in vendoffers["offers"]:
                        offer_criteria = (offer[selector[0]] % maxsize, offer[selector[1]] % maxsize)
                        if offer["offerMessage"]:
                            offer_criteria = (maxsize, maxsize)
                        self.assertLessEqual(prev_offer, offer_criteria,
                                             "\n\nSorting failed for: \n" + str(vendoffers["offers"]))
                        prev_offer = offer_criteria

    def test_preselection(self) -> None:
        print("\nTesting preselection")

        for i in range(self.iterations):
            # upload file
            handle = open(self.sequence_path, 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            # Test preselection by price
            filter = {
                "filter": {"vendors": self.vendors, "price": [0, 100], "deliveryDays": 100, "preselectByPrice": True,
                           "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for seqoffer in response_json["result"]:
                # First create a starting condition that will cause a fail and will be overwritten in any sane scenario
                best = maxsize - 2
                best_secondary = maxsize - 2
                selected = maxsize - 1
                selected_secondary = maxsize - 1
                first_time = True
                offersPresent = False  # Since these are fuzzing tests there is no guarantee that there will be offers to preselect
                for vendoffers in seqoffer["vendors"]:
                    for offer in vendoffers["offers"]:
                        offersPresent = True
                        if not offer["offerMessage"] and (offer["price"] % maxsize <= best % maxsize or first_time):
                            if offer["price"] % maxsize < best % maxsize or \
                                    offer["turnoverTime"] % maxsize < best_secondary % maxsize or first_time:
                                first_time = False
                                best = offer["price"]
                                best_secondary = offer["turnoverTime"]
                        if offer["selected"]:
                            self.assertEqual(selected,
                                             maxsize - 1)  # If this fails there was probably more than one offer selected
                            selected = offer["price"]
                            selected_secondary = offer["turnoverTime"]

                if offersPresent and selected != maxsize - 1:  # It is possible that nothing is selected due to everything being negative
                    self.assertEqual(selected, best, "Preselection failed for:" + str(seqoffer["vendors"]))
                    self.assertGreaterEqual(selected, 0)
                    self.assertEqual(selected_secondary, best_secondary,
                                     "Preselection failed for:" + str(seqoffer["vendors"]))

            # Test preselection by delivery days
            filter = {
                "filter": {"vendors": [0, 1, 2], "price": [0, 100], "deliveryDays": 100,
                           "preselectByPrice": False,
                           "preselectByDeliveryDays": True}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for seqoffer in response_json["result"]:
                # First create a starting condition that will cause a fail and will be overwritten in any sane scenario
                best = maxsize - 2
                best_secondary = maxsize - 2
                selected = maxsize - 1
                selected_secondary = maxsize - 1
                first_time = True
                offersPresent = False  # Since these are fuzzing tests there is no guarantee that there will be offers to preselect
                for vendoffers in seqoffer["vendors"]:
                    for offer in vendoffers["offers"]:
                        offersPresent = True
                        if not offer["offerMessage"] and (
                                offer["turnoverTime"] % maxsize <= best % maxsize or first_time):
                            if offer["turnoverTime"] % maxsize < best % maxsize or \
                                    offer["price"] % maxsize < best_secondary % maxsize or first_time:
                                best = offer["turnoverTime"]
                                best_secondary = offer["price"]
                        if offer["selected"]:
                            self.assertEqual(selected,
                                             maxsize - 1)  # If this fails there was probably more than one offer selected
                            selected = offer["turnoverTime"]
                            selected_secondary = offer["price"]
                        first_time = False
                if offersPresent and selected != maxsize - 1:  # It is possible that nothing is selected due to everything being negative
                    self.assertEqual(selected, best, "Preselection failed for:" + str(seqoffer["vendors"]))
                    self.assertGreaterEqual(selected, 0)
                    self.assertEqual(selected_secondary, best_secondary,
                                     "Preselection failed for:" + str(seqoffer["vendors"]))

    def test_in_memory_session(self) -> None:
        print("\nTesting in-memory session management")

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

            # The offers are a bit more elaborate since it was i encoded in binary
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

    def testSelectionEndpoint(self) -> None:
        print("\nTesting /select endpoint")

        for iteration in range(self.iterations):
            # upload file
            handle = open(self.sequence_path, 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            # This shouldn't select anything
            filter = {
                "filter": {"vendors": self.vendors, "price": [0, 100], "deliveryDays": 100, "preselectByPrice": False,
                           "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            selection = []
            # Verify that nothing is selected and choose what shall be selected next time at random
            for sequence in response_json["result"]:
                for vendor in sequence["vendors"]:
                    for offer in vendor["offers"]:
                        # Check that the offer was not selected by the dry run
                        self.assertFalse(offer["selected"])
                        # Random selection
                        if random() <= 0.4:
                            selection.append(offer["key"])

            response = self.client.post("/api/select", content_type='application/json',
                                        data=json.dumps({"selection": selection}))
            self.assertIn(b"selection set", response.data)

            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for sequence in response_json["result"]:
                for vendor in sequence["vendors"]:
                    for offer in vendor["offers"]:
                        # An offer should be selected if and only if it was in the selection list
                        self.assertEqual(offer["selected"], offer["key"] in selection)

    def test_available_hosts_endpoint(self):
        print("\nTesting /available_hosts endpoint")
        response_json = self.client.get("/api/available_hosts").get_json()
        self.assertGreater(len(response_json), 0)

    # NOTE: This must not be made into an iterated test as it accesses the BOOST service
    #       which we don't want to overload with requests.
    def test_codon_optimization(self):
        print("\nTesting codon optimization")

        host_list = self.client.get("/api/available_hosts").get_json()
        strategies = ["Random", "Balanced", "MostlyUsed"]

        for strategy in strategies:
            response = self.client.post('/api/codon_optimization', content_type='application/json',
                                        data=json.dumps({'host': rand.choice(host_list), 'strategy': strategy}))
            self.assertIn(b"codon optimization options set", response.data)

            # upload protein sequence file
            handle = open("examples/low_temp_yeast.gb", 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for sequence in response_json["result"]:
                self.assertGreater(sequence["sequenceInformation"]["length"], 0)

    def test_results_endpoint(self) -> None:
        print("\nTesting /order endpoint")

        for i in range(self.iterations):
            handle = open(self.sequence_path, 'rb')
            self.client.post('/api/upload', content_type='multipart/form-data',
                             data={'seqfile': handle, 'prefix': "Zucchini" + str(i)})
            filter = '{"filter": {"vendors": [1],"price": [0, 100],"deliveryDays": 5,"preselectByPrice": True,"preselectByDeliveryDays": False}}'
            self.client.post('/api/filter', data=filter)
            searchResult = self.client.post('/api/results', content_type='multipart/form-data',
                                            data={'size': 1000, 'offset': 0}).get_json()

            self.assertNotIn("error", searchResult, "Results endpoint returned error: " + str(searchResult))

            offerkeys = []

            for result in searchResult["result"]:
                for vendor in result["vendors"]:
                    for offer in vendor["offers"]:
                        offerkeys.append(offer["key"])

            orderkeys = rand.sample(offerkeys, rand.randint(0, len(offerkeys) - 1))
            response = self.client.post("/api/order", content_type="application/json",
                                        data=json.dumps({"offers": orderkeys})).get_json()

            for order in response:
                if(order["type"] == "URL_REDIRECT"):
                    self.assertIn("url", order.keys())


if __name__ == '__main__':
    unittest.main()
