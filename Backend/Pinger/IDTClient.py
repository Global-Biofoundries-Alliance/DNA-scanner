class IDTClient: 
    # Constructur for a IDTClient ()
    # Takes as input the configuration's parameters 
    
    def __init__(self, identity_server, token_server, screening_server, idt_username, idt_password, grant_username, grant_password, client_id, shared_secret, token, scope, timeout = 60): 
        self.identity_server = identity_server
        self.token_server = token_server
        self.screening_server = screening_server
        self.idt_username = idt_username
        self.idt_password = idt_password
        self.grant_username = grant_password
        self.client_id = client_id
        self.shared_secret = shared_secret
        self.token = token
        if(self.token == "No_Token"):
            self.getToken()
        self.scope = scope
        self.timeout = timeout
           
    # Get Token
    def getToken(self):
        data = {'grant_type': 'password', 'username': self.grant_username, 'password': self.grant_password, 'scope': self.scope}
        r = requests.post(self.token_server, data, auth=requests.auth.HTTPBasicAuth(self.client_id, shared_secret), timeout = self.timeout)
        access_token = json.loads(r.text)['access_token']
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
        resp = requests.post(self.screening_server,
                  headers={'Authorization': 'Bearer {}'.format(self.token),
                           'Content-Type': 'application/json; charset=utf-8'},
                  constructsList, timeout = self.timeout)
        result = resp.json()
        return result