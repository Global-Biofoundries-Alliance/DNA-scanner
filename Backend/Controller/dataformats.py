class SchmearchResponse(object):
    def __init__(self):
        self.size = 10
        self.count = 150
        self.offset = 1
        self.result = [
            {
                "offers": [
                    {
                        "vendorinformation": {
                            "name": "TWIST DNA ...",
                            "shortname": "TWIST",
                            "key": ""
                        },
                        "price": "0.05",
                        "turnovertime": "10"
                    }
                ],
                "sequenceinformation": {
                    "id": "1233-4566",
                    "name": "Waschmittel",
                    "sequence": "ACTG"
                }
            }
        ]
        self.message = ["TWIST API currently unavailable"]


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
                                    "offerMessage": [],
                                    "selected": False
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


#def toDict(resp: SearchResponse):
#    dictionary = resp.__dict__
#    for key in dictionary.keys():  # remove all of the keys added by python
#        if key.startswith("__", 0, len(key)):
#            del dictionary[key]
#    return dictionary
