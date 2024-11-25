import tkinter as tk
from tkinter import scrolledtext
import csv
import tkinter.messagebox as messagebox

def analizador(cadena):
    elementos = []
    estado = 0
    indice = 0
    cadena = cadena + '$'
    
    while indice <= (len(cadena) - 1) and estado == 0:
        lexema = ''
        token = 'Error'
        identifier = 32
        
        while indice <= (len(cadena) - 1) and estado != 20:
            if estado == 0:
                if cadena[indice].isspace():
                    estado = 0
                elif cadena[indice].isalpha() or cadena[indice] == '_':
                    estado = 4
                    lexema += cadena[indice]
                    token = 'id'
                    identifier = 0  # Identificador para 'id'
                elif cadena[indice] == ';':
                    estado = 20
                    lexema += cadena[indice]
                    token = ';'
                    identifier = 12
                elif cadena[indice] == ',':
                    estado = 20
                    lexema += cadena[indice]
                    token = ','
                    identifier = 13
                elif cadena[indice] == '(':
                    estado = 20
                    lexema += cadena[indice]
                    token = '('
                    identifier = 14
                elif cadena[indice] == ')':
                    estado = 20
                    lexema += cadena[indice]
                    token = ')'
                    identifier = 15
                elif cadena[indice] == '{':
                    estado = 20
                    lexema += cadena[indice]
                    token = '{'
                    identifier = 16
                elif cadena[indice] == '}':
                    estado = 20
                    lexema += cadena[indice]
                    token = '}'
                    identifier = 17
                elif cadena[indice] == '=':
                    estado = 5
                    lexema += cadena[indice]
                    token = '='
                    identifier = 18
                elif cadena[indice].isdigit():
                    estado = 6
                    lexema += cadena[indice]
                    token = 'Constante'
                    identifier = 13
                elif cadena[indice] == '+' or cadena[indice] == '-':
                    estado = 20
                    lexema += cadena[indice]
                    token = 'opSuma'
                    identifier = 5
                elif cadena[indice] == '|' or cadena[indice] == '&':
                    estado = 7
                    lexema += cadena[indice]
                    token = 'Op_logico'
                    identifier = 14
                elif cadena[indice] == '*' or cadena[indice] == '/':
                    estado = 20
                    lexema += cadena[indice]
                    token = 'opMul'
                    identifier = 6
                elif cadena[indice] == '<' or cadena[indice] == '>':
                    estado = 8
                    lexema += cadena[indice]
                    token = 'opRelac'
                    identifier = 7
                elif cadena[indice] == '!':
                    estado = 9
                    lexema += cadena[indice]
                    token = 'opNot'
                    identifier = 10
                elif cadena[indice] == '$':
                    estado = 20
                    lexema += cadena[indice]
                    token = '$'
                    identifier = 23
                else:
                    estado = 20
                    token = 'error'
                    lexema = cadena[indice]
                indice += 1
            elif estado == 4:
                if cadena[indice].isdigit() or cadena[indice].isalpha() or cadena[indice] == '_':
                    estado = 4
                    lexema += cadena[indice]
                    token = 'id'
                    identifier = 0
                    indice += 1
                else:
                    estado = 20
            elif estado == 5:
                if cadena[indice] != '=':
                    estado = 20
                else:
                    estado = 20
                    lexema += cadena[indice]
                    token = 'opIgualdad'
                    identifier = 11
                    indice += 1
            elif estado == 6:
                if cadena[indice].isdigit():
                    estado = 6
                    lexema += cadena[indice]
                    token = 'Constante'
                    identifier = 13
                    indice += 1
                else:
                    estado = 20
            elif estado == 7:
                if cadena[indice] == '|' or cadena[indice] == '&':
                    estado = 20
                    lexema += cadena[indice]
                    token = 'Op_logico'
                    identifier = 14
                    indice += 1
                else:
                    estado = 20
            elif estado == 8:
                if cadena[indice] == '=':
                    estado = 20
                    lexema += cadena[indice]
                    token = 'opRelac'
                    identifier = 7
                    indice += 1
                else:
                    estado = 20
            elif estado == 9:
                if cadena[indice] == '=':
                    estado = 20
                    lexema += cadena[indice]
                    token = 'opIgualdad'
                    identifier = 11
                    indice += 1
                else:
                    estado = 20

        estado = 0
        elementos.append({'token': token, 'lexema': lexema, 'identifier': identifier})

    # Asignar tokens y identifiers para palabras clave
    for elemento in elementos:
        if elemento['lexema'] in ["int", "float", "char", "void"]:
            elemento['token'] = "tipo"
            elemento['identifier'] = 4
        elif elemento['lexema'] == "if":
            elemento['token'] = "if"
            elemento['identifier'] = 19
        elif elemento['lexema'] == "while":
            elemento['token'] = "while"
            elemento['identifier'] = 20
        elif elemento['lexema'] == "return":
            elemento['token'] = "return"
            elemento['identifier'] = 21
        elif elemento['lexema'] == "else":
            elemento['token'] = "else"
            elemento['identifier'] = 22

    return elementos

