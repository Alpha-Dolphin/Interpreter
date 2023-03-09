import sys
from dictionary import dict
from tokenizer import Tokenizer

class BetterTokenizer(Tokenizer):

    def tokenize(self):
        list = []

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
                    list.append((31, value))

                #Identifiers
                
                elif currLine[i].isupper():
                    id = ""
                    while i < len(currLine) and (currLine[i].isdigit() or currLine[i].isupper()) :
                        id += currLine[i]
                        i += 1
                    list.append((32, id))

                #Keywords & reserved words

                else:
                    token = ""
                    while i < len(currLine) :
                        token += currLine[i]
                        i += 1
                        if (token in dict):
                            #len(token) == 1 check for effeciency as most tokens are > 1 len
                            if len(token) == 1 and (token == '=' or token == '!' or token == '<' or token == '>') and i < len(currLine) and currLine[i] == '='  :
                                #Could manually append an "=" but this is simplier
                                continue
                            list.append((dict[token], token))
                            break
                        #Check for invalid token
                        elif i < len(currLine) and currLine[i] == " " :
                            raise ValueError("Token is not an valid keyword: \"%s\"" % token)
        #Conventional end of text character
        list.append((33, "\x1A"))
        return list
