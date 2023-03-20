import sys
from tokenizer import Tokenizer
from dictionary import tokenDict

class AST :

    def __init__(self, program_file_name, input_file_name):
        AST.tokenizer = Tokenizer(program_file_name)
        # TODO: Make this a delimited list
        AST.inputList = input_file_name

    class Node:
        def __init__(self):
            #Abstract behavior to non-init method to allow to other calls when neccessary
            self.isRightNode

        def printName(self):
            print(type(self).__name__)
        
        def isRightNode(self) :
            print()
            #TODO

        def throwError(self) :
            raise ValueError("Error: Position %s - Node Type %s - Token %s" % (AST.tokenizer.currPos, type(self).__name__, str(AST.tokenizer.getToken())))
  
        def isTokenPresent(self, token) -> bool:
            return True if (AST.tokenizer.getToken == tokenDict[token]) else False
        
        def handleSuperflousToken(self, token) -> None:
            self.throwError() if (AST.tokenizer.getToken != tokenDict[token]) else AST.tokenizer.skipToken()

    class ProgramNode(Node):
        def __init__(self):
            super().__init__()
            self.declSeq = AST.DeclSeqNode()
            self.handleSuperflousToken('begin')
            self.stmtSeq = AST.StmtSeqNode()
            self.handleSuperflousToken('end')

    class StmtSeqNode(Node):
        def __init__(self):
            super().__init__()
            self.stmt = AST.StmtNode()
            if self.isTokenPresent('end') :
                AST.tokenizer.skipToken
                self.stmtSeq = AST.StmtSeqNode()
            else :
                AST.tokenizer.skipToken

    class DeclSeqNode(Node):
        def __init__(self):
            super().__init__()
            self.decl = AST.DeclNode()
            if self.isTokenPresent(',') :
                AST.tokenizer.skipToken
                self.declSeq = AST.DeclSeqNode()
            else :
                AST.tokenizer.skipToken

    class DeclNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken('int')
            self.idList = AST.IDListNode()

    class IDListNode(Node):
        def __init__(self):
            super().__init__()
            self.id = AST.IDNode()
            if self.isTokenPresent(',') :
                AST.tokenizer.skipToken
                self.idList = AST.IDListNode()
            else :
                AST.tokenizer.skipToken

    class StmtNode(Node):
        def __init__(self):
            super().__init__()

    class AssignNode(Node):
        def __init__(self):
            super().__init__()
            self.id = AST.IDNode
            self.handleSuperflousToken("=")
            self.exp = AST.ExpNode

    class IfNode(Node):
        def __init__(self):
            super().__init__()
            self.cond = AST.CondNode()
            self.handleSuperflousToken('if')
            self.stmtSeq1 = AST.StmtSeqNode()
            if self.isTokenPresent('else'):
                AST.tokenizer.skipToken()
                AST.tokenizer.skipToken()
            else:
                AST.tokenizer.skipToken()
                self.stmtSeq2 = AST.StmtSeqNode()
            self.handleSuperflousToken('end')

    class LoopNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("while")
            self.cond = AST.CondNode
            self.handleSuperflousToken("loop")
            self.stmtSeq = AST.StmtSeqNode
            self.handleSuperflousToken("end")

    class InNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("read")
            self.idList = AST.IDListNode

    class OutNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("write")
            self.idList = AST.IDListNode

    class CondNode(Node):
        def __init__(self):
            super().__init__()

    class CompNode(Node):
        def __init__(self):
            super().__init__()

    class ExpNode(Node):
        def __init__(self):
            super().__init__()

    class FacNode(Node):
        def __init__(self):
            super().__init__()

    class OpNode(Node):
        def __init__(self):
            super().__init__()

    class CompOpNode(Node):
        def __init__(self):
            super().__init__()

    class IDNode(Node):
        def __init__(self):
            super().__init__()

    class IntNode(Node):
        def __init__(self):
            super().__init__()

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 2:
        input_file_name = sys.argv[2]
        if len(sys.argv) > 1:
            program_file_name = sys.argv[1]
    ast = AST(program_file_name, input_file_name)
