#Ben Elleman

import sys
from dictionary import dict

# def _tokenizeLine(currLine):
#     tokens = [token for token in tokenize(currLine)]
#     return tokens

currPos = 0

def getToken(currToken):
    val = dict.get(currToken, -1)
    if val == -1:
        if currToken.isdigit():
            val = 31
        elif currToken.isalnum() and currToken.isupper():
            val = 32
        #Ascii value of eof token is 3 (called end of text or EOT)
        elif 3 == ascii(currToken):
            val = 33
        else:
            val = 34
    return val

def idName(currToken):
    return currToken if currToken.isalnum() and currToken.isupper() else ValueError("Token is not an identifier: \"%s\"" % currToken)


def intVal(currToken):
    return int(currToken) if currToken.isdigit() else ValueError("Token is not an integer: \"%s\"" % currToken)

def skipToken(tokens):
    if (currPos < len(tokens) and tokens[currPos] < 33) :
        currPos += 1

def tokenize(currLine):
    token = ""
    i = 0
    #This functionality is dumb
    dumb = True

    while i < len(currLine):

        #White space

        if currLine[i] == ' ' :
            i += 1
            dumb = True

        #Integers
        
        elif currLine[i].isdigit():
            while i < len(currLine) and currLine[i].isdigit() :
                i += 1
            yield 31
            dumb = False

        #Identifiers
        
        elif currLine[i].isupper():
            while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                i += 1
            yield 32
            dumb = False     

        #Keywords & reserved words

        else:
            #Loop here for efficiency (now required as i no longer increments in outer loop)
            while i < len(currLine) :
                token += currLine[i]
                i += 1
                if (token in dict):
                    #len(token) == 1 check for effeciency as most tokens are > 1 len
                    if len(token) == 1 and (token == '=' or token == '!' or token == '<' or token == '>') and i < len(currLine) and currLine[i] == '='  :
                        #Could manually append = but this is simplier
                        continue
                    dumb = dumbChecker(dumb, token)
                    yield dict[token]
                    token = ""
                    break
                #Check for invalid token
                elif i < len(currLine) and currLine[i] == " " :
                    raise ValueError("Token is not an valid keyword: \"%s\"" % token)
    yield 33

def dumbChecker(dumb, token) :
    if not (dumb or (12 <= dict[token] <= 30)):
        raise ValueError("Invalid whitespace at token: \"%s\"" % token)
    dumb = True if 12 <= dict[token] <= 30 else False
    return dumb

if __name__ == '__main__':
    input_file_name = "debug.txt"
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    inputFile = open(input_file_name, "r")
    tokens = ""
    with inputFile as f:
        for line in f:
            tokens = [token for token in tokenize(line)]
            for token in tokens:
                print(token)
        #    print(tokens)
        # currPos = 0
        # while True :
        #     print(tokens[currPos])
        #     currPos = skipToken(tokens, currPos)
    inputFile.close()
