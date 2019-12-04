from Bio import SeqIO
import json
import requests
import sbol
# from ..Pinger import p
class SeqObject:
    idN = ""
    name = ""
    sequence = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def parse(inputFileName):
    fileType = getFileType(inputFileName)
    if(fileType == "fasta" or fileType == "genbank"):
        return parseFile(inputFileName,fileType)
    if(fileType == "sbol"):
        return getSBOL(inputFileName)
        
def getFileType(inputFileName):
    if(inputFileName.endswith('.gb') or inputFileName.endswith('.gbk')):
        return 'genbank'
    elif(inputFileName.endswith('.fasta')):
        return 'fasta'
    elif(inputFileName.endswith('.xml') or inputFileName.endswith('.rdf')):
        return 'sbol'
    else:
        raise NameError("FILE NOT SUPPORTED! --gb, gbk, fasta, xml, rdf")
    
def parseFile(inputFile, fileFormat):
    i = 0
    returnList = []
    for seq_record in SeqIO.parse(inputFile, fileFormat):
        sequence = SeqObject()
        sequence.idN = seq_record.id
        sequence.name = seq_record.name
        sequence.sequence = str(seq_record.seq).upper()
        returnList.append(sequence)
    return returnList

def getSBOL(inputFile):
    file = open(inputFile).read()
    request = { 'options': {'language' : 'SBOL2',
                            'test_equality': False,
                            'check_uri_compliance': False,
                            'check_completeness': False,
                            'check_best_practices': False,
                            'fail_on_first_error': False,
                            'provide_detailed_stack_trace': False,
                            'subset_uri': '',
                            'uri_prefix': '',
                            'version': '',
                            'insert_type': False,
                            'main_file_name': 'main file',
                            'diff_file_name': 'comparison file',
                                    },
                'return_file': True,
                'main_file': file
              }
    resp = requests.post("https://validator.sbolstandard.org/validate/", json = request)
    result = resp.json()['result']
    result_file = "res.xml"
    text_file = open(result_file, "w")
    n = text_file.write(result)
    text_file.close()
    return parseSBOL(result_file)
    
def parseSBOL(inputString):
    doc = sbol.Document()
    doc.read(inputString)
    #print(doc)
    #doc.write('aa.xml')
    #print(len(doc))
    i = 0
    returnList = []
    for a in doc.sequences:
        sequence = SeqObject()
        sequence.idN = "NoId"
        sequence.name = "NoName"
        sequence.sequence = str(a.elements).upper()
        returnList.append(sequence)
    #print(returnList[0].idN)
    #print(returnList[0].name)
    #print(returnList[0].sequence)
    #print("~~~~~~~~~~~~~~~~~~~~~~")
    #for cd in doc.componentDefinitions:
    #    returnList[i].idN = cd.displayId
    #    i += 1
    #print(returnList[0].idN)
    #print(returnList[0].name)
    #print(returnList[0].sequence)
    return returnList
