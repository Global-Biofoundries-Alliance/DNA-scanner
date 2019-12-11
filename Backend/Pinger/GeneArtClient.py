import json
import requests
import yaml

cfg_geneart = {}

def getConfig():
    global cfg_geneart
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    cfg_geneart = cfg['geneart']

def statOrAddToCart(projectId, action):
    request = {
        "authentication":
     { "username": cfg_geneart['username'],
       "token": cfg_geneart['token']
     }, 
     "projectId": projectId
    }
    destination = getDestination(action)
    resp = requests.post(destination, json = request)
    result = resp.json()
    if(resp.status_code == 400 or resp.status_code == 500):
        printError(result, resp.status_code)
    else:
        print("ProjectId: " + str(result["projectId"]))
        statusField = str(result["status"])
        print("Status: " + statusField)
        if(not(statusField == "draft")):
            print("CartId: " + str(result["cartId"]))

            
def getDestination(action):
    if(action == "validate"):
        return cfg_geneart['server'] + cfg_geneart['validate']
    if(action == "status"):
        return cfg_geneart['server'] + cfg_geneart['status']
    if(action == "addToCart"):
        return cfg_geneart['server'] + cfg_geneart['addToCart']
    if(action == "upload"):
        return cfg_geneart['server'] + cfg_geneart['upload']

def printError(resultJson, code):
    if(code==400):
        print("ErrorType: " + str(resultJson["errortype"]))
        print("Details: " + str(resultJson["details"]))
    if(code == 500):
        print("Details: " + str(resultJson["details"]))
