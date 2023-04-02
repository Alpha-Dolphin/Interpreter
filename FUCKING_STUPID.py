import sys
from tokenizer import Tokenizer

DEBUG = False

class Node:
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList):
        self.identifiers = identifiers
        self.tokenizer = tokenizer
        self.inputList = inputList
        Node.newLine = False
        if (DEBUG): print(f"\n\t{type(self).__name__}")
        self.isRightNode()
    
    def isRightNode(self) -> None:
        return
        if (self.tokenizer.getToken() <= 30 and \
            self.tokenizer.getTokenName() not in type(self).__name__ ) or \
            (self.tokenizer.getToken() == 31 and \
            not type(self).__name__ is IntNode()) or \
            (self.tokenizer.getToken() == 32 and not type(self).__name__ is IDNode()) \
            or self.tokenizer.getToken() >= 33: \
            self.throwError()

    def throwError(self, token : str) -> None:
        raise ValueError("\n\tPosition - %s\n\tNode Type - %s\n\tExpected Token - %s\n\tTokenizer Token - %s" % \
        (self.tokenizer.currPos, type(self).__name__, token, self.tokenizer.getTokenName()))

    def isTokenPresent(self, token: str) -> bool:
        return self.tokenizer.getTokenName() == token
    
    def handleSuperflousToken(self, token: str) -> None:
        if (DEBUG) : print(token, end=' ')
        self.throwError(token) if (self.tokenizer.getTokenName() != token) else self.tokenizer.skipToken()
    
    def getConsume(self) -> str:
        string = self.tokenizer.getTokenName()
        if (DEBUG) : Node.indentPrint(self, string, 0)
        self.tokenizer.skipToken()
        return string
    
    def indentPrint(self, string : str, indent : int) -> None:
        if(Node.newLine) :
            print(" "  * 4 * indent, end='')
            Node.newLine = False
        print(str(string).lstrip(), end=' ')
        if any(substring in str(string) for substring in [";", "loop", "then", "else", "begin", "program"]):
            print('\n', end = '')
            Node.newLine = True

class ProgramNode(Node) :
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList) :
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList

        super().handleSuperflousToken('program')
        self.declSeq = DeclSeqNode(identifiers, tokenizer, inputList)
        super().handleSuperflousToken('begin')
        self.stmtSeq = StmtSeqNode(identifiers, tokenizer, inputList)
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
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList) :
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList

        self.decl = DeclNode(identifiers, tokenizer, inputList)
        if super().isTokenPresent('int') : self.declSeq = DeclSeqNode(identifiers, tokenizer, inputList)

    def exec(self) :
        self.decl.exec()
        if hasattr(self, "declSeq") : self.declSeq.exec()

    def prettyPrint(self, ind) :
        self.decl.prettyPrint(ind)
        if hasattr(self, "declSeq") : self.declSeq.prettyPrint(ind)

class StmtSeqNode(Node):
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList

        self.stmt = StmtNode(identifiers, tokenizer, inputList)
        if any(self.isTokenPresent(token) for token in ['if', 'while', 'read', 'write']) or self.tokenizer.getTokenNumber() == 32:
            self.stmtSeq = StmtSeqNode(identifiers, tokenizer, inputList)

    def exec(self) :
        self.stmt.exec()
        if hasattr(self, "stmtSeq") : self.stmtSeq.exec()

    def prettyPrint(self, ind) :
        self.stmt.prettyPrint(ind)
        if hasattr(self, "stmtSeq") : self.stmtSeq.prettyPrint(ind)

class DeclNode(Node) :
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList) :
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList

        super().handleSuperflousToken('int')
        self.idList = IDListNode(identifiers, tokenizer, inputList)
        super().handleSuperflousToken(';')

    def exec(self) :
        self.idList.exec()

    def prettyPrint(self, ind) :
        super().indentPrint("int", ind)
        self.idList.prettyPrint(ind)

class IDListNode(Node):
    tokenizer = None
    inputList = None
    identifiers = None
    
    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.id = IDNode(identifiers, tokenizer, inputList, True)
        if super().isTokenPresent(','):
            super().handleSuperflousToken(',')
            self.idList = IDListNode(identifiers, tokenizer, inputList)

    def exec(self):
        result = [self.id.exec()]
        if hasattr(self, "idList"):
            result += self.idList.exec()
        return result

    def prettyPrint(self, ind):
        self.id.prettyPrint(ind)
        if hasattr(self, 'idList'):
            super().indentPrint(",", ind)
            self.idList.prettyPrint(ind)


