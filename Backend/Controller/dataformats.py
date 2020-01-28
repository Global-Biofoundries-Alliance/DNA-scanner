class SearchResponse(object):
    def __init__(self):
        self.data = {
            "size": 10,
            "count": 0,
            "offset": 0,
            "sessionId": "12345-12345-12345",
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