class ElementoPila:
    def __init__(self, valor):
        self.valor = valor

    def __repr__(self):
        return f"{self.__class__.__name__}({self.valor})"

class Terminal(ElementoPila):
    pass

class NoTerminal(ElementoPila):
    pass

class Estado(ElementoPila):
    pass

# Inicialización de la pila con objetos
pila_estados = [Estado(0)]
fila_tokens = [Terminal(0), Terminal(1), Terminal(0), Terminal(2)]
tablaLR = [
    [2, 0, 0, 1],  
    [0, 0, -1, 0],
    [0, 3, 0, 0],  
    [4, 0, 0, 0],  
    [0, 0, -2, 0]  
]
valor_E = 3

pila_estados2 = [Estado(0)]
fila_tokens2 = [Terminal(0), Terminal(1), Terminal(0), Terminal(1), Terminal(0), Terminal(1), Terminal(0), Terminal(1), Terminal(0), Terminal(1), Terminal(0), Terminal(2)]
tablaLR2 = [
    [2, 0, 0, 1],  
    [0, 0, -1, 0],
    [0, 3, -3, 0],  
    [2, 0, 0, 4],  
    [0, 0, -2, 0]  
]
valor_E2 = 3
valor_E2_2 = 2

def analizar_sintactico():
    global pila_estados, fila_tokens
    print(f"Inicio: pila_estados = {pila_estados}, fila_tokens = {fila_tokens}")

    while fila_tokens:
        top_pila = pila_estados[-1].valor
        primer_token = fila_tokens[0].valor if fila_tokens else None  

        accion = tablaLR[top_pila][primer_token] if primer_token is not None else 0

        print(f"Estado actual: {top_pila}, Token actual: {primer_token}, Acción: {accion}")

        if accion > 0:
            pila_estados.append(fila_tokens.pop(0))
            pila_estados.append(Estado(accion))
            print(f"Desplazamiento: agregar {primer_token} a la pila, nueva pila: {pila_estados}, nueva fila: {fila_tokens}")

        elif accion < 0:
            if accion == -1:
                print("Llegamos al estado de aceptación")
                break
            num_eliminar = -accion * valor_E
            pila_estados = pila_estados[:-num_eliminar]
            top_pila = pila_estados[-1].valor
            nuevo_estado = tablaLR[top_pila][valor_E]
            pila_estados.append(NoTerminal(valor_E))
            pila_estados.append(Estado(nuevo_estado))
            print(f"Reducción: eliminar {num_eliminar} elementos, agregar {valor_E} y {nuevo_estado} a la pila, nueva pila: {pila_estados}, nueva fila: {fila_tokens}")

        elif accion == 0:
            print("Error: Estado 0")
            break

def analizar_sintactico2():
    global pila_estados2, fila_tokens2
    print(f"Inicio: pila_estados = {pila_estados2}, fila_tokens = {fila_tokens2}")

    while fila_tokens2:
        top_pila = pila_estados2[-1].valor
        primer_token = fila_tokens2[0].valor if fila_tokens2 else None  

        # Verificar el valor de `primer_token` antes de acceder a la tabla
        if primer_token is None or not (0 <= primer_token < len(tablaLR2[0])):
            print("Error: Token fuera de rango")
            break

        # Verificar el valor de `top_pila` antes de acceder a la tabla
        if not (0 <= top_pila < len(tablaLR2)):
            print(f"Error: Estado fuera de rango. top_pila = {top_pila}, tablaLR2 tiene {len(tablaLR2)} filas.")
            break
        
        accion = tablaLR2[top_pila][primer_token] if primer_token is not None else 0

        print(f"Estado actual: {top_pila}, Token actual: {primer_token}, Acción: {accion}")

        if accion > 0:
            pila_estados2.append(fila_tokens2.pop(0))
            pila_estados2.append(Estado(accion))
            print(f"Desplazamiento: agregar {primer_token} a la pila, nueva pila: {pila_estados2}, nueva fila: {fila_tokens2}")

        elif accion < 0:
            if accion == -1:
                print("Llegamos al estado de aceptación")
                break
            if accion == -3:
                num_eliminar = 2
            elif accion == -2:
                num_eliminar = 6
            else:
                num_eliminar = 0
            
            if len(pila_estados2) < num_eliminar:
                print("Error: La pila está vacía o tiene menos elementos de los necesarios para la reducción")
                break
                
            pila_estados2 = pila_estados2[:-num_eliminar]
            if not pila_estados2:
                print("Error: La pila está vacía después de la reducción")
                break
            top_pila = pila_estados2[-1].valor
            
            # Verificar que `top_pila` y `valor_E2` sean válidos antes de acceder a la tabla
            if not (0 <= top_pila < len(tablaLR2)):
                print(f"Error: Índice fuera de rango para top_pila. top_pila = {top_pila}, tablaLR2 tiene {len(tablaLR2)} filas.")
                break
            if not (0 <= valor_E2 < len(tablaLR2[0])):
                print(f"Error: Índice fuera de rango para valor_E2. valor_E2 = {valor_E2}, tablaLR2 tiene {len(tablaLR2[0])} columnas.")
                break
                
            nuevo_estado = tablaLR2[top_pila][valor_E2]
            pila_estados2.append(NoTerminal(valor_E2))
            pila_estados2.append(Estado(nuevo_estado))
            print(f"Reducción: eliminar {num_eliminar} elementos, agregar {valor_E2} y {nuevo_estado} a la pila, nueva pila: {pila_estados2}, nueva fila: {fila_tokens2}")

        elif accion == 0:
            print("Error: Estado 0")
            break

analizar_sintactico()
analizar_sintactico2()