class StmtNode(Node):
    tokenizer = None
    inputList = None
    identifiers = None
    
    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        if (super().isTokenPresent("if")):
            self.child = IfNode(identifiers, tokenizer, inputList)
        elif (super().isTokenPresent("while")):
            self.child = LoopNode(identifiers, tokenizer, inputList)
        elif (super().isTokenPresent("read")):
            self.child = InNode(identifiers, tokenizer, inputList)
        elif (super().isTokenPresent("write")):
            self.child = OutNode(identifiers, tokenizer, inputList)
        else:
            self.child = AssignNode(identifiers, tokenizer, inputList)
        super().handleSuperflousToken(';')

    def exec(self):
        self.child.exec()

    def prettyPrint(self, ind):
        self.child.prettyPrint(ind)
        self.child.indentPrint(';', ind)


class AssignNode(Node):
    tokenizer = None
    inputList = None
    identifiers = None
    
    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.id = IDNode(identifiers, tokenizer, inputList)
        super().handleSuperflousToken("=")
        self.exp = ExpNode(identifiers, tokenizer, inputList)

    def exec(self):
        self.identifiers[self.id.exec()] = self.exp.exec()

    def prettyPrint(self, ind):
        self.id.prettyPrint(ind)
        super().indentPrint("=", ind)
        self.exp.prettyPrint(ind)


class IfNode(Node):
    tokenizer = None
    inputList = None
    identifiers = None
    
    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        super().handleSuperflousToken('if')
        self.cond = CondNode(identifiers, tokenizer, inputList)
        super().handleSuperflousToken('then')
        self.stmtSeq1 = StmtSeqNode(identifiers, tokenizer, inputList)
        if super().isTokenPresent('else'):
            print("CONSUMED")
            self.getConsume()
            self.stmtSeq2 = StmtSeqNode(identifiers, tokenizer, inputList)
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

class LoopNode(Node):
    def __init__(self, identifiers, tokenizer, inputList):        
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        super().__init__(identifiers, tokenizer, inputList)
        super().handleSuperflousToken("while")
        self.cond = CondNode(self.identifiers, self.tokenizer, self.inputList)
        super().handleSuperflousToken("loop")
        self.stmtSeq = StmtSeqNode(self.identifiers, self.tokenizer, self.inputList)
        super().handleSuperflousToken("end")

    def exec(self):
        while self.cond.exec():
            self.stmtSeq.exec()

    def prettyPrint(self, ind):
        super().indentPrint("while", ind)
        self.cond.prettyPrint(ind)
        super().indentPrint("loop", ind)
        self.stmtSeq.prettyPrint(ind + 1)
        super().indentPrint("end", ind)

class InNode(Node):
    def __init__(self, identifiers, tokenizer, inputList):
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        super().__init__(identifiers, tokenizer, inputList)
        super().handleSuperflousToken("read")
        self.idList = IDListNode(self.identifiers, self.tokenizer, self.inputList)

    def exec(self):
        for identifier in self.idList.exec():
            self.identifiers[identifier] = self.inputList.pop(0)

    def prettyPrint(self, ind):
        super().indentPrint("read", ind)
        self.idList.prettyPrint(ind)

class OutNode(Node):
    def __init__(self, identifiers, tokenizer, inputList):
        self.identifiers = identifiers
        self.tokenizer= tokenizer
        self.inputList = inputList
        super().__init__(identifiers, tokenizer, inputList)
        super().handleSuperflousToken("write")
        self.idList = IDListNode(self.identifiers, self.tokenizer, self.inputList)

    def exec(self):
        for element in self.idList.exec():
            print(f"{element} = {self.identifiers[element]}")

    def prettyPrint(self, ind):
        super().indentPrint("write", ind)
        self.idList.prettyPrint(ind)


class CondNode(Node) :
    identifiers = None
    tokenizer = None
    inputList = None
    def __init__(self, identifiers, tokenizer, inputList) :
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        if self.isTokenPresent("[") :
            self.handleSuperfluousToken("[")
            self.cond1 = CondNode(identifiers, tokenizer, inputList)
            self.logOp = self.getConsume()
            self.cond2 = CondNode(identifiers, tokenizer, inputList)
            self.handleSuperfluousToken("]")
        elif self.isTokenPresent("!") :
            self.notChild = self.getConsume()
            self.cond = CondNode(identifiers, tokenizer, inputList)
        else :
            self.comp = CompNode(identifiers, tokenizer, inputList)

    def exec(self) :
        if hasattr(self, "logOp") :
            return eval(f"{self.cond1.exec()} {self.logOp} {self.cond2.exec()}")
        elif hasattr(self, "notChild") :
            return not self.cond.exec()
        else :
            return self.comp.exec()

    def prettyPrint(self, ind) :
        if hasattr(self, "logOp") :
            self.indentPrint("[", ind)
            self.cond1.prettyPrint(ind)
            self.indentPrint(self.logOp, ind)
            self.cond2.prettyPrint(ind)
            self.indentPrint("]", ind)
        elif hasattr(self, "notChild") :
            self.indentPrint("!", ind)
            self.cond.prettyPrint(ind)
        else :
            self.comp.prettyPrint(ind)