# Función para analizar el código
def analizar_codigo():
    codigo = codigo_text.get("1.0", "end-1c")
    resultados = analizador(codigo)
    resultado_text.config(state="normal")
    resultado_text.delete("1.0", "end")
    
    # Cargar reglas y tabla (omitido aquí, asumiendo que ya lo tienes)
    archivo_reglas = "GR2slrRulesId.txt"
    archivo_tabla = "GR2slrRulesId.txt"
    reglas = []
    tabla = []

    with open(archivo_reglas, newline='') as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            fila = [int(element) for element in row]
            reglas.append(fila)
    
    with open(archivo_tabla, newline='') as file:
        csv_reader = csv.reader(file, delimiter="\t")
        for row in csv_reader:
            fila = [int(element) for element in row]
            tabla.append(fila)
    
    for row in tabla:
        del row[0]

    for elemento in resultados:
        resultado_text.insert("end", f"|Token: {elemento['token']} |Lexema: {elemento['lexema']} |Identifier: {elemento['identifier']}\n")
    
    analisis_sintactico = analizador_sintactico(resultados, reglas, tabla)
    resultado_text.config(state="disabled")

    mostrar_popup(analisis_sintactico)

def analizador_sintactico(tokens, reglas, tabla):
    pila = [0]
    cola_tokens = [entry['identifier'] for entry in tokens]

    while cola_tokens:
        estado = pila[-1]
        entrada = cola_tokens[0]
        accion = tabla[estado][entrada]
        if accion > 0:
            del cola_tokens[0]
            pila.append(entrada)
            pila.append(accion)
        elif accion < 0:
            accion = (accion * -1) - 1
            if accion == 0:
                print("Válido")
                return True
            regla = reglas[accion]
            try:
                num_pop = regla[1] * 2

                for i in range(num_pop):
                    pila.pop()

                estado = tabla[pila[-1]][regla[0]]
                pila.append(regla[0])
                pila.append(estado)
            except:
                print("Archivo de reglas erróneo")
        else:
            return False
    return False

def mostrar_popup(resultado):
    if resultado:
        messagebox.showinfo("Resultado", "Código Válido")
    else:
        messagebox.showerror("Resultado", "Código inválido")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador Léxico")

# Etiqueta para el código fuente
codigo_label = tk.Label(ventana, text="Ingresa el código fuente:")
codigo_label.pack()

# Caja de texto para el código fuente
codigo_text = scrolledtext.ScrolledText(ventana, width=50, height=10)
codigo_text.pack()

# Botón de análisis
analizar_button = tk.Button(ventana, text="Analizar", command=analizar_codigo)
analizar_button.pack()

# Caja de texto para mostrar resultados
resultado_label = tk.Label(ventana, text="Resultados:")
resultado_label.pack()

resultado_text = scrolledtext.ScrolledText(ventana, width=50, height=10)
resultado_text.pack()

ventana.mainloop()
