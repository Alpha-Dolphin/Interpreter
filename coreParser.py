import sys
from tokenizer import Tokenizer

DEBUG = False

#TODO: Talk to 

class AST:

    #AST Methods

    def __init__(self, program_file_name, input_file_name) :
        AST.identifiers = {}
        #Fine per Tyler Ferguson
        AST.tokenizer = Tokenizer(program_file_name)
        with open(input_file_name, 'r') as input_file: file_contents = input_file.read()
        AST.inputList = file_contents.split()
        AST.treeBase = AST.ProgramNode()

    def prettyPrint(self) :
        self.treeBase.prettyPrint(0)
        print("\n", end = "")

    def exec(self) :
        self.treeBase.exec()

    #Node parent class
    #Abstracts out most AST.Tokenizer calls

    class Node:

        def __init__(self) :
            AST.Node.newLine = False
            if (DEBUG): print(f"\n\t{type(self).__name__}")
            #Abstract behavior to non-init method to allow to other calls when neccessary
            self.isRightNode
        
        def isRightNode(self) -> None:
            return
            #This if statement needs a lot of work
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
            return AST.tokenizer.getTokenName() == token
        
        def handleSuperflousToken(self, token: str) -> None:
            if (DEBUG) : print(token, end=' ')
            self.throwError(token) if (AST.tokenizer.getTokenName() != token) else AST.tokenizer.skipToken()
        
        def getConsume(self) -> str:
            string = AST.tokenizer.getTokenName()
            if (DEBUG) : AST.Node.indentPrint(self, string, 0)
            AST.tokenizer.skipToken()
            return string
        
        def indentPrint(self, string : str, indent : int) -> None:
            if(AST.Node.newLine) :
                print(" "  * 4 * indent, end='')
                AST.Node.newLine = False
            #??????????????
            #str(string) is neccessary
            print(str(string).lstrip(), end=' ')
            if any(substring in str(string) for substring in [";", "loop", "if", "then", "else", "begin", "program"]):
                print('\n', end = '')
                AST.Node.newLine = True

    #Node subclasses

    class ProgramNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('program')
            self.declSeq = AST.DeclSeqNode()
            super().handleSuperflousToken('begin')
            self.stmtSeq = AST.StmtSeqNode()
            super().handleSuperflousToken('end')

        def exec(self) :
            self.declSeq.exec()
            self.stmtSeq.exec()

        def prettyPrint(self, ind) :
            super().indentPrint("program", ind)
            self.declSeq.prettyPrint(ind + 1)
            super().indentPrint("begin", ind)
            self.stmtSeq.prettyPrint(ind + 1)
            super().indentPrint("end", ind)

    class DeclSeqNode(Node) :
        def __init__(self) :
            super().__init__()
            self.decl = AST.DeclNode()
            if super().isTokenPresent('int') : self.declSeq = AST.DeclSeqNode()

        def exec(self) :
            self.decl.exec()
            if hasattr(self, "declSeq") : self.declSeq.exec()

        def prettyPrint(self, ind) :
            self.decl.prettyPrint(ind)
            if hasattr(self, "declSeq") : self.declSeq.prettyPrint(ind)

    class StmtSeqNode(Node) :
        def __init__(self) :
            super().__init__()
            self.stmt = AST.StmtNode()
            if not super().isTokenPresent('end') : self.stmtSeq = AST.StmtSeqNode()

        def exec(self) :
            self.stmt.exec()
            if hasattr(self, "stmtSeq") : self.stmtSeq.exec()

        def prettyPrint(self, ind) :
            self.stmt.prettyPrint(ind)
            if hasattr(self, "stmtSeq") : self.stmtSeq.prettyPrint(ind)

    class DeclNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('int')
            self.idList = AST.IDListNode()
            super().handleSuperflousToken(';')

        def exec(self) :
            self.idList.exec()

        def prettyPrint(self, ind) :
            super().indentPrint("int", ind)
            self.idList.prettyPrint(ind)
            super().indentPrint(";", ind)

    class IDListNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = AST.IDNode(True)
            if super().isTokenPresent(',') :
                super().handleSuperflousToken(',')
                self.idList = AST.IDListNode()

        def exec(self) :
            result = [self.id.exec()]
            if hasattr(self, "idList"): result += self.idList.exec()
            return result

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

        def exec(self) :
            self.child.exec()

        def prettyPrint(self, ind) :
            self.child.prettyPrint(ind)
            self.child.indentPrint(';', ind)

    class AssignNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = AST.IDNode()
            super().handleSuperflousToken("=")
            self.exp = AST.ExpNode()

        def exec(self) :
            AST.identifiers[self.id.exec()] = self.exp.exec()

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
            super().handleSuperflousToken('end')

        def exec(self) :
            if (self.cond.exec()) : self.stmtSeq1.exec()
            elif hasattr(self, "stmtSeq2") : self.stmtSeq2.exec()

        def prettyPrint(self, ind) :
            super().indentPrint("if", ind)
            self.cond.prettyPrint(ind + 1)
            super().indentPrint("then", ind)
            self.stmtSeq1.prettyPrint(ind + 1)
            if hasattr(self, "stmtSeq2") :
                super().indentPrint("else", ind)
                self.stmtSeq2.prettyPrint(ind + 1)
            super().indentPrint("end", ind)

    class LoopNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("while")
            self.cond = AST.CondNode()
            super().handleSuperflousToken("loop")
            self.stmtSeq = AST.StmtSeqNode()
            super().handleSuperflousToken("end")

        def exec(self) :
            while(self.cond.exec()) : self.stmtSeq.exec()

        def prettyPrint(self, ind) :
            super().indentPrint("while", ind)
            self.cond.prettyPrint(ind)
            super().indentPrint("loop", ind)
            self.stmtSeq.prettyPrint(ind + 1)
            super().indentPrint("end", ind)

    class InNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("read")
            self.idList = AST.IDListNode()

        def exec(self) :
            #Fine per Tyler Ferguson
            for identifier in self.idList.exec(): AST.identifiers[identifier] = AST.inputList.pop(0)

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

        def exec(self) :
            for element in self.idList.exec() : print(f"{element} = {AST.identifiers[element]}")

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
                self.cond = AST.CondNode()
            else :
                self.comp = AST.CompNode()
        
        def exec(self) :
            return eval(f"{self.cond1.exec()} {self.logOp} {self.cond2.exec()}") if hasattr(self, "logOp") else not self.cond.exec() if hasattr(self, "notChild") else self.comp.exec()

        def prettyPrint(self, ind) :
            if hasattr(self, "cond2"): 
                super().indentPrint("[", ind)
                self.cond1.prettyPrint(ind)
                self.indentPrint(self.logOp, ind)
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
            self.compOp = self.getConsume()
            self.op2 = AST.OpNode()
            super().handleSuperflousToken(")")

        def exec(self) :
            #Error message fine per Tyler Ferguson
            return eval(f"{self.op1.exec()} {self.compOp} {self.op2.exec()}")

        def prettyPrint(self, ind) :
            super().indentPrint("(", ind)
            self.op1.prettyPrint(ind)
            self.indentPrint(self.compOp, ind)
            self.op2.prettyPrint(ind)
            super().indentPrint(")", ind)

    class ExpNode(Node) :
        def __init__(self) :
            super().__init__()
            self.fac = AST.FacNode()
            if (super().isTokenPresent("+") or super().isTokenPresent("-")) :
                self.mathOp = self.getConsume()
                self.exp = AST.ExpNode()

        def exec(self) :
            return eval(f"{self.fac.exec()} {self.mathOp} {self.exp.exec()}") if hasattr(self, "mathOp") else self.fac.exec()

        def prettyPrint(self, ind) :
            self.fac.prettyPrint(ind)
            if hasattr(self,"mathOp") :
                self.indentPrint(self.mathOp, ind)
                self.exp.prettyPrint(ind)

    class FacNode(Node) :
        def __init__(self) :
            super().__init__()
            self.op = AST.OpNode()
            if (super().isTokenPresent("*")) :
                super().handleSuperflousToken("*")
                self.fac = AST.FacNode()

        def exec(self) :
            return eval(f"{self.op.exec()} * {self.fac.exec()}") if hasattr(self, "fac") else self.op.exec()

        def prettyPrint(self, ind) :
            self.op.prettyPrint(ind)
            if hasattr(self,"fac") :
                self.indentPrint("*", ind)
                self.fac.prettyPrint(ind)
    
    class OpNode(Node) :
        def __init__(self) :
            super().__init__()
            #TODO Factor this out?
            if AST.tokenizer.getTokenNumber() == 31 : self.child = AST.IntNode()
            elif AST.tokenizer.getTokenNumber() == 32 : self.child = AST.IDNode()
            else : self.child = AST.ExpNode()

        def exec(self) :
            return AST.identifiers[self.child.exec()] if isinstance(self.child, AST.IDNode) else self.child.exec()

        def prettyPrint(self, ind) :
            if self.child is AST.ExpNode :
                self.indentPrint("(", ind)
                self.child.prettyPrint(ind)
                self.indentPrint(")", ind)
            else :
                self.child.prettyPrint(ind)

    # Redudant Node, fine per Tyler Fergurson
    # class CompOpNode(Node) :
    #     def __init__(self) :
    #         super().__init__()
    #         self.compOp = AST.tokenizer.getTokenName()
    #         super().getConsume()

    #     def exec(self) :
    #         return self.compOp

    #     def prettyPrint(self, ind) :
    #         self.indentPrint(self.compOp, ind)

    class IDNode(Node) :
        def __init__(self, boolean: bool = False):
            super().__init__()
            self.name = AST.tokenizer.getTokenName()
            if (boolean) : AST.identifiers[self.name] = "I, " + self.name + " , have been declared but not initialized"
            elif self.name not in AST.identifiers : raise ValueError(f"ERROR: Use of undeclared identifer {self.name}")
            self.getConsume()

        def exec(self) :
            return self.name

        def prettyPrint(self, ind) :
            self.indentPrint(self.name, ind)

    class IntNode(Node) :
        def __init__(self) :
            super().__init__()
            self.value = AST.tokenizer.getTokenName()
            self.getConsume()

        def exec(self) :
            return self.value

        def prettyPrint(self, ind) :
            self.indentPrint(self.value, ind)

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 1:
        program_file_name = sys.argv[1]
        if len(sys.argv) > 2:
            input_file_name = sys.argv[2]
    ast = AST(program_file_name, input_file_name)
    ast.prettyPrint()
    print('\n---------\n')
    ast.exec()