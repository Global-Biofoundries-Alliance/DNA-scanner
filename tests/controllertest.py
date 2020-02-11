import unittest
from sys import maxsize

from Controller.app import app
from flask import json


class TestController(unittest.TestCase):
    name = "TestController"
    iterations = 100  # How many iterations to perform on iterated tests

    def setUp(self) -> None:
        app.config['TESTING'] = True

        with app.test_client() as client:
            self.client = client

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
            filter = {"filter": {"vendors": [1], "price": [0, 10], "deliveryDays": 50, "preselectByPrice": True, \
                                 "preselectByDeliveryDays": False}}
            response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for res in response_json["result"]:
                for vendor in res["vendors"]:
                    # Data present implies vendor 1
                    self.assertTrue(not vendor["offers"] or vendor["key"] == 1)

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

            # Create data results containing exactly one vendor
            filter = {"filter": {"vendors": [0], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response0 = self.client.post('/api/results', content_type='multipart/form-data',
                                         data={'size': 1000, 'offset': 0})

            filter = {"filter": {"vendors": [1], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response1 = self.client.post('/api/results', content_type='multipart/form-data',
                                         data={'size': 1000, 'offset': 0})

            filter = {"filter": {"vendors": [2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response2 = self.client.post('/api/results', content_type='multipart/form-data',
                                         data={'size': 1000, 'offset': 0})

            # Test if the response is still consistent to what it was before
            filter = {"filter": {"vendors": [0], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response0.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse0 = " + str(response0.data))

            filter = {"filter": {"vendors": [1], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response1.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse1 = " + str(response1.data))

            filter = {"filter": {"vendors": [2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response2.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse2 = " + str(response2.data))

            # Try to confuse the server with empty, full and invalid vendor lists
            filter = {"filter": {"vendors": [], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            filter = {"filter": {"vendors": [0, 1, 2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            filter = {"filter": {"vendors": [666, -42, 0, 0, 0, 0], "price": [0, 10], "deliveryDays": 100,
                                 "preselectByPrice": True, "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})

            # Test if the response is still consistent to what it was before after the confusion effort
            filter = {"filter": {"vendors": [0], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response0.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse0 = " + str(response0.data))

            filter = {"filter": {"vendors": [1], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response1.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse1 = " + str(response1.data))

            filter = {"filter": {"vendors": [2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                                 "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json', data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response = self.client.post('/api/results', content_type='multipart/form-data',
                                        data={'size': 1000, 'offset': 0})
            self.assertEqual(response.data, response2.data,
                             "\n\nresponse = " + str(response.data) + "\n\n\nresponse2 = " + str(response2.data))

    def test_preselection(self) -> None:
        print("Testing preselection")

        for i in range(self.iterations):
            # upload file
            handle = open('../Example_Sequence_Files/difficult_johannes.fasta', 'rb')
            response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
            self.assertIn(b"upload successful", response.data)

            # Test preselection by price
            filter = {
                "filter": {"vendors": [0, 1, 2], "price": [0, 10], "deliveryDays": 100, "preselectByPrice": True,
                           "preselectByDeliveryDays": False}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for seqoffer in response_json["result"]:
                # First create a starting condition that will cause a fail and will be overwritten in any sane scenario
                best = maxsize - 1
                best_secondary = maxsize - 1
                selected = maxsize
                selected_secondary = maxsize
                for vendoffers in seqoffer["vendors"]:
                    for offer in vendoffers["offers"]:
                        if offer["price"] <= best:
                            if offer["price"] < best or offer["turnoverTime"] < best_secondary:
                                best = offer["price"]
                                best_secondary = offer["turnoverTime"]
                        if offer["selected"]:
                            self.assertEqual(selected, maxsize)     #If this fails there was probably more than one offer selected
                            selected = offer["price"]
                            selected_secondary = offer["turnoverTime"]
                self.assertEqual(selected, best)
                self.assertEqual(selected_secondary, best_secondary)

            # Test preselection by delivery days
            filter = {
                "filter": {"vendors": [0, 1, 2], "price": [0, 10], "deliveryDays": 100,
                           "preselectByPrice": False,
                           "preselectByDeliveryDays": True}}
            filter_response = self.client.post('/api/filter', content_type='application/json',
                                               data=json.dumps(filter))
            self.assertIn(b"filter submission successful", filter_response.data)
            response_json = self.client.post('/api/results', content_type='multipart/form-data',
                                             data={'size': 1000, 'offset': 0}).get_json()

            for seqoffer in response_json["result"]:
                # First create a starting condition that will cause a fail and will be overwritten in any sane scenario
                best = maxsize - 1
                best_secondary = maxsize - 1
                selected = maxsize
                selected_secondary = maxsize
                for vendoffers in seqoffer["vendors"]:
                    for offer in vendoffers["offers"]:
                        if offer["turnoverTime"] <= best:
                            if offer["turnoverTime"] < best or offer["price"] < best_secondary:
                                best = offer["turnoverTime"]
                                best_secondary = offer["price"]
                        if offer["selected"]:
                            self.assertEqual(selected,
                                             maxsize)  # If this fails there was probably more than one offer selected
                            selected = offer["turnoverTime"]
                            selected_secondary = offer["price"]
                self.assertEqual(selected, best)
                self.assertEqual(selected_secondary, best_secondary)


if __name__ == '__main__':
    unittest.main()
