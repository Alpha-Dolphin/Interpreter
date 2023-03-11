import sys
from tokenizer import Tokenizer

def parse(tokenizer) :
    for entry in tokenizer :
        entry = entry

if __name__ == '__main__':
    program_file_name = "debug.txt"
    input_file_name = "input.txt"
    if len(sys.argv) > 2:
        program_file_name = sys.argv[1]
        input_file_name = sys.argv[2]
    tokenizer = Tokenizer(program_file_name)
    ast = parse(tokenizer)
    # Create prog node
    # All nodes import tokenizer functionality
    # Gettoken, generate app. node, skip token.
    # Abstract parse tree
    # Reccommend OO approach