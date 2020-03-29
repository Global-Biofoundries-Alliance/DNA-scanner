import unittest
import json
import yaml
import uuid
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
with open('./examples/twist_clienttest_sequences.json') as json_file:
    data = json.load(json_file)

class TestTwistClient(unittest.TestCase):
    name = "TwistClient"
    # The configuration's parameters 
    host = "https://twist-api.twistbioscience-staging.com/"
    timeout = 60
    # Object of type TwistClient used in these tests to communicate with the API.
    twist = Twist.TwistClient(email, password, apitoken, eutoken, username, firstname, lastname, host = host, timeout = timeout)

    # Checks the methods with static results.
    def test_static_results(self):
        print ("\nStart tests for static results of " + self.name + ".")

        print("Test Get Accounts")
        accounts = self.twist.get_accounts()
        assert isinstance(accounts, list)
        if(len(accounts) >= 1):
            for acc in accounts:
                assert isinstance(acc, dict)
                expectedAccountKeys = ['id', 'name', 'type', 'vat', 'tax_exempt_certificate', 'tax_vat_document_url', 'account_manager', 'customer_duns']
                self.assertEqual(True, list(acc.keys()) == expectedAccountKeys)

        print("Test Prices")
        prices = self.twist.get_prices()
        assert isinstance(prices, list)
        if(len(prices) >= 1):
            for element in prices:
                assert isinstance(element, dict)
                expectedPriceKeys = ['product_code', 'unit_price', 'price_type', 'product_family', 'product']
                self.assertEqual(True, list(element.keys()) == expectedPriceKeys)

        print("Test User data")
        userdata = self.twist.get_user_data()
        assert isinstance(userdata, dict)

        expectedUserDataKeys = ['id', 'name', 'account_id', 'account_name', 'allowed_features', 'first_name', 'last_name', 'ship_to_phone', 'email', 'invited_by', 'used_by_e_commerce', 'mobile_phone', 'home_phone', 'phone', 'verification_status', 'default_shipping_address', 'default_payment_method', 'inactive', 'password_expiration_days_ttl', 'order_via_distributor', 'distributor']
        self.assertEqual(True, list(userdata.keys()) == expectedUserDataKeys)

        print("Test Addresses")
        addresses = self.twist.get_addresses()
        assert isinstance(addresses, list)
        if(len(addresses) >= 1):
            for add in addresses:
                assert isinstance(add, dict)
                expectedAddressKeys = ['id', 'first_name', 'last_name', 'address_type', 'state', 'state_name', 'street_1', 'street_2', 'zip_code', 'city', 'organization', 'country', 'country_name', 'phone_number', 'verification_status', 'created_date', 'billing_email', 'google_place_id', 'jaggaer_id', 'is_default']
                self.assertEqual(True, list(add.keys()) == expectedAddressKeys)

        print("Test Payments")
        payments = self.twist.get_payments()
        assert isinstance(payments, list)
        if(len(payments) >= 1):
            for payment in payments:
                assert isinstance(add, dict)
                expectedPaymentKeys = ['id', 'name', 'type', 'verification_status', 'submitted_by', 'is_active', 'created_date', 'submitted_by_contact', 'billing_address', 'available_po_balance', 'open_balance', 'starting_po_balance', 'invoiced_amount', 'open_orders_amount', 'purchase_order_reference', 'expiration_date', 'po_document_url', 'sent_via', 'total_past_utilized_balance', 'invoices', 'open_orders', 'po_date', 'is_default']
                self.assertEqual(True, list(payment.keys()) == expectedPaymentKeys)

        print("Test Vectors")
        vectors = self.twist.get_vectors()
        assert isinstance(vectors, list)

        # Checks the other methods which are used in ordering processes.
    def test_ClientFunctions(self):
        print ("\nStart tests for ordering functions of " + self.name + ".")
        listOfSequences = data

        print("Test Get Constructs")
        constructs = self.twist.get_constructs(listOfSequences)
        assert isinstance(constructs, list)
        self.assertEqual(len(constructs), len(listOfSequences))
        for cons in constructs:
            assert isinstance(cons, dict)
            expectedConsKeys = ['sequences', 'name', 'type', 'insertion_point_mes_uid', 'vector_mes_uid', 'column', 'row', 'plate']
            self.assertEqual(True, list(cons.keys()) == expectedConsKeys)

        print("Test Submit Constructs")
        submittedConstructs = self.twist.submit_constructs(listOfSequences)
        assert isinstance(submittedConstructs, list)
        self.assertEqual(len(submittedConstructs), len(constructs))
        for subCons in submittedConstructs:
            assert isinstance(subCons, dict)
            expectedSubConsKeys = ['id', 'type', 'name', 'vector_mes_uid', 'vector_type', 'insertion_point_mes_uid', 'adapters_on', 'external_id', 'catalog_id', 'production_data', 'product_code', 'score']
            self.assertEqual(True, list(subCons.keys()) == expectedSubConsKeys)
        ids = [i['id'] for i in submittedConstructs]

        print("Test Get Scores")
        scores = self.twist.get_scores(ids)
        assert isinstance(scores, list)
        self.assertEqual(len(scores), len(ids))
        for score in scores:
            assert isinstance(score, dict)
            expectedScoreKeys = ['id', 'score_details', 'production_data', 'score_data', 'sequences', 'owner_contact', 'type', 'name', 'notes', 'score', 'scored', 'vector_mes_uid', 'vector_type', 'insertion_point_mes_uid', 'is_insertion_site_id', 'container_id', 'created_at', 'updated_at', 'adapters_on', 'external_id', 'catalog_id', 'product_code']
            self.assertEqual(True, list(score.keys()) == expectedScoreKeys)
        
        # Adresses and payments are used in the final order.
        addresses = self.twist.get_addresses()
        payments = self.twist.get_payments()

        print("Test Get Quote (1)")
        # This quote is NOT used in the final order. This quote gets deleted later.
        example_id = self.twist.get_quote([ids[0]],
                                    external_id=str(uuid.uuid4()),
                                    address_id=addresses[0]['id'],
                                    first_name=addresses[0]['first_name'],
                                    last_name=addresses[0]['last_name'])

        with self.assertRaises(Twist.TwistError): self.twist.check_quote("A")

        print("Test Deleted Quote")
        # Delete the newly created quote
        delete_quote = self.twist.delete_quote(example_id)
        self.assertEqual(True, {'quote_marked_for_deletion': example_id} == delete_quote)

        print("Test Get Quote (2)")
        # Create a new quote to use for the final order.
        quote_id = self.twist.get_quote([ids[0]],
                                    external_id=str(uuid.uuid4()),
                                    address_id=addresses[0]['id'],
                                    first_name=addresses[0]['first_name'],
                                    last_name=addresses[0]['last_name'])

        print("Test Check Quote")
        finalQuote = self.twist.check_quote(quote_id)
        assert isinstance(finalQuote, dict)
        expecteFinalQuoteKeys = ['id', 'status_info', 'pdf_download_link', 'quote', 'opportunity_id', 'q_number', 'tat', 'owner_contact']
        self.assertEqual(True, list(finalQuote.keys()) == expecteFinalQuoteKeys)

        print("Test Submit Order")
        order = self.twist.submit_order(quote_id, payments[0]['id'])
        assert isinstance(order, dict)
        expecteOrderKeys = ['id']
        self.assertEqual(True, list(order.keys()) == expecteOrderKeys)

if __name__ == '__main__':
    unittest.main()
