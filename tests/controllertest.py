import unittest

from Controller.app import app


class TestController(unittest.TestCase):
    name = "TestController"

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

    def test_upload(self) -> None:
        print("Testing file upload")

        handle = open('../Example_Sequence_Files/difficult_johannes.fasta', 'rb')
        response = self.client.post('/api/upload', content_type='multipart/form-data', data={'seqfile': handle})
        searchResult = eval(response.data)              #Don't do this in production code, kids! (It's okay here since our own mock data is generally trusted)
        expectedCount = 0
        self.assertIn("size", searchResult.keys())
        self.assertIn("count", searchResult.keys())
        self.assertIn("offset", searchResult.keys())
        self.assertIn("sessionId", searchResult.keys())
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
                self.assertIn("name", vendor.keys())
                self.assertIn("shortName", vendor.keys())
                self.assertIn("key", vendor.keys())
                self.assertIn("offers", vendor.keys())
                for offer in vendor["offers"]:
                    self.assertIn("price", offer.keys())
                    self.assertIn("turnoverTime", offer.keys())
                    self.assertIn("offerMessage", offer.keys())


        self.assertEqual(expectedCount, searchResult["count"], "Mismatch between declared and actual sequence count!")

    def test_vendor_endpoint(self) -> None:
        print("Testing /vendors endpoint")

        resp = self.client.get("/api/vendors")
        vendors = eval(resp.data)
        expectedKey = 0
        for vendor in vendors:
            self.assertIn("name", vendor.keys())
            self.assertIn("shortName", vendor.keys())
            self.assertIn("key", vendor.keys())

            self.assertEqual(vendor["key"], expectedKey)
            expectedKey = expectedKey + 1

if __name__ == '__main__':
    unittest.main()
