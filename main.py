import re
from SymbolTable import SymbolTable, HashTable

# Constants for the category ranges
RESERVED_WORDS_RANGE = range(0, 13)
OPERATORS_RANGE = range(13, 24)
SEPARATORS_RANGE = range(24, 32)

# Token categories
RESERVED_WORD = 'Reserved Word'
OPERATOR = 'Operator'
SEPARATOR = 'Separator'
IDENTIFIER = 'Identifier'
CONSTANT = 'Constant'

# Regular expression patterns for tokens
REGEX_IDENTIFIER = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
REGEX_CONSTANT = r'^(0|[+-]?[1-9][0-9]*)$'
REGEX_STRING = r'^".*"$'

# Loads the tokens from the file
def load_tokens(token_file):
    with open(token_file, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

# Generates an entry for the Program Internal Form (PIF)
def genPIF(token, position, pif):
    pif.append((token, position))

# Scans the source code for tokens and categorizes them
def scan_source_code(source_code_file, token_categories, st_identifiers, st_constants, pif):
    with open(source_code_file, 'r') as file:
        source_code = file.read().splitlines()
    
    for line_no, line in enumerate(source_code):
        tokens = re.split('(\W)', line)
        tokens = [token for token in tokens if token.strip() != '']

        for token in tokens:
            # Check if the token is a reserved word, operator, or separator
            if token in token_categories:
                genPIF(token, 0, pif)
            # Check if the token is an identifier or constant and add it to the symbol table
            elif re.match(REGEX_IDENTIFIER, token):
                if not st_identifiers.contains(token):
                    st_identifiers.insert(token, 'id')
                genPIF(token, st_identifiers.get(token), pif)
            elif re.match(REGEX_CONSTANT, token):
                if not st_constants.contains(token):
                    st_constants.insert(token, 'const')
                genPIF(token, st_constants.get(token), pif)
            else:
                print(f"Lexical error at line {line_no + 1}: {token}")
                return False
    return True

# Main program execution
if __name__ == "__main__":
    token_file_path = 'Token.in'  # Update with the correct path
    source_code_path = 'p1.txt'  # Update with the correct path

    # Initialize symbol tables and PIF output list
    st_identifiers = SymbolTable()
    st_constants = SymbolTable()
    pif_output = []

    # Load tokens and scan the source code
    token_categories = load_tokens(token_file_path)
    is_lexically_correct = scan_source_code(source_code_path, token_categories, st_identifiers, st_constants, pif_output)

    # Write PIF and ST to files
    with open('PIF.out', 'w') as pif_file:
        for entry in pif_output:
            pif_file.write(f"{entry[0]} : {entry[1]}\n")

    with open('ST_Identifiers.out', 'w') as st_id_file:
        for identifier in st_identifiers:
            st_id_file.write(f"{identifier} : {st_identifiers.get(identifier)}\n")

    with open('ST_Constants.out', 'w') as st_const_file:
        for constant in st_constants:
            st_const_file.write(f"{constant} : {st_constants.get(constant)}\n")

    if is_lexically_correct:
        print("Source code is lexically correct.")
    else:
        print("There were lexical errors in the source code.")
