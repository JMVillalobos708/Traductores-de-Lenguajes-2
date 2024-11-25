import scanner
import parser

def main():
    parsing_table = parser.cargar_tabla_parsing('compilador.csv')

    codigo = input("Introduce el código para analizar: ") + "$"
    tokens = scanner.obtener_tokens(codigo)

    acepted = parser.analizar(tokens, parsing_table)  
    if acepted:
        print("Sintaxis correcta")
    else:
        print("Error de sintaxis")

if __name__ == '__main__':
    main()