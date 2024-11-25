import pandas as pd
import scanner

def cargar_tabla_parsing(ruta_archivo):
    parsing_table = pd.read_csv(ruta_archivo, index_col=0)
    parsing_table = parsing_table.astype(object)
    parsing_table.fillna("error", inplace=True)
    return parsing_table

reducciones = {
    1: ('programa', 1),
    2: ('Definiciones', 0),
    3: ('Definiciones', 2),
    4: ('Definicion', 1),
    5: ('Definicion', 1),
    6: ('DefVar', 4),
    7: ('ListaVar', 0),
    8: ('ListaVar', 3),
    9: ('DefFunc', 6),
    10: ('Parametros', 0),
    11: ('Parametros', 3),
    12: ('ListaParam', 0),
    13: ('ListaParam', 4),
    14: ('BloqFunc', 3),
    15: ('DefLocales', 0),
    16: ('DefLocales', 2),
    17: ('DefLocal', 1),
    18: ('DefLocal', 1),
    19: ('Sentencias', 0),
    20: ('Sentencias', 2),
    21: ('Sentencia', 4),
    22: ('Sentencia', 6),
    23: ('Sentencia', 5),
    24: ('Sentencia', 3),
    25: ('Sentencia', 2),
    26: ('Otro', 0),
    27: ('Otro', 2),
    28: ('Bloque', 3),
    29: ('ValorRegresa', 0),
    30: ('ValorRegresa', 1),
    31: ('Argumentos', 0),
    32: ('Argumentos', 2),
    33: ('ListaArgumentos', 0),
    34: ('ListaArgumentos', 3),
    35: ('Termino', 1),
    36: ('Termino', 1),
    37: ('Termino', 1),
    38: ('Termino', 1),
    39: ('Termino', 1),
    40: ('LlamadaFunc', 4),
    41: ('SentenciaBloque', 1),
    42: ('SentenciaBloque', 1),
    43: ('Expresion', 3),
    44: ('Expresion', 2),
    45: ('Expresion', 2),
    46: ('Expresion', 3),
    47: ('Expresion', 3),
    48: ('Expresion', 3),
    49: ('Expresion', 3),
    50: ('Expresion', 3),
    51: ('Expresion', 3),
    52: ('Expresion', 1)
}

class Pila:
    def __init__(self):
        self.pila = []
    
    def push(self, elemento):
        self.pila.append(elemento)
    
    def pop(self):
        return self.pila.pop()
    
    def top(self):
        return self.pila[-1]

def analizar(tokens, parsing_table):
    pila = Pila()
    pila.push(0)
    i = 0
    longitud = len(tokens)
    acepted = False

    while i < longitud:
        print(f"Pila actual: {pila.pila}")
        token = tokens[i]
        estado = pila.top()

        try:
            accion = parsing_table.loc[estado, token.simbolo]
        except KeyError:
            print(f"Error: No se encontró el símbolo '{token.simbolo}' en el estado {estado}.")
            break
        
        if accion == 'r0':
            acepted = True
            break	
        elif accion[0] == 'd': 
            pila.push(token.simbolo)
            pila.push(int(accion[1:]))
            if token.simbolo != '$':
                i += 1
        elif accion[0] == 'r':
            regla = int(accion[1:])
            no_terminal, num_elementos = reducciones[regla]
            for _ in range(num_elementos * 2):
                pila.pop()
            estado = pila.top()
            pila.push(no_terminal)
            pila.push(int(parsing_table.loc[estado, no_terminal]))
        else:
            print(f"Error: No se encontró acción para el token {token.simbolo}")
            break
    
    return acepted

if __name__ == '__main__':
    parsing_table = cargar_tabla_parsing('compilador.csv')

    codigo = input("Introduce el código para analizar: ") + "$"
    tokens = scanner.obtener_tokens(codigo)
    acepted = analizar(tokens, parsing_table)
    if acepted:
        print("Sintaxis correcta")
    else:
        print("Error de sintaxis")
