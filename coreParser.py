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
        
        def isRightNode(self) :
            if (AST.tokenizer.getToken() <= 30 and \
                AST.tokenizer.getTokenName() not in type(self).__name__ ) or \
                (AST.tokenizer.getToken() == 31 and \
                not type(self).__name__ is AST.IntNode()) or \
                (AST.tokenizer.getToken() == 32 and not type(self).__name__ is AST.IDNode()) \
                or AST.tokenizer.getToken() >= 33: \
                self.throwError()

        def throwError(self) :
            raise ValueError("Error: Position %s - Node Type %s - Token %s" % (AST.tokenizer.currPos, type(self).__name__, str(AST.tokenizer.getToken())))
  
        def isTokenPresent(self, token: str) -> bool:
            return True if (AST.tokenizer.getToken() == tokenDict[token]) else False
        
        def handleSuperflousToken(self, token: str) -> None:
            self.throwError() if (AST.tokenizer.getToken() != tokenDict[token]) else AST.tokenizer.skipToken()

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
                AST.tokenizer.skipToken()
                self.stmtSeq = AST.StmtSeqNode()
            else :
                AST.tokenizer.skipToken()

    class DeclSeqNode(Node):
        def __init__(self):
            super().__init__()
            self.decl = AST.DeclNode()
            if self.isTokenPresent(',') :
                AST.tokenizer.skipToken()
                self.declSeq = AST.DeclSeqNode()
            else :
                AST.tokenizer.skipToken()

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
                AST.tokenizer.skipToken()
                self.idList = AST.IDListNode()
            else :
                AST.tokenizer.skipToken()

    class StmtNode(Node):
        def __init__(self):
            super().__init__()

    class AssignNode(Node):
        def __init__(self):
            super().__init__()
            self.id = AST.IDNode()
            self.handleSuperflousToken("=")
            self.exp = AST.ExpNode()

    class IfNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken('if')
            self.cond = AST.CondNode()
            self.handleSuperflousToken('then')
            self.stmtSeq1 = AST.StmtSeqNode()
            if self.isTokenPresent('else'):
                AST.tokenizer.skipToken()
            else:
                AST.tokenizer.skipToken()
                self.stmtSeq2 = AST.StmtSeqNode()
            self.handleSuperflousToken('end')

    class LoopNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("while")
            self.cond = AST.CondNode()
            self.handleSuperflousToken("loop")
            self.stmtSeq = AST.StmtSeqNode()
            self.handleSuperflousToken("end")

    class InNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("read")
            self.idList = AST.IDListNode()

    class OutNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("write")
            self.idList = AST.IDListNode()

    class CondNode(Node):
        def __init__(self):
            super().__init__()

    class CompNode(Node):
        def __init__(self):
            super().__init__()
            self.handleSuperflousToken("(")
            self.op1 = AST.OpNode()
            self.compOp = AST.CompOpNode()
            self.op2 = AST.OpNode()
            self.handleSuperflousToken(")")

    class ExpNode(Node):
        def __init__(self):
            super().__init__()
            self.fac = AST.FacNode()
            if (self.isTokenPresent("+")) :
                self.handleSuperflousToken("+")
                self.exp = AST.ExpNode()
            if (self.isTokenPresent("-")) :
                self.handleSuperflousToken("-")
                self.exp = AST.ExpNode()

    class FacNode(Node):
        def __init__(self):
            super().__init__()
            self.opNode = AST.OpNode()
            if (self.isTokenPresent("*")) :
                self.handleSuperflousToken("*")
                self.fac = AST.FacNode()

    class OpNode(Node):
        def __init__(self):
            super().__init__()
            if AST.tokenizer.getToken() == 31 : self.child = AST.IntNode()
            elif AST.tokenizer.getToken() == 32 : self.child = AST.IDNode()
            else : self.child = AST.ExpNode()
    
    class CompOpNode(Node):
        def __init__(self):
            super().__init__()
            self.operator = AST.tokenizer.getToken()
            AST.tokenizer.skipToken()

    class IDNode(Node):
        def __init__(self):
            super().__init__()
            self.name = AST.tokenizer.idName()
            AST.tokenizer.skipToken()
        #Need two methods for creating identifiers vs refering to existing identifiers

    class IntNode(Node):
        def __init__(self):
            super().__init__()
            self.value = AST.tokenizer.intVal()
            AST.tokenizer.skipToken()

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 2:
        input_file_name = sys.argv[2]
        if len(sys.argv) > 1:
            program_file_name = sys.argv[1]
    ast = AST(program_file_name, input_file_name)