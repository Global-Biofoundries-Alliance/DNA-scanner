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
                            "key": 0,
                            "offers": [
                                {
                                    "price": 0.0,
                                    "currency": "UNKNOWN",
                                    "turnoverTime": 0,
                                    "key": 0,
                                    "offerMessage": [],
                                    "selected": False

                                },
                            ]
                        }
                    ]
                }
            ],
            "globalMessage": [],
            "vendorMessage": []
        }