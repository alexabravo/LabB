from regex import *
from afn import *
import copy
from operator import attrgetter
import graphviz 

class Thompson:
    def __init__(self, expresion_regular):
        self.a = Regex(expresion_regular)
        self.maquinas = []
        self.expresion_regular = self.a.regex_to_postfix()

    def parsing(self):
        alpha = self.a.alfabeto(self.expresion_regular)
        for i in self.expresion_regular:
            if i == "*":
                self.kleene(self.maquinas.pop())
            if i in alpha:
                self.repetir(i)
            if i == "+":
                self.mas(self.maquinas.pop())
            if i == "|":
                self.OR(self.maquinas.pop(),self.maquinas.pop())
            if i == "?":
                self.interrogacion(self.maquinas.pop())
            if i == "ß":
                self.concatenacion(self.maquinas.pop(),self.maquinas.pop())

        return self.maquinas[0]
        

    def compilar(self):
        return self.parsing()
        

        

    def concatenacion(self, maquina1, maquina2):
        estados = []
        estados = maquina2.estados[:-1]
        punto_referencia = len(maquina2.estados) -1

        for estado in maquina1.estados:
            if estado.tipo == 1:
                estado.etiqueta = "s" + str(punto_referencia)
                estado.tipo = 2
            else:
                estado.etiqueta = "s" + str((int(estado.etiqueta[1:]) + punto_referencia))

            
            for transicion in estado.transiciones:
                transicion.destino = "s" + str((int(transicion.destino[1:]) + punto_referencia))

            estados.append(estado)
        
        self.maquinas.append(AFN(estados,[],[])) 



    def kleene(self, auotomata):
        estados = []
        estado_inicial = Estado("s0",[Transicion("s1","Ɛ"),Transicion("s"+str(len(auotomata.estados)+1),"Ɛ")],1)
        estado_final = Estado("s"+str((len(auotomata.estados)+1)),[],3)

        
        auotomata.estados[0].tipo = 2
        auotomata.estados[-1].tipo = 2

        estados.append(estado_inicial)

        for s in auotomata.estados:
            s.etiqueta = "s"+ str((int(s.etiqueta[1])+ 1))

            if len(s.transiciones) == 0:
                s.transiciones = [Transicion("s"+ str(len(auotomata.estados)+1),"Ɛ"), Transicion("s1", "Ɛ")]
            else: 
                for t in s.transiciones:
                    t.destino = "s" + str((int(t.destino[1])+ 1))
            estados.append(s)

        estados.append(estado_final)
        self.maquinas.append(AFN(estados,[],[]))

    
    def mas(self,automata):
        automata2 = copy.deepcopy(automata) 
        self.kleene(automata)
        self.concatenacion(self.maquinas.pop(),automata2)


    def OR(self,automata1,automata2):
        
        estados = []
        estado_inicial = Estado("s0",[Transicion("s1","Ɛ"),Transicion("s"+str(len(automata2.estados)+1),"Ɛ")],1)
        estado_final = Estado("s"+str(len(automata1.estados)+len(automata2.estados)+1),[],3)

        automata1.estados[0].tipo = 2 
        automata1.estados[-1].tipo = 2 

        automata2.estados[0].tipo = 2
        automata2.estados[-1].tipo = 2

        estados.append(estado_inicial)
        
        
        for s in automata2.estados:
            s.etiqueta = "s"+ str((int(s.etiqueta[1])+ 1)) 
            for t in s.transiciones:
                t.destino =  "s" + str((int(t.destino[1])+ 1))
            estados.append(s)
        

        estados[-1].transiciones =[Transicion("s"+str(len(automata1.estados)+len(automata2.estados)+1),"Ɛ")]

        for i in automata1.estados:
            i.etiqueta = "s"+ str((int(i.etiqueta[1])+len(automata2.estados)+ 1)) 
            for j in i.transiciones:
                j.destino = "s"+ str((int(j.destino[1])+len(automata2.estados)+ 1)) 
            estados.append(i)

        estados[-1].transiciones =[Transicion("s"+str(len(automata1.estados)+len(automata2.estados)+1),"Ɛ")]
        estados.append(estado_final)

        self.maquinas.append(AFN(estados,[],[]))

    def interrogacion(self,automata):
        self.repetir("Ɛ")
        self.OR(self.maquinas.pop(),automata)


    def repetir(self, caracter):
        trans = Transicion("s1", caracter)
        estado1 = Estado("s0", [trans],1)
        estadof = Estado("s1", [], 3)
        self.maquinas.append(AFN([estado1,estadof],[],trans))


    def graficar_afn(self):
        maquina = self.maquinas[0]
        afn = graphviz.Digraph('finite_state_machine', filename='AFN.gv')
        afn.attr(rankdir='LR', size='8,5')
        afn.attr('node', shape='ellipse')
        afn.node('s0')
        afn.attr('node', shape='doublecircle')
        afn.node(maquina.estados[-1].etiqueta)
        for estado in maquina.estados:
            if estado.tipo == 3:
                continue
            for transi in estado.transiciones:
                afn.attr('node', shape='circle')
                afn.edge(estado.etiqueta, transi.destino, label=transi.caracter)
        alfabeto = self.a.alfabeto(self.expresion_regular)
        print('---', '---'.join(alfabeto))
        name_dict = {}
        for estado in maquina.estados:
            for i in alfabeto:
                name_dict[i] = "X"
            row = f"{estado.etiqueta}"
            for transicion in estado.transiciones:
                name_dict[transicion.caracter] = transicion.destino
            print(row, '---'.join(list(name_dict.values())))
        print("Maquina", self.a.alfabeto(self.expresion_regular))
        afn.view()
    

    def move_afn(self,states,chr):
        response = []
        for s in states:
            for i in s.transiciones:
                if i.caracter == chr:
                    estado = None
                    for st in self.maquinas[0].estados:
                        if st.etiqueta == i.destino:
                            estado = st
                    if estado is not None and estado not in response:
                        response.append(estado)
                    elif s not in response:
                        response.append(s)

        return response

    
    def eClosure(self,states):
        next2 = []
        while True:
            siguiente =[]    
            for s in states:
                    if s.tipo == 3 and s not in siguiente:
                        siguiente.append(s)
                    for i in s.transiciones:
                        #Caracter abajo
                        if i.caracter == "Ɛ":
                            estado = None
                            for st in self.maquinas[0].estados:
                                if st.etiqueta == i.destino:
                                    estado = st
                                    break
                            if estado is not None: 
                                if estado not in siguiente:
                                    if s not in siguiente:
                                        siguiente.append(s)
                                    siguiente.append(estado)
                            elif s not in siguiente:
                                siguiente.append(s)                    
                        elif s not in siguiente:
                            siguiente.append(s)
            siguiente.sort(key =attrgetter("etiqueta"),reverse=False)
            if states == siguiente:
                for x in siguiente:
                    if x not in next2:
                        next2.append(x)
                return next2  
            states = siguiente

            for x in siguiente:
                if x not in next2:
                    next2.append(x)
        return siguiente

    def simulacion_afn(self,afn,cadena):
        estados = [afn.estados[0]]
        estados = self.eClosure(estados)
        for i in cadena:
            estados = self.eClosure(self.move_afn(estados,i))
        return  afn.estados[-1] in estados
    
    
    def graficar_afd(self,afd1):
        sf =  []
        afd = graphviz.Digraph('finite_state_machine', filename='FDA.gv')
        afd.attr(rankdir='LR', size='8,5')
        
        for s in afd1.estados:
            if s.tipo == 1:
                afd.attr('node', shape='ellipse')
                afd.node('s0')
            if (s.tipo ==3):
                for t in s.transiciones:
                    print(s.etiqueta)
                    afd.attr('node', shape='doublecircle')
                    afd.edge(s.etiqueta, t.destino, label=t.caracter)
                    sf.append(s.etiqueta)
                
                if len(s.transiciones) == 0:
                    afd.attr('node', shape='doublecircle')
                    afd.node(s.etiqueta)
        for st in afd1.estados:
            for t in st.transiciones:
                if st.tipo !=3 and st.etiqueta not in sf:
                    afd.attr('node', shape='circle')
                    afd.edge(st.etiqueta, t.destino, label=t.caracter)
        afd.view()

    def subset(self,afn):
        alpha = self.a.alfabeto(self.expresion_regular)
        print(alpha)
        alpha.sort()
        if "Ɛ" in alpha:
            alpha = list(filter(lambda x:x!="Ɛ", alpha))
        afd = []
        destados = [self.eClosure([afn.estados[0]])]
        cont, indicador = 0,0
        while indicador < len(destados):
            transi = []
            cont = indicador + 1
            for c in alpha:
                aaa = self.move_afn(destados[indicador], c)
                temp = self.eClosure(self.move_afn(destados[indicador],c))
                if temp in destados:
                    arr = list(filter(lambda x: x == temp,destados)) 
                    pos = destados.index(arr[0])
                    transi.append(Transicion("s"+str(pos),c)) 
                else:
                    if len(temp)== 0:
                        cont =cont -1 
                        continue
                    if indicador > 0:
                        transi.append(Transicion("s"+str(len(destados)),c))
                    else:
                        transi.append(Transicion("s"+str(cont),c))
                    destados.append(temp)
                    cont =cont + 1

            tipo3 = False
            sf = afn.estados[-1].etiqueta 

            for j in destados[indicador]:
                if j.etiqueta == sf:
                    tipo3 = True
                    break
            if indicador == 0:
                afd.append(Estado("s"+str(indicador),transi,3 if tipo3 else 1))
            else:
                afd.append(Estado("s"+str(indicador),transi,3 if tipo3 else 2))
            indicador =indicador +1
        
        return AFN(afd,[],alpha)


    def simulacion_afd(self,cadena,afd):
        estados = []
        estados.append(afd.estados[0])
        cont = 1
        for c in cadena:
            estados = self.move_afd(estados,c,afd)
            cont +=1
        return len(estados) > 0 and estados[0].tipo == 3

    def move_afd(self,states,chr,maquina): 
        response = []
        for s in states:
            for i in s.transiciones:
                if i.caracter == chr:
                    estado = None
                    for st in maquina.estados:
                        if st.etiqueta == i.destino:
                            estado = st    
                    if estado is not None:
                        if estado not in response:
                            response.append(estado)
                    elif s not in response:
                        response.append(s)
        return response