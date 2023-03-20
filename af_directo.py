from utilidades_directo import *
from regex import *
from afd import *
import graphviz 

alpha = "abcdefghijklmnopqrstuvwxyz0123456789E#"

class Directo:
    def __init__(self, expresion):
        self.estados = []
        self.estado0 = None
        self.estadoF = None
        self.estdosAceptacion = []
        self.transiciones = []
        self.alpha = []
        self.nombre = 0
        self.n_utilizados = 0
        self.arbol = 0
        self.nodos = []
        self.posiciones = {}
        self.epicentro = None

        regular_exp_mod = cambio_expresion(expresion, 2)
        regular_exp_mod = add2(regular_exp_mod)
        self.arbol_stx(regular_exp_mod)

        for x in self.nodos:
            if x.signo == '#':
                self.estadoF = x.arbol
                break

        self.gettear_siguientes_posiciones()
        self.repetir_directo()

    def definicion_de_nombre(self):
        possible_names = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
        name = possible_names[self.nombre]
        self.nombre += 1
        if self.nombre == len(possible_names):
            self.n_utilizados += 1
            self.nombre = 0
        return name + str(self.n_utilizados)


    def precedencia_doble(self, first, second):
        pre_fir = precedencia_op(first)
        pre_sec = precedencia_op(second)
        return pre_fir >= pre_sec


    def arbol_stx(self, expresion):
        caracteres = []
        operadores = []
        for i in expresion:
            if i in alpha:
                caracteres.append(i)
            elif i == "(":
                operadores.append(i)
            elif i == ")":
                caracter_final = operadores[-1] if operadores else None
                while caracter_final is not None and caracter_final[0] != "(":
                    epi = self.gettear_op_chars(operadores, caracteres)
                    caracteres.append(epi)
                    caracter_final = operadores[-1] if operadores else None
                operadores.pop()

            else:
                caracter_final = operadores[-1] if operadores else None
                while caracter_final is not None and caracter_final not in "()" and self.precedencia_doble(caracter_final, i):
                    epi = self.gettear_op_chars(operadores, caracteres)
                    caracteres.append(epi)
                    caracter_final = operadores[-1] if operadores else None
                operadores.append(i)

        final = self.gettear_op_chars(operadores, caracteres)
        caracteres.append(final)
        self.epicentro = caracteres.pop()

    def gettear_op_chars(self, operadores, caracteres):
        op = operadores.pop()
        derecha = caracteres.pop()
        izquierda = None
        if (derecha not in self.alpha) and (derecha != "Ɛ") and (derecha !=  "#") and (derecha is not None):
            self.alpha.append(derecha)
        if op != "*":
            izquierda = caracteres.pop()
            if (izquierda not in self.alpha) and (izquierda != "Ɛ") and (izquierda !=  "#") and (izquierda is not None):
                self.alpha.append(izquierda)
        if op == "|" or op == "-": return self.OR_AND(izquierda, derecha, op)
        elif op == "*": return self.kleene_directo(derecha)

    def OR_AND(self, izquierdo, derecho, operador):
        if (type(izquierdo) == Central) and (type(derecho) == Central):
            if operador == "|":
                fuente = Central(operador, None, True, [izquierdo, derecho], izquierdo.verificador or derecho.verificador)
                self.nodos += [fuente]
                return fuente
            elif operador == "-":
                fuente = Central(operador, None, True, [izquierdo, derecho], izquierdo.verificador and derecho.verificador)
                self.nodos += [fuente]
                return fuente


        elif (type(izquierdo) != Central) and (type(derecho) != Central):
            if operador == "|":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "Ɛ" else None
                etiqueta_derecha = self.arbol + 2  if derecho not in "Ɛ" else None
                self.arbol = self.arbol + 2
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [nodo_izquierdo, nodo_derecho], nodo_izquierdo.verificador or nodo_derecho.verificador)
                self.nodos += [nodo_izquierdo, nodo_derecho, fuente]
                return fuente
            elif operador == "-":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "Ɛ" else None
                etiqueta_derecha = self.arbol + 2  if derecho not in "Ɛ" else None
                self.arbol = self.arbol + 2
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [nodo_izquierdo, nodo_derecho], nodo_izquierdo.verificador and nodo_derecho.verificador)
                self.nodos += [nodo_izquierdo, nodo_derecho, fuente]
                return fuente

        elif (type(izquierdo) == Central) and (type(derecho) != Central):
            if operador == "|":
                etiqueta_derecha = self.arbol + 1  if derecho not in "Ɛ" else None
                self.arbol = self.arbol + 1
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [izquierdo, nodo_derecho], izquierdo.verificador or nodo_derecho.verificador)
                self.nodos += [nodo_derecho, fuente]
                return fuente
            elif operador == "-":
                etiqueta_derecha = self.arbol + 1  if derecho not in "Ɛ" else None
                self.arbol = self.arbol + 1
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [izquierdo, nodo_derecho], izquierdo.verificador and nodo_derecho.verificador)
                self.nodos += [nodo_derecho, fuente]
                return fuente


        elif (type(izquierdo) != Central) and (type(derecho) == Central):
            if operador == "|":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "Ɛ" else None
                self.arbol = self.arbol + 1
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                fuente = Central(operador   , None, True, [nodo_izquierdo, derecho], nodo_izquierdo.verificador or derecho.verificador)
                self.nodos += [nodo_izquierdo, fuente]
                return fuente

            elif operador == "-":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "Ɛ" else None
                self.arbol = self.arbol + 1
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                fuente = Central(operador, None, True, [nodo_izquierdo, derecho], nodo_izquierdo.verificador and derecho.verificador)
                self.nodos += [nodo_izquierdo, fuente]
                return fuente


    def kleene_directo(self, nodo_hijo):
        if (type(nodo_hijo) == Central):
            fuente_interrogacion = Central("*", None, True, [nodo_hijo], True)
            self.nodos += [fuente_interrogacion]
            return fuente_interrogacion
        else:
            identificador = self.arbol + 1 if nodo_hijo not in "Ɛ" else None
            self.arbol = self.arbol + 1
            var_nodo_hijo = Central(nodo_hijo, identificador, False, [], False)
            fuente_interrogacion = Central("*", None, True, [var_nodo_hijo], True)
            self.nodos += [var_nodo_hijo, fuente_interrogacion]
            return fuente_interrogacion

    def gettear_siguientes_posiciones(self):
        for x in self.nodos:
            if not x.operador and not x.verificador:
                self.posicion_siguiente2(x.arbol, [])
            if x.signo == "-":
                primer_hijo = x.posicion[0]
                segundo_hijo = x.posicion[1]
                for y in primer_hijo.ultimaposicion:
                    self.posicion_siguiente2(y, segundo_hijo.posicion0)
            if x.signo == "*":
                for y in x.ultimaposicion:
                    self.posicion_siguiente2(y, x.posicion0)


    def posicion_siguiente2(self, arbol, posicion_siguiente):
        if arbol not in self.posiciones.keys():
            self.posiciones[arbol] = []
        self.posiciones[arbol] += posicion_siguiente
        self.posiciones[arbol] = set_to_list(self.posiciones[arbol])

    def id_por_nodo(self, arbol):
        for x in self.nodos:
            if x.arbol == arbol:
                return x

    def repetir_directo(self):
        estado_inicial = self.epicentro.posicion0
        nodo_estado_inicial = afd(self.definicion_de_nombre(), estado_inicial, 2)
        self.estados.append(nodo_estado_inicial)
        self.estado0 = nodo_estado_inicial.signo
        if self.estadoF in [x for x in nodo_estado_inicial.nodos]:
            self.estdosAceptacion.append(nodo_estado_inicial.signo)
        estados_etiquetados = [estado.terminado for estado in self.estados]
        while False in estados_etiquetados:
            for estado in self.estados:
                if not estado.terminado:
                    estados_sin_etiqeutar = estado
                    break
            estados_sin_etiqeutar.terminado = True
            
            for s in self.alpha:
                if type(s) != Central:
                    siguiente_pos_entry = []
                    for x in estados_sin_etiqeutar.nodos:
                        if self.id_por_nodo(x).signo == s:
                            siguiente_pos_entry += self.posiciones [x]
                    siguiente_pos_entry = set_to_list(siguiente_pos_entry)
                    if siguiente_pos_entry is empty:
                        continue
                    nuevo = afd(self.definicion_de_nombre(), siguiente_pos_entry, 2)
                    if nuevo.estados not in [estado.estados for estado in self.estados] and nuevo.estados != "":
                        if self.estadoF in [nodo for nodo in nuevo.nodos]:
                            self.estdosAceptacion .append(nuevo.signo)
                        self.estados.append(nuevo)
                        self.transiciones.append([estados_sin_etiqeutar.signo, s, nuevo.signo])
                    else:
                        self.nombre -= 1
                        for estado in self.estados:
                            if nuevo.estados == estado.estados:
                                self.transiciones.append([estados_sin_etiqeutar.signo, s, estado.signo])
                            
            estados_etiquetados = [estado.terminado for estado in self.estados]

