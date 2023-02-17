#Ben Elleman

import sys
from dictionary import dict

class Tokenizer:

    def __init__(self, input_file_name):
        self.currPos = 0
        self.input_file = open(input_file_name, "r")
        with open(input_file_name) as self.input_file:
            self.tokens = self.tokenize()
            # for token in self.tokens:
            #     print(token)

    def getToken(self):
        return self.tokens[self.currPos][0]

    def idName(self):
        #Python doesn't allow exception raises in ternaries, what a rip off
        if self.tokens[self.currPos][0] == 32:
            return self.tokens[self.currPos][1]
        else:
            raise ValueError("Token is not an identifier: \"%s\"" % self.tokens[self.currPos][1])

    def intVal(self):
        if self.tokens[self.currPos][0] == 31:
            return self.tokens[self.currPos][1]
        else:
            raise ValueError("Token is not an integer: \"%s\"" % self.tokens[self.currPos][1])

    def skipToken(self):
        if (self.currPos < len(self.tokens) and self.tokens[self.currPos][0] < 33) :
            self.currPos += 1

    def tokenize(self):
        list = []
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
                    integer = 0
                    while i < len(currLine) and currLine[i].isdigit() :
                        integer *= 10 + int(currLine[i])
                        i += 1
                    list.append((31, integer))
                    dumb = False

                #Identifiers
                
                elif currLine[i].isupper():
                    id = ""
                    while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                        id += currLine[i]
                        i += 1
                    list.append((32, id))
                    dumb = False     

                #Keywords & reserved words

                else:
                    #Loop here for efficiency (now required as i no longer increments in outer loop)
                    token = ""
                    while i < len(currLine) :
                        token += currLine[i]
                        i += 1
                        if (token in dict):
                            #len(token) == 1 check for effeciency as most tokens are > 1 len
                            if len(token) == 1 and (token == '=' or token == '!' or token == '<' or token == '>') and i < len(currLine) and currLine[i] == '='  :
                                #Could manually append = but this is simplier
                                continue
                            dumb = self.dumbChecker(dumb, token)
                            list.append((dict[token], token))
                            break
                        #Check for invalid token
                        elif i < len(currLine) and currLine[i] == " " :
                            raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        #Conventional end of text character
        list.append((33, "\x1A"))
        return list

    def dumbChecker(self, dumb, token) :
        if (12 <= dict[token] <= 30) :
            return True
        elif dumb :
            return False
        else :
            raise ValueError("Invalid whitespace at token: \"%s\"" % token)



if __name__ == '__main__':
    input_file_name = "debug.txt"
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    tokenizer = Tokenizer(input_file_name)

    # Call getToken() and print the return value
    print(tokenizer.getToken())

    # Call skipToken() multiple times and print the return value
    for i in range(2):
        print(tokenizer.skipToken())

    # Call idName() and print the return value
    print(tokenizer.idName())

    #Now crash :)
    print(tokenizer.intVal())
