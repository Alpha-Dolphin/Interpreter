from coreParser import AST
from dictionary import tokenDict

class Node:

    def __init__(self):
        #Abstract behavior to non-init method to allow to other calls when neccessary
        self.isRightNode
    
    def isRightNode(self) :
        return
        #The if statement needs a lot of work
        if (AST.tokenizer.getToken() <= 30 and \
            AST.tokenizer.getTokenName() not in type(self).__name__ ) or \
            (AST.tokenizer.getToken() == 31 and \
            not type(self).__name__ is AST.IntNode()) or \
            (AST.tokenizer.getToken() == 32 and not type(self).__name__ is AST.IDNode()) \
            or AST.tokenizer.getToken() >= 33: \
            self.throwError()

    def throwError(self) :
        raise ValueError("Error: Position %s - Node Type %s - Token %s" % \
        (AST.tokenizer.currPos, type(self).__name__, str(AST.tokenizer.getToken())))

    def isTokenPresent(self, token: str) -> bool:
        return True if (AST.tokenizer.getToken() == tokenDict[token]) else False
    
    def handleSuperflousToken(self, token: str) -> None:
        self.throwError() if (AST.tokenizer.getToken() != tokenDict[token]) else AST.tokenizer.skipToken()
    
    def getConsume(self) -> int :
        val = AST.tokenizer.getToken()
        AST.tokenizer.skipToken
        return val
    
    def indentPrint(self, indent, str) :
        x = 0
        while (x < indent) : print("    ")
        print("%s\n", str)
