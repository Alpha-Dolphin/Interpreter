import sys
from tokenizer import Tokenizer

DEBUG = False

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
        
        def isRightNode(self) -> None:
            return
            #The if statement needs a lot of work
            if (AST.tokenizer.getToken() <= 30 and \
                AST.tokenizer.getTokenName() not in type(self).__name__ ) or \
                (AST.tokenizer.getToken() == 31 and \
                not type(self).__name__ is AST.IntNode()) or \
                (AST.tokenizer.getToken() == 32 and not type(self).__name__ is AST.IDNode()) \
                or AST.tokenizer.getToken() >= 33: \
                self.throwError()

        def throwError(self, token : str) -> None:
            raise ValueError("\n\tPosition - %s\n\tNode Type - %s\n\tExpected Token - %s\n\tTokenizer Token - %s" % \
            (AST.tokenizer.currPos, type(self).__name__, token, AST.tokenizer.getTokenName()))
  
        def isTokenPresent(self, token: str) -> bool:
            return True if (AST.tokenizer.getTokenName() == token) else False
        
        def handleSuperflousToken(self, token: str) -> None:
            if (DEBUG) : print(token + "\n")
            self.throwError(token) if (AST.tokenizer.getTokenName() != token) else AST.tokenizer.skipToken()
        
        def getConsume(self) -> str:
            string = AST.tokenizer.getTokenName()
            if (DEBUG) : print(string + "\n")
            AST.tokenizer.skipToken()
            return string
        
        def indentPrint(self, string : str, indent : int) -> None:
            print(" " * indent, string, end='')
            #??????????????
            if (";" in str(string)) : print('\n', end='')

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
            super().indentPrint("program", ind)
            self.declSeq.prettyPrint(ind)
            super().indentPrint("begin", ind)
            self.stmtSeq.prettyPrint(ind)
            super().indentPrint("end", ind)

        def exec(self) :
            print("TODO")
   
    class DeclSeqNode(Node) :
        def __init__(self) :
            super().__init__()
            self.decl = AST.DeclNode()
            if super().isTokenPresent('int') :
                self.declSeq = AST.DeclSeqNode()

        def prettyPrint(self, ind) :
            self.decl.prettyPrint(ind)
            if hasattr(self, "declSeq") : self.declSeq.prettyPrint(ind)

    class StmtSeqNode(Node) :
        def __init__(self) :
            super().__init__()
            self.stmt = AST.StmtNode()
            if not super().isTokenPresent('end') :
                self.stmtSeq = AST.StmtSeqNode()

        def prettyPrint(self, ind) :
            self.stmt.prettyPrint(ind)
            if hasattr(self, "stmtSeq") : self.stmtSeq.prettyPrint(ind)

    class DeclNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('int')
            self.idList = AST.IDListNode()
            super().handleSuperflousToken(';')

        def prettyPrint(self, ind) :
            super().indentPrint("int", ind)
            self.idList.prettyPrint(ind)
            super().indentPrint(";", ind)

    class IDListNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = AST.IDNode()
            if super().isTokenPresent(',') :
                super().handleSuperflousToken(',')
                self.idList = AST.IDListNode()

        def prettyPrint(self, ind) :
            self.id.prettyPrint(ind)
            if hasattr(self, 'idList'):
                super().indentPrint(",", ind)
                self.idList.prettyPrint(ind)

    class StmtNode(Node) :
        def __init__(self) :
            super().__init__()
            if (super().isTokenPresent("if")) : self.child = AST.IfNode()
            elif (super().isTokenPresent("while")) : self.child = AST.LoopNode()
            elif (super().isTokenPresent("read")) : self.child = AST.InNode()
            elif (super().isTokenPresent("write")) : self.child = AST.OutNode()
            else : self.child = AST.AssignNode()
            super().handleSuperflousToken(';')

        def prettyPrint(self, ind) :
            self.child.prettyPrint(ind)
            self.child.indentPrint(';', ind)

    class AssignNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = AST.IDNode()
            super().handleSuperflousToken("=")
            self.exp = AST.ExpNode()

        def prettyPrint(self, ind) :
            self.id.prettyPrint(ind)
            super().indentPrint("=", ind)
            self.exp.prettyPrint(ind)

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

        def prettyPrint(self, ind) :
            super().indentPrint("if", ind)
            self.cond.prettyPrint(ind)
            super().indentPrint("then", ind)
            if hasattr(self, "stmtSeq2") :
                super().indentPrint("else", ind)
                self.stmtSeq2.prettyPrint(ind)
            super().indentPrint("end", ind)

    class LoopNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("while")
            self.cond = AST.CondNode()
            super().handleSuperflousToken("loop")
            self.stmtSeq = AST.StmtSeqNode()
            super().handleSuperflousToken("end")

        def prettyPrint(self, ind) :
            super().indentPrint("while", ind)
            self.cond.prettyPrint(ind)
            super().indentPrint("loop", ind)
            self.stmtSeq.prettyPrint(ind)
            super().indentPrint("end", ind)

    class InNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("read")
            self.idList = AST.IDListNode()

        def prettyPrint(self, ind) :
            super().indentPrint("read", ind)
            self.idList.prettyPrint(ind)

    class OutNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("write")
            self.idList = AST.IDListNode()

        def prettyPrint(self, ind) :
            super().indentPrint("write", ind)
            self.idList.prettyPrint(ind)

    class CondNode(Node) :
        def __init__(self) :
            super().__init__()
            if super().isTokenPresent("[") :
                super().handleSuperflousToken("[")
                self.cond1 = AST.CondNode()
                self.logOp = self.getConsume()
                self.cond2 = AST.CondNode()
            elif super().isTokenPresent("!") :
                self.notChild = self.getConsume()
                self.cond1 = AST.CondNode()
            else :
                self.comp = AST.CompNode()

        def prettyPrint(self, ind) :
            if hasattr(self, "cond2"): 
                super().indentPrint("[", ind)
                self.cond1.prettyPrint(ind)
                self.logOp.prettyPrint(ind)
                self.cond2.prettyPrint(ind)
                super().indentPrint("]", ind)
            elif hasattr(self, "notChild"): 
                super().indentPrint("!", ind)
                self.cond1.prettyPrint(ind)
            else :
                self.comp.prettyPrint(ind)

    class CompNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("(")
            self.op1 = AST.OpNode()
            self.compOp = AST.CompOpNode()
            self.op2 = AST.OpNode()
            super().handleSuperflousToken(")")

        def prettyPrint(self, ind) :
            super().indentPrint("(", ind)
            self.op1.prettyPrint(ind)
            self.compOp.prettyPrint(ind)
            self.op2.prettyPrint(ind)
            super().indentPrint(")", ind)

    class ExpNode(Node) :
        def __init__(self) :
            super().__init__()
            self.fac = AST.FacNode()
            if (super().isTokenPresent("+") or super().isTokenPresent("-")) :
                self.mathOp = self.getConsume()
                self.exp = AST.ExpNode()

        def prettyPrint(self, ind) :
            self.fac.prettyPrint(ind)
            if hasattr(self,"mathOp") :
                self.indentPrint(self.mathOp, ind)
                self.exp.prettyPrint(ind)

    class FacNode(Node) :
        def __init__(self) :
            super().__init__()
            self.opNode = AST.OpNode()
            if (super().isTokenPresent("*")) :
                super().handleSuperflousToken("*")
                self.fac = AST.FacNode()

        def prettyPrint(self, ind) :
            self.opNode.prettyPrint(ind)
            if hasattr(self,"fac") :
                self.indentPrint("*", ind)
                self.fac.prettyPrint(ind)
    
    class OpNode(Node) :
        def __init__(self) :
            super().__init__()
            if AST.tokenizer.getToken() == 31 : self.child = AST.IntNode()
            elif AST.tokenizer.getToken() == 32 : self.child = AST.IDNode()
            else : self.child = AST.ExpNode()

        def prettyPrint(self, ind) :
            if self.child is AST.ExpNode :
                self.indentPrint("(", ind)
                self.child.prettyPrint(ind)
                self.indentPrint(")", ind)
            else :
                self.child.prettyPrint(ind)

    class CompOpNode(Node) :
        def __init__(self) :
            super().__init__()
            self.compOp = AST.tokenizer.getTokenName()
            self.getConsume()

        def prettyPrint(self, ind) :
            self.indentPrint(self.compOp, ind)

    class IDNode(Node) :
        def __init__(self) :
            super().__init__()
            self.name = AST.tokenizer.idName()
            self.getConsume()
        #TODO: Need two methods for creating identifiers vs refering to existing identifiers
        
        def prettyPrint(self, ind) :
            self.indentPrint(self.name, ind)

    class IntNode(Node) :
        def __init__(self) :
            super().__init__()
            self.value = AST.tokenizer.intVal()
            self.getConsume()

        def prettyPrint(self, ind) :
            self.indentPrint(self.value, ind)

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 2:
        input_file_name = sys.argv[2]
        if len(sys.argv) > 1:
            program_file_name = sys.argv[1]
    ast = AST(program_file_name, input_file_name)
    ast.prettyPrint()