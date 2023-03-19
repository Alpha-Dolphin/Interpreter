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
        
        def isRightNode(self) :
            print()

        def throwError(self) :
            raise ValueError("Error: Position %s - Node Type %s - Token %s", AST.tokenizer.currPos, type(self).__name__, AST.tokenizer.getToken)

    class ProgramNode(Node):
        def __init__(self):
            super().__init__()
            self.isRightNode()
            self.declSeqNode = AST.DeclSeqNode()
            if (AST.tokenizer.getToken != "begin") : self.throwError()
            AST.tokenizer.skipToken
            self.stmtSeqNode = AST.StmtSeqNode()
            if (AST.tokenizer.getToken != "end") : self.throwError()

    class StmtSeqNode(Node):
        def __init__(self):
            super().__init__()
            self.isRightNode()
            self.stmtNode = AST.StmtNode()
            if (AST.tokenizer.getToken == 'end') :
                AST.tokenizer.skipToken
                self.stmtSeqNode = AST.StmtSeqNode()
            else :
                AST.tokenizer.skipToken

    class DeclSeqNode(Node):
        def __init__(self):
            super().__init__()
            self.declNode = AST.DeclNode()
            if (AST.tokenizer.getToken == ',') :
                AST.tokenizer.skipToken
                self.declSeqNode = AST.DeclSeqNode()
            else :
                AST.tokenizer.skipToken

    class DeclNode(Node):
        def __init__(self):
            super().__init__()
            self.idList = AST.IDListNode()

    class IDListNode(Node):
        def __init__(self):
            super().__init__()
            self.idNode = AST.IDNode()
            if (AST.tokenizer.getToken == ',') :
                AST.tokenizer.skipToken
                self.idListNode = AST.IDListNode()
            else :
                AST.tokenizer.skipToken

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
            AST.tokenizer.skipToken()
            self.stmtSeqNode1 = AST.StmtSeqNode()
            if AST.tokenizer.getToken() == 'end':
                AST.tokenizer.skipToken()
                AST.tokenizer.skipToken()
            else:
                AST.tokenizer.skipToken()
                self.stmtSeqNode2 = AST.StmtSeqNode()

    class LoopNode(Node):
        def __init__(self):
            super().__init__()

    class InNode(Node):
        def __init__(self):
            super().__init__()

    class OutNode(Node):
        def __init__(self):
            super().__init__()

    class CondNode(Node):
        def __init__(self):
            super().__init__()

    class CompNode(Node):
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
    # Create prog node
    # All nodes import tokenizer functionality
    # Gettoken, generate app. node, skip token.
    # Abstract parse tree
    # Reccommend OO approach
