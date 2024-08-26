def is_letter(char):
    return char.isalpha()

def is_digit(char):
    return char.isdigit()

def lexer(input_string):
    i = 0
    n = len(input_string)
    tokens = []
    buffer = ''
    state = 'START'

    # Bucle principal del analizador léxico
    while i < n:
        char = input_string[i]

        # Uso de match/case para manejar los estados
        match state:
            case 'START':
                if is_letter(char):
                    buffer += char
                    state = 'IDENTIFIER'
                elif is_digit(char):
                    buffer += char
                    state = 'INTEGER'
                elif char == '"':
                    buffer += char
                    state = 'STRING'
                elif char.isspace():
                    pass  # Ignora los espacios en blanco
                elif char in "+-":
                    tokens.append(("opSuma", 5))
                elif char in "*/":
                    tokens.append(("opMul", 6))
                elif char in "<>":
                    buffer += char
                    state = 'RELATIONAL_OPERATOR'
                elif char in "|":
                    buffer += char
                    state = 'OR_OPERATOR'
                elif char in "&":
                    buffer += char
                    state = 'AND_OPERATOR'
                elif char == "!":
                    buffer += char
                    state = 'NOT_OPERATOR'
                elif char == "=":
                    buffer += char
                    state = 'EQUALITY_OPERATOR'
                elif char in ";":
                    tokens.append((";", 12))
                elif char in ",":
                    tokens.append((",", 13))
                elif char in "(":
                    tokens.append(("(", 14))
                elif char in ")":
                    tokens.append((")", 15))
                elif char in "{":
                    tokens.append(("{", 16))
                elif char in "}":
                    tokens.append(("}", 17))
                elif char == "$":
                    tokens.append(("$", 23))
                else:
                    raise ValueError(f"Caracter inesperado: {char}")

            case 'IDENTIFIER':
                if is_letter(char) or is_digit(char):
                    buffer += char
                else:
                    if buffer in ["int", "float", "void"]:
                        tokens.append(("tipo", 4))
                    elif buffer in ["if", "while", "return", "else"]:
                        tokens.append((buffer, {"if": 19, "while": 20, "return": 21, "else": 22}[buffer]))
                    else:
                        tokens.append(("identificador", 0))
                    buffer = ''
                    state = 'START'
                    i -= 1  # Retrocede para reanalizar este carácter con el estado inicial

            case 'INTEGER':
                if is_digit(char):
                    buffer += char
                elif char == '.':
                    buffer += char
                    state = 'REAL'
                else:
                    tokens.append(("entero", 1))
                    buffer = ''
                    state = 'START'
                    i -= 1  # Retrocede para reanalizar este carácter con el estado inicial

            case 'REAL':
                if is_digit(char):
                    buffer += char
                    state = 'REAL_NUMBER'
                else:
                    raise ValueError(f"Se esperaba un dígito después del punto decimal en: {char}")

            case 'REAL_NUMBER':
                if is_digit(char):
                    buffer += char
                else:
                    tokens.append(("real", 2))
                    buffer = ''
                    state = 'START'
                    i -= 1  # Retrocede para reanalizar este carácter con el estado inicial

            case 'STRING':
                buffer += char
                if char == '"':
                    tokens.append(("cadena", 3))
                    buffer = ''
                    state = 'START'

            case 'RELATIONAL_OPERATOR':
                if char == '=':
                    buffer += char
                    tokens.append(("opRelac", 7))
                else:
                    tokens.append(("opRelac", 7))
                    i -= 1
                buffer = ''
                state = 'START'

            case 'OR_OPERATOR':
                if char == '|':
                    buffer += char
                    tokens.append(("opOr", 8))
                else:
                    raise ValueError(f"Operador '|' incompleto: {buffer}")
                buffer = ''
                state = 'START'

            case 'AND_OPERATOR':
                if char == '&':
                    buffer += char
                    tokens.append(("opAnd", 9))
                else:
                    raise ValueError(f"Operador '&' incompleto: {buffer}")
                buffer = ''
                state = 'START'

            case 'NOT_OPERATOR':
                if char == '=':
                    buffer += char
                    tokens.append(("opIgualdad", 11))
                else:
                    tokens.append(("opNot", 10))
                    i -= 1
                buffer = ''
                state = 'START'

            case 'EQUALITY_OPERATOR':
                if char == '=':
                    buffer += char
                    tokens.append(("opIgualdad", 11))
                else:
                    tokens.append(("=", 18))
                    i -= 1
                buffer = ''
                state = 'START'

        i += 1

    # Manejo de buffer al final de la cadena
    if state == 'IDENTIFIER':
        if buffer in ["int", "float", "void"]:
            tokens.append(("tipo", 4))
        elif buffer in ["if", "while", "return", "else"]:
            tokens.append((buffer, {"if": 19, "while": 20, "return": 21, "else": 22}[buffer]))
        else:
            tokens.append(("identificador", 0))
    elif state == 'REAL_NUMBER':
        tokens.append(("real", 2))
    elif state == 'INTEGER':
        tokens.append(("entero", 1))
    elif state == 'STRING':
        tokens.append(("cadena", 3))
    elif state in ['REAL', 'RELATIONAL_OPERATOR', 'OR_OPERATOR', 'AND_OPERATOR', 'NOT_OPERATOR', 'EQUALITY_OPERATOR']:
        raise ValueError(f"Entrada incompleta o malformada: {buffer}")

    return tokens

# Ejemplo de uso
input_string = 'var1 12 123.456 "hello" int + - * / < <= > >= || && ! == != ; , ( ) { } = if while return else $'
tokens = lexer(input_string)
print(tokens)