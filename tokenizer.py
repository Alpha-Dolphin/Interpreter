from dictionary import tokenDict

class Tokenizer:

    def __init__(self, input_file_name):
        self.currPos = 0
        self.input_file = open(input_file_name, "r")
        with open(input_file_name) as self.input_file : self.tokenList = self.tokenize()
        self.currPos = 0

    def getToken(self):
        return self.tokens[self.currPos][0]
    
    def getTokenName(self):
        return self.tokens[self.currPos][1]
    
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
        #This functionality is dumb
        dumb = True

        for currLine in self.input_file :
            self.tokens = []
            i = 0
            
            while i < len(currLine) :

                #White space

                if currLine[i] == ' ' :
                    i += 1
                    dumb = True

                #Integers
                
                elif currLine[i].isdigit():
                    value = 0
                    while i < len(currLine) and currLine[i].isdigit() :
                        value = value * 10 + int(currLine[i])
                        i += 1
                    dumb = self.dumbChecker(dumb, value)
                    self.tokens.append((31, value))

                #Identifiers
                
                elif currLine[i].isupper():
                    id = ""
                    while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                        id += currLine[i]
                        i += 1
                    dumb = self.dumbChecker(dumb, id)
                    self.tokens.append((32, id))

                #Keywords & reserved words

                else:
                    token = ""
                    while i < len(currLine) :
                        token += currLine[i]
                        i += 1
                        if (token in tokenDict):
                            #len(token) == 1 check for effeciency as most tokens are > 1 len
                            if len(token) == 1 and (token == '=' or token == '!' or token == '<' or token == '>') and i < len(currLine) and currLine[i] == '='  :
                                #Could manually append an "=" but this is simplier
                                continue
                            dumb = self.dumbChecker(dumb, token)
                            self.tokens.append((tokenDict[token], token))
                            break
                        #Check for invalid token
                        elif i < len(currLine) and currLine[i] == " " :
                            raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        #Conventional end of text character
        self.tokens.append((33, "\x1A"))

    def dumbChecker(self, dumb, token) :
        if dict.get(token, -1) in range(12, 31):
            return True
        elif dumb :
            return False
        else :
            raise ValueError("Invalid whitespace at token: \"%s\"" % token)
