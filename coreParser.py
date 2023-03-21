import sys
from tokenizer import Tokenizer

DEBUG = True

class AST:

    #AST Methods

    def __init__(self, program_file_name, input_file_name) :
        AST.tokenizer = Tokenizer(program_file_name)
        # TODO: Make this a delimited list
        AST.inputList = input_file_name
        self.treeBase = AST.ProgramNode()

    def prettyPrint(self) :
        self.treeBase.prettyPrint(0)

    def exec(self) :
        self.treeBase.exec()

    #Node parent class
    #Abstracts out all AST.Tokenizer calls

    class Node:
        def __init__(self) :
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

        def throwError(self, token: str) :
            raise ValueError("\n\tPosition - %s\n\tNode Type - %s\n\tExpected Token - %s\n\tTokenizer Token - %s" % \
            (AST.tokenizer.currPos, type(self).__name__, token, AST.tokenizer.getTokenName()))
  
        def isTokenPresent(self, token: str) -> bool:
            return True if (AST.tokenizer.getTokenName() == token) else False
        
        def handleSuperflousToken(self, token: str) -> None:
            if (DEBUG) : print(token + "\n")
            self.throwError(token) if (AST.tokenizer.getTokenName() != token) else AST.tokenizer.skipToken()
        
        def getConsume(self) -> int :
            val = AST.tokenizer.getToken()
            if (DEBUG) : 
                if (val == 31) : print(str(AST.tokenizer.intVal()) + "\n")
                elif (val == 32) : print(AST.tokenizer.idName() + "\n")
                else : print(str(val) + "\n")
            AST.tokenizer.skipToken()
            return val
        
        def indentPrint(self, indent, str) :
            print(" " * indent, str)

    #Node subclasses

    class ProgramNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('program')
            self.declSeq = AST.DeclSeqNode()
            super().handleSuperflousToken('begin')
            self.stmtSeq = AST.StmtSeqNode()
            super().handleSuperflousToken('end')

        def prettyPrint(self, ind) :
            ind += 1
            super().indentPrint("program", ind)
            self.declSeq.prettyPrint(ind)
            super().indentPrint("begin", ind)
            self.stmtSeq.prettyPrint(ind)
            super().indentPrint("end", ind)
            ind -= 1

        def exec(self) :
            print("TODO")
   
    class DeclSeqNode(Node) :
        def __init__(self) :
            super().__init__()
            self.decl = AST.DeclNode()
            if super().isTokenPresent('int') :
                self.declSeq = AST.DeclSeqNode()

    class StmtSeqNode(Node) :
        def __init__(self) :
            super().__init__()
            self.stmt = AST.StmtNode()
            if not super().isTokenPresent('end') :
                self.stmtSeq = AST.StmtSeqNode()

        def prettyPrint(self, ind) :
            ind += 1
            self.stmt.prettyPrint(ind)
            if self.stmtSeq is not None: self.stmtSeq.prettyPrint(ind)
            ind -= 1

    class DeclNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('int')
            self.idList = AST.IDListNode()
            super().handleSuperflousToken(';')

    class IDListNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = AST.IDNode()
            if super().isTokenPresent(',') :
                super().handleSuperflousToken(',')
                self.idList = AST.IDListNode()

    class StmtNode(Node) :
        def __init__(self) :
            super().__init__()
            if (super().isTokenPresent("if")) : self.child = AST.IfNode()
            elif (super().isTokenPresent("while")) : self.child = AST.LoopNode()
            elif (super().isTokenPresent("read")) : self.child = AST.InNode()
            elif (super().isTokenPresent("write")) : self.child = AST.OutNode()
            else : self.child = AST.AssignNode()
            super().handleSuperflousToken(';')

    class AssignNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = AST.IDNode()
            super().handleSuperflousToken("=")
            self.exp = AST.ExpNode()

    class IfNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('if')
            self.cond = AST.CondNode()
            super().handleSuperflousToken('then')
            self.stmtSeq1 = AST.StmtSeqNode()
            if super().isTokenPresent('else') :
                self.getConsume()
                self.stmtSeq2 = AST.StmtSeqNode()
            else: self.getConsume()
            super().handleSuperflousToken('end')

    class LoopNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("while")
            self.cond = AST.CondNode()
            super().handleSuperflousToken("loop")
            self.stmtSeq = AST.StmtSeqNode()
            super().handleSuperflousToken("end")

    class InNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("read")
            self.idList = AST.IDListNode()

    class OutNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("write")
            self.idList = AST.IDListNode()

    class CondNode(Node) :
        def __init__(self) :
            super().__init__()
            if super().isTokenPresent("[") :
                super().handleSuperflousToken("[")
                self.cond1 = AST.CondNode()
                self.logOp = self.getConsume()
                self.cond2 = AST.CondNode()
            else :
                if super().isTokenPresent("!") : self.notChild = self.getConsume()
                self.cond1 = AST.CompNode()

    class CompNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("(")
            self.op1 = AST.OpNode()
            self.compOp = AST.CompOpNode()
            self.op2 = AST.OpNode()
            super().handleSuperflousToken(")")

    class ExpNode(Node) :
        def __init__(self) :
            super().__init__()
            self.fac = AST.FacNode()
            if (super().isTokenPresent("+") or super().isTokenPresent("-")) :
                self.mathOp = self.getConsume()
                self.exp = AST.ExpNode()

    class FacNode(Node) :
        def __init__(self) :
            super().__init__()
            self.opNode = AST.OpNode()
            if (super().isTokenPresent("*")) :
                super().handleSuperflousToken("*")
                self.fac = AST.FacNode()

    class OpNode(Node) :
        def __init__(self) :
            super().__init__()
            if AST.tokenizer.getToken() == 31 : self.child = AST.IntNode()
            elif AST.tokenizer.getToken() == 32 : self.child = AST.IDNode()
            else : self.child = AST.ExpNode()
    
    class CompOpNode(Node) :
        def __init__(self) :
            super().__init__()
            self.operator = AST.tokenizer.getToken()
            self.getConsume()

    class IDNode(Node) :
        def __init__(self) :
            super().__init__()
            self.name = AST.tokenizer.idName()
            self.getConsume()
        #TODO: Need two methods for creating identifiers vs refering to existing identifiers

    class IntNode(Node) :
        def __init__(self) :
            super().__init__()
            self.value = AST.tokenizer.intVal()
            self.getConsume()

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 2:
        input_file_name = sys.argv[2]
        if len(sys.argv) > 1:
            program_file_name = sys.argv[1]
    ast = AST(program_file_name, input_file_name)