from thompson import *
from af_directo import *

def conversion(cadena):
    cadena2 = ""
    operadores_concatenacion = [")", "*", "+", "?"]
    for c in range(len(cadena)):
        cadena2 += cadena[c]    
        if c < len(cadena)-1:
        
            if cadena[c] in operadores_concatenacion and verificador(cadena[c+1]):
                cadena2 += "ß"
            elif verificador(cadena[c]) and cadena[c+1] == "(":
                print(c)
                cadena2 += "ß"

            elif verificador(cadena[c]) and verificador(cadena[c+1]):
                cadena2 += "ß"

            elif cadena[c]== ")" and cadena[c+1]=="(":
                cadena2 += "ß"

            elif cadena[c] =="+" and cadena[c+1] == "(":
                cadena2 += "ß"
            
            elif cadena[c] =="*" and cadena[c+1] == "(":
                cadena2 += "ß"

            elif cadena[c] =="?" and cadena[c+1] == "(":
                cadena2 += "ß"

    return cadena2


def verificador(caracter):
    operadores = ['*', '+','?', 'ß', "|", "(", ")"]
    return caracter not in operadores

bandera = True
while bandera:
    parentesis_abiertos = 0
    parentesis_cerrados = 0
    exp = input("Ingrese la expresion deseada --> ")
    for string in exp:
        if string == "(":
            parentesis_abiertos = parentesis_abiertos +1

        elif string == ")":
            parentesis_cerrados = parentesis_cerrados+1


    if parentesis_abiertos == parentesis_cerrados:
        bandera = False
    else:
        print("La cantidad de parentesis no es la misma")



afn = None
afd = None
alpha = "abcdefghijklmnopqrstuvwxyz0123456789E"
operadores = "*|+?()"

while True:
    print("0. Cambiar expresion regular")
    print("1. AFN utilizando el Algoritmo de Thompson")
    print("2. AFD utilizando el Algoritmo por medio de subconjuntos")
    print("3. Simulacion de AFN")
    print("4. Simulacion de AFD")
    print("5. Af Directo y su simulacion")
    print("6. Salir")
    print("")
    
    opcion = input("Elija una opcion: ")
    
    c = conversion(exp)
    print("Expresión Concatenada: ", c)


    if opcion == "0":
        exp = input("Ingrese la expresion --> ")
        
    elif opcion == "1":
        a = Thompson(c)
        afn = a.compilar()
        a.graficar_afn()

    elif opcion == "2":
        if afn is not None:
            afd = a.subset(afn)
            a.graficar_afd(afd)


    elif opcion == "3":
        try:
            if afn is not None:
                cadena = input("Ingrese la cadena a evaluar: ")
                d = a.simulacion_afn(afn,cadena)
                if d:
                    print("")
                    print("La cadena SI es aceptada")
                    print("")
                else:
                    print("")
                    print("La cadena NO es aceptada: ")
                    print("")
            else:
                print("No se ha creado ningun AFN")
        except:
            print("Cadena no valida")
    
    elif opcion == "4":
        if afd is not None:
            cadena = input("Ingrese la cadena a evaluar: ")
            d = a.simulacion_afd(cadena, afd)
            # ----------------------------------------
            if d:
                print("")
                print("La cadena SI es aceptada")
                print("")
            else:
                print("")
                print("La cadena NO es aceptada")
                print("")
        else:
            print("No se ha creado ningun AFD")
            


    elif opcion == "5":
        print("--- AF Directo ---")
        bandera = False
        for i in exp:
            if i not in alpha and i not in operadores:
                print("Input invalido")
                bandera = True
                break
        
        if not bandera:
            cadena = input("Ingrese la cadena que deesea evaluar: ")
            print("")

            automata_nuevo = Directo(exp)

            estados = {state.signo for state in automata_nuevo.estados}
            estado_inicial = automata_nuevo.estado0
            estados_aceoatacion_finales = {state for state in automata_nuevo.estdosAceptacion}
            trans_func = trans_func_afd(automata_nuevo.transiciones)
            verifiacacion_validez = simulacion_directo(cadena, estado_inicial, estados_aceoatacion_finales, automata_nuevo.transiciones)
            print("La cadena es aceptada por el AFD --> ", verifiacacion_validez)
            print('---------------------------------------------------------------')
            print("Estados del AFN --> ", estados)
            print('---------------------------------------------------------------')
            print("Estado Inicial --> ", estado_inicial)
            print('---------------------------------------------------------------')
            print("Estados de aceptacion --> ", estados_aceoatacion_finales)
            print('---------------------------------------------------------------')
            graficador_directo(estados, estado_inicial, estados_aceoatacion_finales, trans_func, "FinalDirecto")


    elif opcion == "6":
        break