def add2(expresion):
    modified = ""
    operators = ["*","|","("]
    alphabeto = "abcdefghijklmnopqrstuvwxyz0123456789E"
    idx = 0
    while idx < len(expresion):
        if expresion[idx] == "*" and ((expresion[idx+1] in alphabeto) or expresion[idx+1] == "("):
            modified += expresion[idx]+"-"
        elif not (expresion[idx] in operators) and expresion[idx+1] == ")":
            modified += expresion[idx]
        elif (not (expresion[idx] in operators) and not (expresion[idx+1] in operators)) or (not (expresion[idx] in operators) and (expresion[idx+1] == "(")):
            modified += expresion[idx]+"-"
        else:
            modified += expresion[idx]
        idx += 1
        if idx+1 >= len(expresion):
            modified += expresion[-1]
            break
    return modified

def precedencia_op(oper):
    if oper == "|":
        return 1
    elif oper == "-":
        return 2
    elif oper == "*":
        return 3
    return 0

def cambio_expresion(regular_exp, op = 1):
    final_exp = []
    to_modify = []
    inside_par = 0
    i = 0
    if "+" in regular_exp:
        while "+" in regular_exp:
            idx = regular_exp.find("+")
            if regular_exp[idx - 1] == ")":
                while i < len(regular_exp):
                    if regular_exp[i] == "(":
                        to_modify.append(i)                        
                    if regular_exp[i] == ")" and i < len(regular_exp) - 1:
                        final_exp.append(regular_exp[i])
                        if regular_exp[i + 1] == "+":
                            inside_par = i + 1
                            final_exp.append("*")
                            final_exp.append(regular_exp[to_modify.pop() : inside_par])
                            i += 1
                        else:
                            to_modify.pop()
                    else:
                        final_exp.append(regular_exp[i])
                    i += 1
                regular_exp = "".join(final_exp)
            else:
                inside = regular_exp[idx - 1]
                regular_exp = regular_exp.replace(inside + "+", "(" + inside + "*" + inside + ")")
    final_exp = []
    to_modify = []
    inside_par = 0
    i = 0
    if "?" in regular_exp:
        while "?" in regular_exp:
            idx = regular_exp.find("?")
            if regular_exp[idx - 1] == ")":
                while i < len(regular_exp):
                    if regular_exp[i] == "(":
                        to_modify.append(i)                        

                    if regular_exp[i] == ")":
                        final_exp.append(regular_exp[i])
                        if regular_exp[i + 1] == "?":
                            final_exp.append("|")
                            final_exp.append("Ɛ")
                            final_exp.append(")")
                            final_exp.insert(to_modify[-1], "(")
                            i += 1
                        else:
                            to_modify.pop()

                    else:
                        final_exp.append(regular_exp[i])
                    i += 1

                regular_exp = "".join(final_exp)
            else:
                inside = regular_exp[idx - 1]
                regular_exp = regular_exp.replace(inside + "?", "(" + inside + "|E)")

    if op == 1:
        return regular_exp

    elif op == 2:
        return "(" + regular_exp + ")#"


