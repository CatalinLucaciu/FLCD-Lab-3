import re
from SymbolTable import SymbolTable

RESERVED_WORDS_RANGE = range(0, 13)
OPERATORS_RANGE = range(13, 24)
SEPARATORS_RANGE = range(24, 32)

REGEX_IDENTIFIER = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
REGEX_CONSTANT = r'\b\d+\b'

RESERVED_WORD = 'Reserved Word'
OPERATOR = 'Operator'
SEPARATOR = 'Separator'
IDENTIFIER = 'Identifier'
CONSTANT = 'Constant'

def load_tokens(file_path):
    token_categories = {}
    with open(file_path, 'r') as file:
        for index, line in enumerate(file):
            token = line.strip()
            if index in RESERVED_WORDS_RANGE:
                token_categories[token] = RESERVED_WORD
            elif index in OPERATORS_RANGE:
                token_categories[token] = OPERATOR
            elif index in SEPARATORS_RANGE:
                token_categories[token] = SEPARATOR
    return token_categories

def genPIF(token, index):
    print(f"PIF: {token}, {index}")

def scan_source_code(file_path, token_categories, st_identifiers, st_constants):
    with open(file_path, 'r') as file:
        source_code = file.readlines()

    for line_no, line in enumerate(source_code):
        for token in re.finditer('|'.join([REGEX_IDENTIFIER, REGEX_CONSTANT] + [re.escape(t) for t in token_categories.keys()]), line):
            if token.group() in token_categories:
                if token_categories[token.group()] in [RESERVED_WORD, OPERATOR, SEPARATOR]:
                    genPIF(token.group(), 0)
                elif token_categories[token.group()] == IDENTIFIER:
                    if not st_identifiers.contains(token.group()):
                        st_identifiers.insert(token.group(), len(st_identifiers.identifiers.table))
                    genPIF(token.group(), st_identifiers.get(token.group()))
                elif token_categories[token.group()] == CONSTANT:
                    if not st_constants.contains(token.group()):
                        st_constants.insert(token.group(), len(st_constants.identifiers.table))
                    genPIF(token.group(), st_constants.get(token.group()))
                else:
                    print(f"Lexical error at line {line_no+1}, token: {token.group()}")
            else:
                print(f"Lexical error at line {line_no+1}, token: {token.group()}")

if __name__ == "__main__":
    token_file_path = input("").strip()
    source_code_path = input("").strip()

    token_categories = load_tokens(token_file_path)

    st_identifiers = SymbolTable()
    st_constants = SymbolTable()

    scan_source_code(source_code_path, token_categories, st_identifiers, st_constants)


   


