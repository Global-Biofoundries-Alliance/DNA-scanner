from Bio import SeqIO
import json
import sbol

# Object representing a sequence
class SeqObject:
    idN = ""
    name = ""
    sequence = ""
    
    # Converts the SeqObject into a JSON-Object
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    # Parse File based on inputFileName
def parse(inputFileName):
    fileType = getFileType(inputFileName)
    if(fileType == "fasta" or fileType == "genbank"):
        return parseFastaGB(inputFileName,fileType)
    if(fileType == "sbol"):
        return parseSBOL(inputFileName)
    
    # Returns the file format based on the file ending
def getFileType(inputFileName):
    if(inputFileName.endswith('.gb') or inputFileName.endswith('.gbk')):
        return 'genbank'
    elif(inputFileName.endswith('.fasta') or inputFileName.endswith('.fna') or inputFileName.endswith('.faa')):
        return 'fasta'
    elif(inputFileName.endswith('.xml') or inputFileName.endswith('.rdf')):
        return 'sbol'
    else:
        raise NameError("FILE NOT SUPPORTED! --gb, gbk, fasta, faa, fna, xml, rdf")
    
    # Parses only Fasta and GenBank files
    # Returns a list of SeqObject where each object represents a sequence of the given file
def parseFastaGB(inputFile, fileFormat):
    i = 0
    returnList = []
    for seq_record in SeqIO.parse(inputFile, fileFormat):
        sequence = SeqObject()
        sequence.idN = seq_record.id
        sequence.name = seq_record.name
        sequence.sequence = str(seq_record.seq).upper()
        returnList.append(sequence)
    return returnList

    # Parses only SBOL files
    # Returns a list of SeqObject where each object represents a sequence of the given file
def parseSBOL(inputFile):
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
