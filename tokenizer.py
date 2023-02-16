#Ben Elleman

import sys
from dictionary import dict

class Tokenizer:

    def __init__(self, input_file_name):
        self.currPos = 0
        self.input_file = open(input_file_name, "r")
        with open(input_file_name) as self.input_file:
            self.tokens = self.tokenize()
            for token in self.tokens:
                print(token)


    # def _tokenizeLine(currLine):
    #     tokens = [token for token in tokenize(currLine)]
    #     return tokens

    def getToken(self):
        val = dict.get(self.tokens[self.currPos], -1)
        if val == -1:
            if self.tokens[self.currPos].isdigit():
                val = 31
            elif self.tokens[self.currPos].isalnum() and self.tokens[self.currPos].isupper():
                val = 32
            #Ascii value of eof token is 3 (called end of text or EOT)
            elif 3 == ascii(self.tokens[self.currPos]):
                val = 33
            else:
                val = 34
        return val

    def idName(self):
        return self.tokens[self.currPos] if self.tokens[self.currPos].isalnum() and self.tokens[self.currPos].isupper() else ValueError("Token is not an identifier: \"%s\"" % self.tokens[self.currPos])

    def intVal(self):
        return int(self.tokens[self.currPos]) if self.tokens[self.currPos].isdigit() else ValueError("Token is not an integer: \"%s\"" % self.tokens[self.currPos])

    def skipToken(self):
        if (self.currPos < len(tokens) and self.getToken() < 33) :
            self.currPos += 1

    def tokenize(self):
        list = []
        token = ""
        i = 0
        #This functionality is dumb
        dumb = True

        for currLine in self.input_file :
            
            while i < len(currLine) :

                #White space

                if currLine[i] == ' ' :
                    i += 1
                    dumb = True

                #Integers
                
                elif currLine[i].isdigit():
                    while i < len(currLine) and currLine[i].isdigit() :
                        i += 1
                    list.append(31)
                    dumb = False

                #Identifiers
                
                elif currLine[i].isupper():
                    while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                        i += 1
                    list.append(32)
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
                            dumb = self.dumbChecker(dumb, token)
                            list.append(dict[token])
                            token = ""
                            break
                        #Check for invalid token
                        elif i < len(currLine) and currLine[i] == " " :
                            raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        list.append(31)
        return list

    def dumbChecker(self, dumb, token) :
        if not (dumb or (12 <= dict[token] <= 30)):
            raise ValueError("Invalid whitespace at token: \"%s\"" % token)
        dumb = True if 12 <= dict[token] <= 30 else False
        return dumb

if __name__ == '__main__':
    input_file_name = "debug.txt"
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    tokens = ""
    tokenizer = Tokenizer(input_file_name)