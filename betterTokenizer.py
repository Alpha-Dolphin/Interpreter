#Ben Elleman

import sys
from dictionary import dict

# def _tokenizeLine(currLine):
#     tokens = [token for token in tokenize(currLine)]
#     return tokens
class Tokenizer:

    def __init__(self):
        self.currPos = 0

    def getToken(self, currToken):
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

    def idName(self, currToken):
        return currToken if currToken.isalnum() and currToken.isupper() else ValueError("Token is not an identifier: \"%s\"" % currToken)


    def intVal(self, currToken):
        return int(currToken) if currToken.isdigit() else ValueError("Token is not an integer: \"%s\"" % currToken)

    def skipToken(self, tokens):
        if (self.currPos < len(tokens) and tokens[self.currPos] < 33) :
            self.currPos += 1

    def tokenize(self, currLine):
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
                        #len(token) == 1 check for effeciency as most tokens are > 1 len
                        if len(token) == 1 and (token == '=' or token == '!' or token == '<' or token == '>') and i < len(currLine) and currLine[i] == '='  :
                            #Could manually append = but this is simplier
                            continue
                        yield dict[token]
                        token = ""
                        break
                    #Check for invalid token
                    elif i < len(currLine) and currLine[i] == " " :
                        raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        yield 33

if __name__ == '__main__':
    input_file_name = "debug.txt"
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    inputFile = open(input_file_name, "r")
    tokens = ""
    tokenizer = Tokenizer()
    with open(input_file_name) as f:
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize(f.read())
        for token in tokens:
            print(token)
        #    print(tokens)
        # currPos = 0
        # while True :
        #     print(tokens[currPos])
        #     currPos = skipToken(tokens, currPos)
    inputFile.close()
