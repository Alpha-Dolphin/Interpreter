import sys
from tokenizer import Tokenizer

class AST :

    def __init__(self, program_file_name, input_file_name):
        AST.tokenizer = Tokenizer(program_file_name)
        # TODO: Make this a delimited list
        AST.inputList = input_file_name

    class Node:
        def __init__(self):
            self.name = type(self).__name__
        
        def printName(self):
            print(self.name)

    class ProgramNode(Node):
        def __init__(self):
            super().__init__()
            self.declSeqNode = AST.DeclSeqNode()
            self.stmtSeqNode = AST.StmtSeqNode()

    class StmtSeqNode(Node):
        def __init__(self):
            super().__init__()

    class DeclSeqNode(Node):
        def __init__(self):
            super().__init__()

    class DeclNode(Node):
        def __init__(self):
            super().__init__()

    class VarListNode(Node):
        def __init__(self):
            super().__init__()

    class StmtNode(Node):
        def __init__(self):
            super().__init__()

    class AssignNode(Node):
        def __init__(self):
            super().__init__()

    class IfNode(Node):
        def __init__(self):
            super().__init__()
            self.condNode = AST.CondNode()
            self.condNode.ParseCond()
            AST.tokenizer.skipToken()
            self.stmtSeqNode1 = AST.StmtSeqNode()
            self.stmtSeqNode1.ParseSS()
            if AST.tokenizer.getToken() == 'end':
                AST.tokenizer.skipToken()
                AST.tokenizer.skipToken()
            else:
                AST.tokenizer.skipToken()
                self.stmtSeqNode2 = AST.StmtSeqNode()
                self.stmtSeqNode2.ParseSS()

    class LoopNode(Node):
        def __init__(self):
            super().__init__()
            self.condNode = AST.CondNode()
            self.stmtSeqNode = AST.StmtSeqNode()

    class InNode(Node):
        def __init__(self):
            super().__init__()
            self.varListNode = AST.VarListNode()

    class OutNode(Node):
        def __init__(self):
            super().__init__()
            self.varListNode = AST.VarListNode()

    class CondNode(Node):
        def __init__(self):
            super().__init__()

    class CompNode(Node):
        def __init__(self):
            super().__init__()
            self.opNode1 = AST.OpNode()
            self.opNode2 = AST.OpNode()

    class OpNode(Node):
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
    # Create prog node
    # All nodes import tokenizer functionality
    # Gettoken, generate app. node, skip token.
    # Abstract parse tree
    # Reccommend OO approach
