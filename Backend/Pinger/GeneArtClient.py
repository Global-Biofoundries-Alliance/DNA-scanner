class GeneArtClient:   
    def __init__(self): 
        with open("../config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.conf = cfg['pinger']['geneart']
        self.dnaStrings = self.conf['dnaStrings'] == "enabled"
        self.hqDnaStrings = self.conf['hqDnaStrings'] == "enabled"
        self.server = self.conf['server']
        self.validate = self.conf['validate']
        self.status = self.conf['status']
        self.addToCart = self.conf['addToCart']
        self.upload = self.conf['upload']
        self.username = self.conf['username']
        self.token = self.conf['token']
        self.validAcc = self.authenticate()
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
    
    def authenticate(self):
        result = self.statusReview("2019AAAAAX")
        if("errortype" in result.keys() and result["errortype"] == "authenticationFailed"):
            return False
        else:
            return True
    
    def statusReview(self, projectId):
        request = self.getAuthPart(projectId)
        dest = self.destination("status")
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
    
    def toCart(self, projectId):
        request = self.getAuthPart(projectId)
        dest = self.destination("addToCart")
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
    
    def constUpload(self, listOfSequences, product):
        now = datetime.now() 
        dt_string = now.strftime("%d-%m-%Y_%H_%M")
        projectname = "ect-" + str(dt_string)
        dest = self.destination("upload")
        constructsList = []
        for construct in listOfSequences:
            sequence = {
                "name": self.generateName(construct["name"]),
                "sequence": construct["sequence"],
                "product": product,
                "comment": "idN: " + construct["idN"] + " , name: " + construct["name"]
              }
            constructsList.append(sequence)
        request = {
            "authentication":
         { "username": self.username,
           "token": self.token
         },
            "project": {
                "name": projectname,
                "constructs": constructsList
            }
        }
        #print(constructsList)
        #print(index)
        print(request)
        resp = requests.post(dest, json = request)
        print(resp)
        result = resp.json()
        print(result)
        
    def constValidate(self, listOfSequences, product):
        now = datetime.now() 
        dt_string = now.strftime("%d-%m-%Y_%H_%M")
        projectname = "project-" + str(dt_string)
        dest = self.destination("validate")
        constructsList = []
        for construct in listOfSequences:
            sequence = {
                "name": self.generateName(construct["name"]),
                "sequence": construct["sequence"],
                "product": product,
                "comment": "idN: " + construct["idN"] + " , name: " + construct["name"]
              }
            constructsList.append(sequence)
        request = {
           "project": {
                "name": projectname,
                "constructs": constructsList
            }
        }
        #print(constructsList)
        #print(index)
        print(request)
        resp = requests.post(dest, json = request)
        print(resp)
        result = resp.json()
        print(result)
    
    def generateName(self, prevName):
        if(len(prevName) == 0):
            now = datetime.now() 
            dt_string = now.strftime("%d/%m/%Y_%H:%M")
            prevName = "consname-" + str(dt_string)
        else: 
            if(len(prevName) > 20):
                prevName = prevName[:20]
        clean_consName = re.sub(r'[^.A-z0-9_\-]', "_", prevName)
        return clean_consName
