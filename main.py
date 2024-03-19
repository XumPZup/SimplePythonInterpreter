import minipar.parser as par
import minipar.lexer as lex
import minipar.interpreter as inter
import sys
import os

# Test for MiniPar
def read_program(file_path):
    with open(file_path, 'r') as file:
        program = file.read()
    return program

def main():
    # Verify if the command has two argumets as expected
    if len(sys.argv) != 2:
        print("Use: python main.py <path/to/your/file.mini>")
        sys.exit(1)

    program_file = sys.argv[1]

    # Verify if the file exists
    if not os.path.exists(program_file):
        print(f"Error: The file '{program_file}' was not found.")
        sys.exit(1)
    
    # Read program
    input_program = read_program(program_file)
    
    lexer = lex.lexer
    result = par.parser.parse(input_program, lexer=lexer)
    
    if result:
        if not inter.has_error:
            inter.run_stmt(result)
        else:
            pass

if __name__ == "__main__":
    main()
