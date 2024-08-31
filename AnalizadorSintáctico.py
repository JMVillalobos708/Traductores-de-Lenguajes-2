pila_estados = [0]
fila_tokens = [0, 1, 0, 2]
tablaLR = [
    [2, 0, 0, 1],  
    [0, 0, -1, 0],
    [0, 3, 0, 0],  
    [4, 0, 0, 0],  
    [0, 0, -2, 0]  
]
valor_E = 3

pila_estados2 = [0]
fila_tokens2 = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 2]
tablaLR2 = [
    [2, 0, 0, 1],  
    [0, 0, -1, 0],
    [0, 3, -3, 0],  
    [2, 0, 0, 4],  
    [0, 0, -2, 0]  
]
valor_E2 = (3)*2
valor_E2_2 = 2


def analizar_sintactico():
    global pila_estados, fila_tokens
    print(f"Inicio: pila_estados = {pila_estados}, fila_tokens = {fila_tokens}")

    while fila_tokens != 0: 
        top_pila = pila_estados[-1] 
        #print(top_pila)
        primer_token = fila_tokens[0] if fila_tokens else None  

        accion = tablaLR[top_pila][primer_token] if primer_token is not None else 0

        print(f"Estado actual: {top_pila}, Token actual: {primer_token}, Acción: {accion}")

        if accion > 0:
            pila_estados.append(primer_token) 
            fila_tokens.pop(0) 
            pila_estados.append(accion) 
            print(f"Desplazamiento: agregar {primer_token} a la pila, nueva pila: {pila_estados}, nueva fila: {fila_tokens}")

        elif accion < 0 and ( accion != -1):
            num_eliminar = -accion * valor_E
            pila_estados = pila_estados[:-num_eliminar]
            top_pila = pila_estados[-1]
            nuevo_estado = tablaLR[top_pila][valor_E]
            pila_estados.append(valor_E)
            pila_estados.append(nuevo_estado) 
            print(f"Reducción: eliminar {num_eliminar} elementos, agregar {valor_E} y {nuevo_estado} a la pila, nueva pila: {pila_estados}, nueva fila: {fila_tokens}")

        elif accion == 0:
            print("Error: Estado 0")
            break
        
        elif accion == -1: 
            print("Llegamos al estado de aceptación")
            break

def analizar_sintactico2():
    global pila_estados2, fila_tokens2
    print(f"Inicio: pila_estados = {pila_estados2}, fila_tokens = {fila_tokens2}")

    while fila_tokens2:
        top_pila = pila_estados2[-1] 
        primer_token = fila_tokens2[0] if fila_tokens2 else None  

        accion = tablaLR2[top_pila][primer_token] if primer_token is not None else 0

        print(f"Estado actual: {top_pila}, Token actual: {primer_token}, Acción: {accion}")

        if accion > 0:
            pila_estados2.append(primer_token) 
            fila_tokens2.pop(0) 
            pila_estados2.append(accion) 
            print(f"Desplazamiento: agregar {primer_token} a la pila, nueva pila: {pila_estados2}, nueva fila: {fila_tokens2}")

        elif accion < 0:
            if accion == -1: 
                print("Llegamos al estado de aceptación")
                break
            if accion == -3:
                num_eliminar = 2
            elif accion == -2:
                num_eliminar = 6
            pila_estados2 = pila_estados2[:-num_eliminar] 
            top_pila = pila_estados2[-1]
            nuevo_estado = tablaLR2[top_pila][valor_E]
            pila_estados2.append(valor_E)
            pila_estados2.append(nuevo_estado)
            print(f"Reducción: eliminar {num_eliminar} elementos, agregar {valor_E} y {nuevo_estado} a la pila, nueva pila: {pila_estados2}, nueva fila: {fila_tokens2}")

        elif accion == 0:
            print("Error: Estado 0")
            break

analizar_sintactico()
analizar_sintactico2()