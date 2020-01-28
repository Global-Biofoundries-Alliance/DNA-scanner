from Bio import SeqIO
import json
import sbol

# Object representing a sequence
class SeqObject():
    def SeqObject(idN, name, sequence):
        self.idN = idN
        self.name = name
        self.sequence = sequence
    
    # Converts the SeqObject into a JSON-Object
    def toJSON(self):
        return {"idN": self.idN, "name": self.name, "sequence": self.sequence}

    # Parse File based on inputFileName
def parse(inputFileName):
    fileType = getFileType(inputFileName)
    if(fileType == "fasta" or fileType == "genbank"):
        return parseFastaGB(inputFileName,fileType)
    if(fileType == "sbol"):
        return parseSBOL(inputFileName)
    
    # Returns the file format based on the file ending
def getFileType(inputFileName):
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
def parseFastaGB(inputFile, fileFormat):
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
def parseSBOL(inputFile):
    i = 0
    doc = sbol.Document()
    doc.read(inputFile)
    returnList = []
    for a in doc.sequences:
        sequence = SeqObject(idN = a.displayId, name = "Sequence " + str(i), sequence = str(a.elements).upper())
        returnList.append(sequence)
        i = i + 1
    return returnList
