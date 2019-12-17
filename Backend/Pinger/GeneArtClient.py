class GeneArtClient: 
    # Constructur for a GeneArtClient ()
    # Takes as input the configuration's parameters 
    # dnaStrings and hqDnaStrings have per defualt the value True

    def __init__(self, server, validate, status, addToCart, upload, username, token, dnaStrings = True, hqDnaStrings = True): 
        self.server = server
        self.validate = validate
        self.status = status
        self.addToCart = addToCart
        self.upload = upload
        self.username = username
        self.token = token
        self.dnaStrings = dnaStrings 
        self.hqDnaStrings = hqDnaStrings
        self.validAcc = self.authenticate()
        if(self.validAcc == False):
            raise Exception('User Credentials are wrong')
        
    # Defines the destination address for the action defined in the parameter     
    def destination(self, action):
        if(action == "validate"):
            return self.server + self.validate
        if(action == "status"):
            return self.server + self.status
        if(action == "addToCart"):
            return self.server + self.addToCart
        if(action == "upload"):
            return self.server + self.upload
    
    # Returns the authentication field which is used in several requests.
    def getAuthPart(self, projectId):
        request = {
            "authentication":
         { "username": self.username,
           "token": self.token
         }, 
         "projectId": projectId
        }
        return request
    
    # Authentication Operation
    # Checks if the username and password are correct
    # Distinguishes based on the error message
    def authenticate(self):
        result = self.statusReview("2019AAAAAX") # Dummy projectId
        if("errortype" in result.keys() and result["errortype"] == "authenticationFailed"):
            return False
        else:
            return True

    # Review stored project
    def statusReview(self, projectId):
        request = self.getAuthPart(projectId)
        dest = self.destination("status")
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result

    # Add Project to Cart
    def toCart(self, projectId):
        request = self.getAuthPart(projectId)
        dest = self.destination("addToCart")
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
    
    # Upload Project with constructs
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
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
    
    # Validate Project
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
        resp = requests.post(dest, json = request)
        result = resp.json()
        return result
    
    # Name-Generator used to define project name if none is given and adjust the given name if it isn't conform the documentation
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
