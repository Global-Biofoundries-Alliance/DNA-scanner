from Bio import SeqIO
import json
import sbol
import time
import requests
# Object representing a sequence
class SeqObject():
    def __init__(self, idN, name, sequence):
        self.idN = idN
        self.name = name
        self.sequence = sequence
    
    # Converts the SeqObject into a JSON-Object
    def toJSON(self):
        return {"idN": self.idN, "name": self.name, "sequence": self.sequence}
class BoostClient:
    def __init__(self, url_job, url_hosts, url_submit, url_login, username, password, juggling_strategy, host, timeout = 60): 
        self.url_job = url_job
        self.url_hosts = url_hosts
        self.url_submit = url_submit
        self.url_login = url_login
        self.username = username
        self.password = password
        self.juggling_strategy = juggling_strategy
        self.host = host
        self.timeout = timeout
        self.token = "NO_TOKEN"
        self.jwt = {'NO': 'TOKEN'}
        self.uuid = "NO_UUID"
        self.codonUsageTable = "NO_TABLE"

    # Log-In
    def login(self):
        data = {"username": self.username, "password": self.password}
        response = requests.post(url = self.url_login, json = data)
        print(response)
        self.token = response.json()["boost-jwt"]
        self.jwt = {"boost-jwt": self.token}
        print("Token: ", self.token)
    
    # Translate
    def translate(self, inputSequences):
        self.login()
        self.getPreDefinedHosts()
        inputString = ""
        for i in inputSequences:
            inputString = inputString + (">" + str((i.toJSON())["name"]) + "\n" + str((i.toJSON())["sequence"]) + "*\n")
        inputString = inputString[: -2]    
        submit = self.submit(inputString, self.codonUsageTable, self.juggling_strategy)
        while(self.getInformation1(self.uuid) != "FINISHED"):
            print("SLEEP 2 Seconds")
            time.sleep(3)
        response = self.getInformation2(self.uuid)
        file = open("resultfile.fasta","w") 
        file.write(response["job"]["job-report"]["response"][0]["modified-sequences-text"]) 
        file.close()
        #return g
    
    # Submit a Job
    def submit(self, inputString, codonTable, strategy):
        job = {"job": {"job-BOOST-function": "REVERSE_TRANSLATE"},"sequences": {
                "text": inputString,
                "type": ["PROTEIN"]
            },
            "modifications": {
                "text": codonTable,
                "strategy": strategy,
                "genetic-code": "STANDARD"
            },
            "output": {
                "format": "FASTA"
            }
        }
        print(job)
        response = requests.post(url='https://boost.jgi.doe.gov/rest/jobs/submit', json = job, cookies = self.jwt)
        print(response)
        print(response.json())
        self.uuid = response.json()["job-uuid"]
        print("Job-UUID", self.uuid)

    # Get information for this job
    def getInformation1(self, uuid):
        url_job_uuid = self.url_job + str(uuid)
        print(url_job_uuid)
        print(self.jwt)
        response = requests.get(url=url_job_uuid, cookies = self.jwt)
        print("GG")
        print(response)
        print(response.json()["job"]["job-status"])
        return response.json()["job"]["job-status"]
    
        # Get information for this job
    def getInformation2(self, uuid):
        url_job_uuid = self.url_job + str(uuid)
        response = requests.get(url=url_job_uuid, cookies = self.jwt)
        return response.json()

    # Get Pre-defined hosts
    def getPreDefinedHosts(self):
        response = (requests.get(url=self.url_hosts, cookies = self.jwt)).json()
        for i in response["predefined-hosts"]:
            if(i["host-name"]== self.host):
                self.codonUsageTable = i["codon-usage-table"]
                break


class Parser:
    def __init__(self, url_job, url_hosts, url_submit, url_login, username, password, juggling_strategy, host, timeout = 60): 
        self.url_job = url_job
        self.url_hosts = url_hosts
        self.url_submit = url_submit
        self.url_login = url_login
        self.username = username
        self.password = password
        self.juggling_strategy = juggling_strategy
        self.host = host
        self.timeout = timeout
        self.token = "NO_TOKEN"
        self.jwt = "NO_JWT"
        self.uuid = "NO_UUID"

        # Parse File based on inputFileName
    def parse(self, inputFileName, aminoacids):
        fileType = self.getFileType(inputFileName)
        if(fileType == "fasta" or fileType == "genbank"):
            parsedSequences = self.parseFastaGB(inputFileName,fileType)
        if(fileType == "sbol"):
            parsedSequences = self.parseSBOL(inputFileName)
        if(aminoacids == True):        
            self.boostClient = BoostClient(self.url_job, self.url_hosts, self.url_submit, self.url_login, self.username, self.password, self.juggling_strategy, self.host, self.timeout)
            if(len(parsedSequences) == 0):
                raise RuntimeError("Parsing went wrong.")
            translatedSequences = self.boostClient.translate(parsedSequences)
            return self.parse("resultfile.fasta", False)
        return parsedSequences
        
        # Returns the file format based on the file ending
    def getFileType(self, inputFileName):
        f = open(inputFileName)
        line = f.readline()
        f.close()
        words = line.split()
        if(inputFileName.endswith('.gb') or inputFileName.endswith('.gbk')):
            if(words[0] == "LOCUS"):
                return 'genbank'
            else:
                raise RuntimeError("Not a valid GenBank file.")
        elif(inputFileName.endswith('.fasta') or inputFileName.endswith('.fna') or inputFileName.endswith('.faa')):
            if(words[0][0] == ">"):
                return 'fasta'
            else:
                raise RuntimeError("Not a valid Fasta file.")
        elif(inputFileName.endswith('.xml') or inputFileName.endswith('.rdf')):
            return 'sbol'
        else:
            raise NameError("FILE NOT SUPPORTED! --gb, gbk, fasta, faa, fna, xml, rdf")
        
        # Parses only Fasta and GenBank files
        # Returns a list of SeqObject where each object represents a sequence of the given file
    def parseFastaGB(self, inputFile, fileFormat):
        i = 0
        returnList = []
        try:
            parsed = SeqIO.parse(inputFile, fileFormat)
        except:
            print("Parsing of the file failed.")    
        for seq_record in parsed:
            sequence = SeqObject(idN = seq_record.id, name = seq_record.name, sequence = str(seq_record.seq).upper())
            returnList.append(sequence)
            i = i + 1
        return returnList

        # Parses only SBOL files
        # Returns a list of SeqObject where each object represents a sequence of the given file
    def parseSBOL(self, inputFile):
        i = 0
        doc = sbol.Document()
        doc.read(inputFile)
        returnList = []
        for a in doc.sequences:
            sequence = SeqObject(idN = a.displayId, name = "Sequence " + str(i), sequence = str(a.elements).upper())
            returnList.append(sequence)
            i = i + 1
        return returnList
