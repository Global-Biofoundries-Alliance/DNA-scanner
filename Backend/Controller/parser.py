from Bio import SeqIO
import json
import sbol

# Object representing a sequence
class SeqObject:
    idN = ""
    name = ""
    sequence = ""
    length = ""
    
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
        print("Something else went wrong")    
    for seq_record in parsed:
        sequence = SeqObject()
        sequence.idN = seq_record.id
        sequence.name = seq_record.name
        sequence.sequence = str(seq_record.seq).upper()
        sequence.length = len(sequence.sequence)
        returnList.append(sequence)
        i = i + 1
    return returnList

    # Parses only SBOL files
    # Returns a list of SeqObject where each object represents a sequence of the given file
def parseSBOL(inputFile):
    i = 0
    doc = sbol.Document()
    try:
        doc.read(inputFile)
    except RuntimeError:
        print("Not a valid SBOL2 file")
    except:
        print("Something went wrong")
    returnList = []
    for a in doc.sequences:
        sequence = SeqObject()
        sequence.idN = a.displayId
        sequence.name = "Sequence " + str(i)
        sequence.sequence = str(a.elements).upper()
        sequence.length = len(sequence.sequence)
        returnList.append(sequence)
        i = i + 1
    return returnList
