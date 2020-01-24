class SearchResponse(object):
    def __init__(self):
        self.data = {
            "size": 10,
            "count": 0,
            "offset": 0,
            "result": [
                {
                    "sequenceInformation": {
                        "id": "1233-4566",
                        "name": "Waschmittel",
                        "sequence": "ACTG",
                        "length": 255
                    },
                    "vendors": [
                        {
                            "name": "TWIST DNA ...",
                            "shortName": "TWIST",
                            "key": "",
                            "offers": [
                                {
                                    "price": 0.0,
                                    "turnoverTime": 0,
                                    "offerMessage": []
                                },
                            ]
                        }
                    ]
                }
            ],
            "globalMessage": [
                "TWIST API currently unavailable"
            ]
        }


# Represents the filtering settings
# used on results and vendors
class Filter(object):




    def Filter(self, filter_dict):
        # List of permitted vendor ids
        self.vendors = filter_dict["vendors"]

        # Allowed price range
        self.price = filter_dict["price"]

        # Maximum number of days until delivery
        self.deliveryDays = filter_dict["deliveryDays"]

        # Determines whether price or turnover time
        # has greater weight when determining which offers
        # to select by default
        # Note: Exactly one of these must be True!
        self.preselectByPrice = filter_dict["preselectByPrice"]
        # Enforce that exactly one of these can be true
        self.preselectByDeliveryDays = not self.preselectByDeliveryDays
