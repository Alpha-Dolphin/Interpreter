import sys
import os

from dictionary import tokenDict

class Tokenizer:

    def __init__(self, program_file_name) :
        self.currPos = 0
        self.tokenList = []
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\' + program_file_name, "r") as self.input_file : self.tokenize()

    def getTokenNumber(self) -> int:
        return self.tokenList[self.currPos][0]
    
    def getTokenName(self) -> str:
        return self.tokenList[self.currPos][1]

    def skipToken(self) :
        if (self.currPos < len(self.tokenList) and self.tokenList[self.currPos][0] < 33) : self.currPos += 1

    def tokenize(self) :
        #This functionality is dumb
        dumb = True

        for currLine in self.input_file :
            i = 0
            
            while i < len(currLine) :

                #White space

                if currLine[i] == ' ' :
                    i += 1
                    dumb = True

                #Integers
                
                elif currLine[i].isdigit() :
                    value = 0
                    while i < len(currLine) and currLine[i].isdigit() :
                        value = value * 10 + int(currLine[i])
                        i += 1
                    dumb = self.dumbChecker(dumb, value)
                    self.tokenList.append((31, value))

                #Identifiers
                
                elif currLine[i].isupper() :
                    id = ""
                    while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                        id += currLine[i]
                        i += 1
                    dumb = self.dumbChecker(dumb, id)
                    self.tokenList.append((32, id))

                #Keywords & reserved words

                else:
                    token = ""
                    while i < len(currLine) :
                        token += currLine[i]
                        i += 1
                        if (token in tokenDict) :
                            #len(token) == 1 check for effeciency as most tokens are > 1 len
                            if len(token) == 1 and (token == '=' or token == '!' or token == '<' or token == '>') and i < len(currLine) and currLine[i] == '='  :
                                #Could manually append an "=" but this is simplier
                                continue
                            dumb = self.dumbChecker(dumb, token)
                            self.tokenList.append((tokenDict[token], token))
                            break
                        #Check for invalid token
                        elif i < len(currLine) and currLine[i] == " " :
                            raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        #Conventional end of text character
        self.tokenList.append((33, "\x1A"))

    def dumbChecker(self, dumb, token) :
        if tokenDict.get(token, -1) in range(12, 31) : return True
        elif dumb : return False
        else : raise ValueError("Invalid whitespace at token: \"%s\"" % token)

if __name__ == '__main__':
    program_file_name = "debug.txt"
    if len(sys.argv) > 1: program_file_name = sys.argv[1]
    tokenizer = Tokenizer(program_file_name)
    for token in tokenizer.tokenList : print(token)