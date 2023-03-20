class AFN:
    def __init__(self, estados, alfabeto, transicion ):
        self.estados = estados 
        self.alfabeto = alfabeto
        self.transicion = transicion 

class Transicion: 
    def __init__(self, destino, caracter):
        self.destino = destino
        self.caracter = caracter 

class Estado:
    def __init__(self, etiqueta, transiciones,tipo):
        self.etiqueta = etiqueta 
        self.transiciones = transiciones 
        self.tipo = tipo 
