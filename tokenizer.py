#Ben Elleman

import sys
from dictionary import dict

def getToken(currToken):
    val = dict.get(currToken, -1)
    if val == -1:
        if currToken.isdigit():
            val = 31
        elif currToken.isalnum() and currToken.isupper():
            val = 32
        else:
            val = 34
            raise ValueError("Invalid token encountered: \"%s\"" % currToken)
    return val

def idName(currToken):
    if (getToken(currToken) == 32):
        return currToken
    else:
        raise ValueError("Token is not an identifier: \"%s\"" % currToken)

def intVal(currToken):
    if (getToken(currToken) == 31):
        return int(currToken)
    else:
        raise ValueError("Token is not an integer: \"%s\"" % currToken)

def skipToken(currToken):
    currToken += 1

def tokenize(currLine):
    token = ""
    i = 0

    while i < len(currLine):

        #White space

        if currLine[i] == ' ' :
            i += 1

        #Integers
        
        elif currLine[i].isdigit():
            while i < len(currLine) and currLine[i].isdigit() :
                i += 1
            yield 31
        
        #Identifiers
        
        elif currLine[i].isupper():
            while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                i += 1
            yield 32

        #Keywords & reserved words

        else:
            #Loop here for efficiency (now required as i no longer increments in outer loop)
            while i < len(currLine) :
                token += currLine[i]
                i += 1
                if (token in dict):
                    yield dict[token]
                    token = ""
                    break
#               elif currLine[i] == " " :
#                    raise ValueError("Token is not an valid keyword: \"%s\"" % token)

if __name__ == '__main__':
    input_file_name = "debug.txt"
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    inputFile = open(input_file_name, "r")
    tokens = ""
    with inputFile as f:
        for line in f:
            tokens = [token for token in tokenize(line)]
            print(" ".join(str(token) for token in tokens))
        print("33")
    inputFile.close()
