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
        return parseSBOL(inputFileName)
        
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

  
def parseSBOL(inputString):
    i = 0
    doc = sbol.Document()
    doc.read(inputFile)
    returnList = []
    for a in doc.sequences:
        sequence = SeqObject()
        sequence.idN = a.displayId
        sequence.name = "Sequence " + str(i)
        sequence.sequence = str(a.elements).upper()
        returnList.append(sequence)
        i = i + 1
    return returnList
