class GeneArtClient:
    server = ""
    validate = ""
    status = ""
    addToCart = ""
    upload = ""
    username = ""
    token = ""
    diagnostics = ""
    validAcc = False
    conf = {}
    
    def __init__(self): 
        with open("../config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.conf = cfg['pinger']['geneart']
        self.server = self.conf['server']
        self.validate = self.conf['validate']
        self.status = self.conf['status']
        self.addToCart = self.conf['addToCart']
        self.upload = self.conf['upload']
        self.username = self.conf['username']
        self.token = self.conf['token']
        self.diagnostics = "https://www.thermofisher.com/order/gene-design-services/api/diagnostics/v1/bulk?waitSec=60&forceRecompute=true"
        self.validAcc = self.auth()
        if(self.validAcc == False):
            raise Exception('User Credentials are wrong')
        
    def destination(self, action):
        if(action == "validate"):
            return self.server + self.validate
        if(action == "status"):
            return self.server + self.status
        if(action == "addToCart"):
            return self.server + self.addToCart
        if(action == "upload"):
            return self.server + self.upload
    
    def getAuthPart(self, projectId):
        request = {
            "authentication":
         { "username": self.username,
           "token": self.token
         }, 
         "projectId": projectId
        }
        return request
    
    def auth(self):
        result = self.statusRev("2019AAAAAX")
        if("errortype" in result.keys() and result["errortype"] == "authenticationFailed"):
            return False
        else:
            return True
    
    def statusRev(self, projectId):
        request = self.getAuthPart(projectId)
        dest = self.destination("status")
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
    
    def addtocrt(self, projectId):
        request = self.getAuthPart(projectId)
        dest = self.destination("addToCart")
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
