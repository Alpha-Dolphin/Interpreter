import sys
from tokenizer import Tokenizer

class AST :
    def __init__(self, program_file_name, input_file_name):
        self.tokenizer = Tokenizer(program_file_name)
        #TODO : Make this a delimited list
        self.inputList = input_file_name
    
    class Node:
        def __init__(self, name):
            self.name = name
        
        def printName(self) :
            print(self.name)

    class ProgramNode(Node):
        def __init__(self):
            super().__init__("ProgramNode")
            self.declSeqNode = None
            self.stmtSeqNode = None

    class DeclSeqNode(Node):
        def __init__(self):
            super().__init__("DeclSeqNode")

    class StmtSeqNode(Node):
        def __init__(self):
            super().__init__("StmtSeqNode")

    class DeclNode(Node):
        def __init__(self, varList):
            super().__init__("DeclNode")

    class VarListNode(Node):
        def __init__(self, varName):
            super().__init__("VarListNode")

    class StmtNode(Node):
        def __init__(self, name):
            super().__init__(name)

    class AssignNode(Node):
        def __init__(self, varName, expNode):
            super().__init__("AssignNode")

    class IfNode(Node):
        def __init__(self, condNode, stmtSeqNode1, stmtSeqNode2):
            super().__init__("IfNode")
            self.condNode = CondNode(condNode)
            self.condNode.ParseCond()
            self.tokenizer
            self.stmtSeqNode1 = StmtSeqNode(stmtSeqNode1)
            self.stmtSeqNode2 = StmtSeqNode(stmtSeqNode2)

    class LoopNode(Node):
        def __init__(self, condNode, stmtSeqNode):
            super().__init__("LoopNode")

    class InNode(Node):
        def __init__(self, varList):
            super().__init__("InNode")

    class OutNode(Node):
        def __init__(self, varList):
            super().__init__("OutNode")

    class CondNode(Node):
        def __init__(self, name):
            super().__init__(name)

    class CompNode(Node):
        def __init__(self, opNode1, compOpNode, opNode2):
            super().__init__("CompNode")

    
if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 2:
        input_file_name = sys.argv[2]
        if len(sys.argv) > 1:
            program_file_name = sys.argv[1]
    ast = AST(program_file_name, input_file_name)
    # Create prog node
    # All nodes import tokenizer functionality
    # Gettoken, generate app. node, skip token.
    # Abstract parse tree
    # Reccommend OO approach