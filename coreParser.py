import sys
import os
from tokenizer import Tokenizer
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't') #.env for booleans is buggy

class Wrapper:

    #Wrapper Methods

    def __init__(self, program_file_name, input_file_name) :
        Wrapper.identifiers = {}
        Wrapper.tokenizer = Tokenizer(program_file_name)
        with open(input_file_name) as input_file: file_contents = input_file.read()
        Wrapper.inputList = file_contents.split()
        Wrapper.treeBase = Wrapper.ProgramNode()

    def prettyPrint(self) :
        print("\n--------", end = "\n")
        self.treeBase.prettyPrint(0)
        print("\n--------", end = "\n")

    def exec(self) :
        self.treeBase.exec()

    #Node parent class
    #Abstracts out most Wrapper.Tokenizer calls

    class Node:

        def __init__(self) :
            Wrapper.Node.newLine = False
            if (DEBUG): print(f"\n\t{type(self).__name__}")

        def throwError(self, token : str) -> None:
            raise ValueError("\n\tPosition - %s\n\tNode Type - %s\n\tExpected Token - %s\n\tTokenizer Token - %s" % \
            (Wrapper.tokenizer.currPos, type(self).__name__, token, Wrapper.tokenizer.getTokenName()))
  
        def isTokenPresent(self, token: str) -> bool:
            return Wrapper.tokenizer.getTokenName() == token
        
        def handleSuperflousToken(self, token) -> None:
            if (DEBUG) : print(token, end=' ')
            if ((type(token) is int and Wrapper.tokenizer.getTokenNumber() != token) or (type(token) is str and Wrapper.tokenizer.getTokenName() != token)) : self.throwError(str(token))
            Wrapper.tokenizer.skipToken()
        
        def getConsume(self) -> str:
            string = Wrapper.tokenizer.getTokenName()
            if (DEBUG) : Wrapper.Node.indentPrint(self, string, 0)
            Wrapper.tokenizer.skipToken()
            return string
        
        def indentPrint(self, string : str, indent : int) -> None:
            if(Wrapper.Node.newLine) :
                print(" "  * 4 * indent, end='')
                Wrapper.Node.newLine = False
            #??????????????
            #str(string) is neccessary
            print(str(string).lstrip(), end=' ')
            if any(substring in str(string) for substring in [";", "loop", "then", "else", "begin", "program"]):
                print('\n', end = '')
                Wrapper.Node.newLine = True

    #Node subclasses

    class ProgramNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('program')
            self.declSeq = Wrapper.DeclSeqNode()
            super().handleSuperflousToken('begin')
            self.stmtSeq = Wrapper.StmtSeqNode()
            super().handleSuperflousToken('end')
            super().handleSuperflousToken(33)

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
            self.decl = Wrapper.DeclNode()
            if super().isTokenPresent('int') : self.declSeq = Wrapper.DeclSeqNode()

        def exec(self) :
            self.decl.exec()
            if hasattr(self, "declSeq") : self.declSeq.exec()

        def prettyPrint(self, ind) :
            self.decl.prettyPrint(ind)
            if hasattr(self, "declSeq") : self.declSeq.prettyPrint(ind)

    class StmtSeqNode(Node):
        def __init__(self):
            super().__init__()
            self.stmt = Wrapper.StmtNode()
            #Need to call self here rather than super()
            if any(self.isTokenPresent(token) for token in ['if', 'while', 'read', 'write']) or Wrapper.tokenizer.getTokenNumber() == 32: self.stmtSeq = Wrapper.StmtSeqNode()

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
            self.idList = Wrapper.IDListNode()
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
            self.id = Wrapper.IDNode(True)
            if super().isTokenPresent(',') :
                super().handleSuperflousToken(',')
                self.idList = Wrapper.IDListNode()

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
            if (super().isTokenPresent("if")) : self.child = Wrapper.IfNode()
            elif (super().isTokenPresent("while")) : self.child = Wrapper.LoopNode()
            elif (super().isTokenPresent("read")) : self.child = Wrapper.InNode()
            elif (super().isTokenPresent("write")) : self.child = Wrapper.OutNode()
            else : self.child = Wrapper.AssignNode()
            super().handleSuperflousToken(';')

        def exec(self) :
            self.child.exec()

        def prettyPrint(self, ind) :
            self.child.prettyPrint(ind)
            self.child.indentPrint(';', ind)

    class AssignNode(Node) :
        def __init__(self) :
            super().__init__()
            self.id = Wrapper.IDNode()
            super().handleSuperflousToken("=")
            self.exp = Wrapper.ExpNode()

        def exec(self) :
            Wrapper.identifiers[self.id.exec()] = self.exp.exec()

        def prettyPrint(self, ind) :
            self.id.prettyPrint(ind)
            super().indentPrint("=", ind)
            self.exp.prettyPrint(ind)

    class IfNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken('if')
            self.cond = Wrapper.CondNode()
            super().handleSuperflousToken('then')
            self.stmtSeq1 = Wrapper.StmtSeqNode()
            if super().isTokenPresent('else') :
                self.getConsume()
                self.stmtSeq2 = Wrapper.StmtSeqNode()
            super().handleSuperflousToken('end')

        def exec(self) :
            if (self.cond.exec()) : self.stmtSeq1.exec()
            elif hasattr(self, "stmtSeq2") : self.stmtSeq2.exec()

        def prettyPrint(self, ind) :
            super().indentPrint("if", ind)
            self.cond.prettyPrint(ind)
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
            self.cond = Wrapper.CondNode()
            super().handleSuperflousToken("loop")
            self.stmtSeq = Wrapper.StmtSeqNode()
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
            self.idList = Wrapper.IDListNode()

        def exec(self) :
            #Error message fine per Tyler Ferguson
            for identifier in self.idList.exec(): Wrapper.identifiers[identifier] = Wrapper.inputList.pop(0)

        def prettyPrint(self, ind) :
            super().indentPrint("read", ind)
            self.idList.prettyPrint(ind)

    class OutNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("write")
            self.idList = Wrapper.IDListNode()

        def prettyPrint(self, ind) :
            super().indentPrint("write", ind)
            self.idList.prettyPrint(ind)

        def exec(self) :
            for element in self.idList.exec() : print(f"{element} = {Wrapper.identifiers[element]}")

    class CondNode(Node) :
        def __init__(self) :
            super().__init__()
            if super().isTokenPresent("[") :
                super().handleSuperflousToken("[")
                self.cond1 = Wrapper.CondNode()
                self.logOp = self.getConsume()
                self.cond2 = Wrapper.CondNode()
                super().handleSuperflousToken("]")
            elif super().isTokenPresent("!") :
                self.notChild = self.getConsume()
                self.cond = Wrapper.CondNode()
            else :
                self.comp = Wrapper.CompNode()
        
        def exec(self) :
            return eval(f"{self.cond1.exec()} {self.logOp} {self.cond2.exec()}".replace('&&', 'and').replace('||', 'or').replace('!', 'not ')) if hasattr(self, "logOp") else not self.cond.exec() if hasattr(self, "notChild") else self.comp.exec()

        def prettyPrint(self, ind) :
            if hasattr(self, "cond2"): 
                super().indentPrint("[", ind)
                self.cond1.prettyPrint(ind)
                self.indentPrint(self.logOp, ind)
                self.cond2.prettyPrint(ind)
                super().indentPrint("]", ind)
            elif hasattr(self, "notChild"): 
                super().indentPrint("!", ind)
                self.cond.prettyPrint(ind)
            else :
                self.comp.prettyPrint(ind)

    class CompNode(Node) :
        def __init__(self) :
            super().__init__()
            super().handleSuperflousToken("(")
            self.op1 = Wrapper.OpNode()
            self.compOp = self.getConsume()
            self.op2 = Wrapper.OpNode()
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
            self.fac = Wrapper.FacNode()
            if (super().isTokenPresent("+") or super().isTokenPresent("-")) :
                self.mathOp = self.getConsume()
                self.exp = Wrapper.ExpNode()

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
            self.op = Wrapper.OpNode()
            if (super().isTokenPresent("*")) :
                super().handleSuperflousToken("*")
                self.fac = Wrapper.FacNode()

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
            if Wrapper.tokenizer.getTokenNumber() == 31 : self.child = Wrapper.IntNode()
            elif Wrapper.tokenizer.getTokenNumber() == 32 : self.child = Wrapper.IDNode()
            else : self.child = Wrapper.ExpNode()

        def exec(self) :
            return Wrapper.identifiers[self.child.exec()] if isinstance(self.child, Wrapper.IDNode) else self.child.exec()

        def prettyPrint(self, ind) :
            if self.child is Wrapper.ExpNode :
                self.indentPrint("(", ind)
                self.child.prettyPrint(ind)
                self.indentPrint(")", ind)
            else :
                self.child.prettyPrint(ind)

    # Redudant Node, fine per Tyler Fergurson
    # class CompOpNode(Node) :
    #     def __init__(self) :
    #         super().__init__()
    #         self.compOp = Wrapper.tokenizer.getTokenName()
    #         super().getConsume()

    #     def exec(self) :
    #         return self.compOp

    #     def prettyPrint(self, ind) :
    #         self.indentPrint(self.compOp, ind)

    class IDNode(Node) :
        def __init__(self, boolean: bool = False):
            super().__init__()
            self.name = Wrapper.tokenizer.getTokenName()
            if boolean : Wrapper.identifiers[self.name] = "I, " + self.name + " , have been declared but not initialized"
            elif self.name not in Wrapper.identifiers : raise ValueError(f"ERROR: Use of undeclared identifer {self.name}")
            self.getConsume()

        def exec(self) :
            return self.name

        def prettyPrint(self, ind) :
            self.indentPrint(self.name, ind)

    class IntNode(Node) :
        def __init__(self) :
            super().__init__()
            self.value = Wrapper.tokenizer.getTokenName()
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
    program_file_name = os.path.dirname(os.path.abspath(__file__)) + '\\' + program_file_name
    input_file_name = os.path.dirname(os.path.abspath(__file__)) + '\\' + input_file_name
    ast = Wrapper(program_file_name, input_file_name)
    ast.prettyPrint()
    ast.exec()