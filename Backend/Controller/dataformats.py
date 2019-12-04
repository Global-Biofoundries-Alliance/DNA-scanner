class SearchResponse(object):
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


def toDict(resp: SearchResponse):
    dictionary = resp.__dict__
    for key in dictionary.keys():  # remove all of the keys added by python
        if key.startswith("__", 0, len(key)):
            del dictionary[key]
    return dictionary
