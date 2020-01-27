import requests
import json
class IDTClient: 
    # Constructur for a IDTClient ()
    # Takes as input the configuration's parameters 
    
    def __init__(self, token_server, screening_server, idt_username, idt_password, client_id, client_secret, scope, token = "", timeout = 60):
        self.token_server = token_server
        self.screening_server = screening_server
        self.idt_username = idt_username
        self.idt_password = idt_password
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.scope = scope
        self.timeout = timeout
        if(self.token == ""):
            self.getToken()
           
    # Get Token
    def getToken(self):
        data = {'grant_type': 'password', 'username': self.idt_username, 'password': self.idt_password, 'scope': self.scope}
        r = requests.post(self.token_server, data, auth=requests.auth.HTTPBasicAuth(self.client_id, self.client_secret), timeout = self.timeout)
        if(not('access_token' in r.json())):
            raise KeyError("Access token could not be generated. Check your credentials.")
        access_token = r.json()['access_token']
        self.token = access_token
        
    # Use API-Endpoint
    def screening(self, listOfSequences):
        constructsList = []
        for construct in listOfSequences:
            sequence = {
                "Name": construct["name"],
                "Sequence": construct["sequence"],
              }
            constructsList.append(sequence)
        print(constructsList)
        resp = requests.post(self.screening_server,
                  headers={'Authorization': 'Bearer {}'.format(self.token), 'Content-Type': 'application/json; charset=utf-8'}, json=constructsList, timeout = self.timeout)
        result = resp.json()
        return result
