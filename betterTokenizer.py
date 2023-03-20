from dictionary import tokenDict
from tokenizer import Tokenizer

class BetterTokenizer(Tokenizer):

    def tokenize(self):

        for currLine in self.input_file :
                        
            i = 0
         
            while i < len(currLine) :

                #White space

                if currLine[i] == ' ' :
                    i += 1

                #Integers
                
                elif currLine[i].isdigit():
                    value = 0
                    while i < len(currLine) and currLine[i].isdigit() :
                        value = value * 10 + int(currLine[i])
                        i += 1
                    self.tokenList.append((31, value))

                #Identifiers
                
                elif currLine[i].isupper():
                    id = ""
                    while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                        id += currLine[i]
                        i += 1
                    self.tokenList.append((32, id))

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
                            self.tokenList.append((tokenDict[token], token))
                            break
                        #Check for invalid token
                        elif i < len(currLine) and currLine[i] == " " :
                            raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        #Conventional end of text character
        self.tokenList.append((33, "\x1A"))