class CompNode(Node) :
    def __init__(self, identifiers, tokenizer, inputList) :
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        super().handleSuperflousToken("(")
        self.op1 = OpNode(identifiers, tokenizer, inputList)
        self.compOp = self.getConsume()
        self.op2 = OpNode(identifiers, tokenizer, inputList)
        super().handleSuperflousToken(")")

    def exec(self) :
        return eval(f"{self.op1.exec()} {self.compOp} {self.op2.exec()}")

    def prettyPrint(self, ind) :
        super().indentPrint("(", ind)
        self.op1.prettyPrint(ind)
        self.indentPrint(self.compOp, ind)
        self.op2.prettyPrint(ind)
        super().indentPrint(")", ind)

class ExpNode(Node):
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        self.fac = FacNode(identifiers, tokenizer, inputList)
        if (super().isTokenPresent("+") or super().isTokenPresent("-")):
            self.mathOp = self.getConsume()
            self.exp = ExpNode(identifiers, tokenizer, inputList)

    def exec(self):
        return eval(f"{self.fac.exec()} {self.mathOp} {self.exp.exec()}") if hasattr(self, "mathOp") else self.fac.exec()

    def prettyPrint(self, ind):
        self.fac.prettyPrint(ind)
        if hasattr(self, "mathOp"):
            self.indentPrint(self.mathOp, ind)
            self.exp.prettyPrint(ind)


class FacNode(Node):
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        self.op = OpNode(identifiers, tokenizer, inputList)
        if (super().isTokenPresent("*")):
            super().handleSuperflousToken("*")
            self.fac = FacNode(identifiers, tokenizer, inputList)

    def exec(self):
        return eval(f"{self.op.exec()} * {self.fac.exec()}") if hasattr(self, "fac") else self.op.exec()

    def prettyPrint(self, ind):
        self.op.prettyPrint(ind)
        if hasattr(self, "fac"):
            self.indentPrint("*", ind)
            self.fac.prettyPrint(ind)


class OpNode(Node):
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        #TODO Factor this out?
        if self.tokenizer.getTokenNumber() == 31:
            self.child = IntNode(identifiers, tokenizer, inputList)
        elif self.tokenizer.getTokenNumber() == 32:
            self.child = IDNode(identifiers, tokenizer, inputList)
        else:
            self.child = ExpNode(identifiers, tokenizer, inputList)

    def exec(self):
        return self.identifiers[self.child.exec()] if isinstance(self.child, IDNode) else self.child.exec()

    def prettyPrint(self, ind):
        if self.child is ExpNode:
            self.indentPrint("(", ind)
            self.child.prettyPrint(ind)
            self.indentPrint(")", ind)
        else:
            self.child.prettyPrint(ind)


class IDNode(Node):
    identifiers = None
    tokenizer = None
    inputList = None

    def __init__(self, identifiers, tokenizer, inputList, boolean: bool = False):
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        self.name = self.tokenizer.getTokenName()
        if boolean:
            self.identifiers[self.name] = "I, " + self.name + " , have been declared but not initialized"
        elif self.name not in self.identifiers:
            raise ValueError(f"ERROR: Use of undeclared identifer {self.name}")
        self.getConsume()

    def exec(self):
        return self.name

    def prettyPrint(self, ind):
        self.indentPrint(self.name, ind)



class IntNode(Node):
    def __init__(self, identifiers, tokenizer, inputList):
        super().__init__(identifiers, tokenizer, inputList)
        self.tokenizer= tokenizer
        self.inputList = inputList
        self.identifiers = identifiers
        self.value = self.tokenizer.getTokenName()
        self.getConsume()

    def exec(self):
        return self.value

    def prettyPrint(self, ind):
        self.indentPrint(self.value, ind)

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 1:
        program_file_name = sys.argv[1]
        if len(sys.argv) > 2:
            input_file_name = sys.argv[2]
    identifiers = {}
    tokenizer = Tokenizer(program_file_name)
    with open(input_file_name, 'r') as input_file: file_contents = input_file.read()
    inputList = file_contents.split()
    ast = ProgramNode(identifiers, tokenizer, inputList)
    ast.prettyPrint(0)
    print('\n---------\n')
    ast.exec()