def set_to_list(something):
    something = {a for a in something}
    return [a for a in something]


def trans_func_afd(transitions):
    trans_f = {}
    for transition in transitions:
        init_state, char, end_state = [*transition]
        if init_state not in trans_f.keys():
            trans_f[init_state] = {}
        trans_f[init_state][char] = end_state
    return trans_f



def next_state_afd(state, char, transitions):
    next_state = None
    for trans in transitions:
        if trans[0] == state and trans[1] == char:
            next_state = trans[2]
    return next_state


def simulacion_directo(cadena, init_state, accept_states, transitions):
    actual_state = init_state
    for char in cadena:
        actual_state = next_state_afd(actual_state, char, transitions)
        if actual_state == None:
            return False
    if actual_state in accept_states:
        return True
    else:
        return False

def graficador_directo(states, init_state, end_states, trans_f, title):
    graph = graphviz.Digraph()

    for state in states:
        if state in end_states and state in init_state:
            graph.attr('node', shape = 'doublecircle')
            graph.node(state)

        elif state in end_states:
            graph.attr('node', shape = 'doublecircle')
            graph.node(state)

        elif state in init_state:
            graph.attr('node', shape = 'ellipse')
            graph.node(state)

        else:
            graph.attr('node', shape = 'circle')
            graph.node(str(state))

    for trans in trans_f:
        for t in trans_f[trans]:
            graph.edge(trans, trans_f[trans][t], t)

    graph.render(title, view=True)