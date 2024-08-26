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

    while i < n:
        char = input_string[i]

        # Switch
        match state:
            case 'START':
                if is_letter(char):
                    buffer += char
                    state = 'IDENTIFIER'
                elif is_digit(char):
                    buffer += char
                    state = 'INTEGER'
                elif char.isspace():
                    pass
                else:
                    raise ValueError(f"Caracter inesperado en el inicio: {char}")

            case 'IDENTIFIER':
                if is_letter(char) or is_digit(char):
                    buffer += char
                else:
                    tokens.append(("IDENTIFICADOR", buffer))
                    buffer = ''
                    state = 'START'
                    i -= 1

            case 'INTEGER':
                if is_digit(char):
                    buffer += char
                elif char == '.':
                    buffer += char
                    state = 'REAL'
                else:
                    raise ValueError(f"Se esperaba un punto decimal para números reales en: {char}")

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
                    tokens.append(("REAL", buffer))
                    buffer = ''
                    state = 'START'
                    i -= 1 

        i += 1

    # Manejo de buffer al final de la cadena
    if state == 'IDENTIFIER':
        tokens.append(("IDENTIFICADOR", buffer))
    elif state == 'REAL_NUMBER':
        tokens.append(("REAL", buffer))
    elif state in ['INTEGER', 'REAL']:
        raise ValueError(f"Entrada incompleta o malformada para un número real: {buffer}")

    return tokens

# Ejemplo de uso
input_string = "var1 123.456 var2 789.0"
tokens = lexer(input_string)
print(tokens)