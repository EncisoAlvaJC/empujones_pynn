###################################################################
## MENACE_empujones, por Julio Enciso septiembre 2014
##
## Version sin prueba de errores, con fines de prueba
###################################################################

import json
import unicodedata

import pybrain

###################################################################
###################################################################

from pybrain.structure import FeedForwardNetwork, SigmoidLayer, FullConnection

CEREBRO = FeedForwardNetwork()

entrad = SigmoidLayer(21)
#entrad = SigmoidLayer(1)
oculto = SigmoidLayer(50)
salida = SigmoidLayer(1)

CEREBRO.addInputModule(entrad)
CEREBRO.addModule(oculto)
CEREBRO.addOutputModule(salida)

preproceso = FullConnection(entrad,oculto)
posproceso = FullConnection(oculto,salida)

CEREBRO.addConnection(preproceso)
CEREBRO.addConnection(posproceso)

CEREBRO.sortModules()

#CEREBRO.activate([0])

###################################################################
###################################################################

T = [['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']]
ficha1 = 'x'
ficha2 = 'o'

def vaciar_tablero():
    returner = []
    for i in T:
        for j in i:
            returner.append(ord(j))
    return returner

def preguntar(let1,sig1,fich,letr2,sig2):
    return CEREBRO.activate([ ord(let1) , ord(sig1) , ord(fich) ] + vaciar_tablero() + [ ord(letr2), ord(sig2) ])

def imprimir_tablero():
    print " -->"
    print "|"
    print "V"
    print "   a b c d"
    print
    cont = 1
    for i in T:
        print "",cont,
        for j in i:
            print j,
        print "\n"
        cont += 1
    print

def imprimir_mensaje(D):
    if D == 0:
        print "Su turno, jugador humano."
    else:
        print "Turno del jugador computadora.\nEl proceso puede tardar un poco"
    print

def han_ganado():
    victoria = False
    gano0 = False
    gano1 = False
    for i in range(4):
        candidato = T[i][0]
        if candidato <> '_':
            cuantos = 0
            for j in range(4):
                if T[i][j] == candidato:
                    cuantos += 1            
            if cuantos == 4:
                print
                victoria = True
                print "El jugador"
                if candidato == ficha1:
                    print "humano"
                    gano0 = True
                else:
                    print "computadora"
                    gano1 = True
                print "ha completado una columna, la",i+1
                imprimir_tablero()
    for i in range(4):
        candidato = T[0][i]
        if candidato <> '_':
            cuantos = 0
            for j in range(4):
                if T[j][i] == candidato:
                    cuantos += 1            
            if cuantos == 4:
                print
                victoria = True
                print "El jugador",
                if candidato == ficha1:
                    print "humano",
                    gano0 = True
                else:
                    print "computadora",
                    gano1 = True
                print "ha completado una fila, la",chr(i+ord('a'))
                imprimir_tablero()
    print
    return victoria , gano0 , gano1

def meter_ficha(signo,letra,D):
    #letra = letr[0]
    #signo = sign[0]
    if D == 0:
        traeger1 = ficha1
    else:
        traeger1 = ficha2
    if ord('1') <= ord (letra) <= ord('4'):
        donde = ord(letra) - ord('1')
        if signo == '+':
            for i in range(4):
                if traeger1 <> '_':
                    traeger2 = T[donde][i]
                    T[donde][i] = traeger1
                    traeger1 = traeger2
                else:
                    break
        elif signo == '-':
            for i in range(4):
                if traeger1 <> '_':
                    traeger2 = T[donde][3-i]
                    T[donde][3-i] = traeger1
                    traeger1 = traeger2
                else:
                    break
    elif ord('a') <= ord (letra) <= ord('d'):
        donde = ord(letra) - ord('a')
        if signo == '+':
            for i in range(4):
                if traeger1 <> '_':
                    traeger2 = T[i][donde]
                    T[i][donde] = traeger1
                    traeger1 = traeger2
                else:
                    break
        elif signo == '-':
            for i in range(4):
                if traeger1 <> '_':
                    traeger2 = T[3-i][donde]
                    T[3-i][donde] = traeger1
                    traeger1 = traeger2
                else:
                    break
    else:
        print "Jugada invalida"
    return traeger1



def JUEGA():
    print
    print "ESTADO : JUGANDO"
    print

    LIST0 = open('recuerdos0.txt','w')
    LIST1 = open('recuerdos1.txt','w')

    # vision del MENACE
    #LIST0 =[]
    #LIST1 =[]

    dran = 0
    l_ant = '_'
    s_ant = '_'
    f_ant = '_'

    ya_ganaron = False
    w0 = False
    w1 = False

    n_fichas = 0

    while ya_ganaron == False:
        imprimir_tablero()
        imprimir_mensaje(dran)

        if dran == 1:
            for i in [ 'a','b','c','d','1','2','3','4' ]:
                for j in [ '+' , '-' ]:
                    print i , j ,
                    print preguntar( l_ant, s_ant, f_ant, i , j )

        validez_jugada = False
        
        while validez_jugada == False:
            temp = raw_input("Introduzca su jugada: ")
            if temp == "" or len(temp) < 2:
	        for i in T:
   		    for j in i:
		        j = '_'
                return
            if dran == 0:
                if temp[0] <> l_ant or f_ant <> ficha1 or temp[1] == s_ant:
                    validez_jugada = True
                else:
                    print "Esa jugada es ilegal, intente nuevamente"
            else:
                if temp[0] <> l_ant or f_ant <> ficha2 or temp[1] == s_ant:
                    validez_jugada = True
                else:
                    print "Esa jugada es ilegal, intente nuevamente"

        # aqui se registran las jugadas
        if dran == 1:
            G = [['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']]
            for i in range(4):
                for j in range(4):
                    if T[i][j] == ficha1:
                        G[i][j] = ficha2
                    elif T[i][j] == ficha2:
                        G[i][j] = ficha1
            if f_ant == ficha1:
                f_ant_p = ficha2
            elif f_ant == ficha2:
                f_ant_p = ficha1
            else:
                f_ant_p = '_'
            LIST0.write(json.dumps([n_fichas,l_ant,s_ant,f_ant_p,G,temp[0],temp[1]]))
            LIST0.write('\n')
            #del G
            #del f_ant_p
        else:
            G =[]
            for i in T:
                G.append(i)
            LIST1.write(json.dumps([n_fichas,l_ant,s_ant,f_ant,G,temp[0],temp[1]]))
            LIST1.write('\n')
            #del G

        l_ant = temp[0]
        s_ant = temp[1]
        f_ant = meter_ficha(temp[1],temp[0],dran)

        n_fichas += 1

        ya_ganaron,w1,w2 = han_ganado()

        if dran == 0:
            dran = 1
        else:
            dran = 0

    for i in range(4):
        for j in range(4):
            T[i][j] = '_'

    print
    print "ESTADO : JUEGO FINALIZADO"
    print

    print 
    print "ESTADO : CODIFICANDO PARTIDA"
    print

    LIST0.close()
    LIST1.close()

    cortoplazo = open('cortoplazo.txt','w')
    # hora de recordar
    if w0 == True:
        N = recupera('recuerdos0.txt')
        #print N
        for i in N:
            cortoplazo.write(json.dumps(i))
            cortoplazo.write('\n')
        #del N
    if w1 == True:
        N = recupera('recuerdos1.txt')
        #print N
        for i in N:
            cortoplazo.write(json.dumps(i))
            cortoplazo.write('\n')
        #del N
    cortoplazo.close()

    estudia()


def normaliza(unic):
    return unicodedata.normalize('NFKD',unic).encode('ascii','ignore')

def normaliza2(data):
    res = []
    for i in data:
        res = res + [ normaliza(i) ]
    return res

def recupera(nombre):
    returner = []
    archivo = open(nombre,'r')
    for y in archivo:        
        temp = json.loads(y)
        recuperador = [ temp[0] ] + normaliza2([ temp[1] , temp[2] , temp[3] ])
        tab = temp[4]
        trab = []
        for m in tab:
            Q = []
            for n in m:
                Q.append(normaliza(n))
            trab.append(Q)
        recuperador.append(trab)
        recuperador = recuperador + normaliza2([ temp[-2] , temp[-1] ]) 
        #print recuperador
        returner = returner + [ recuperador ]
    archivo.close()
    #print returner
    return returner

def estandariza(lista):
    returner = []
    returner = returner + [ lista[0] , lista[1] , lista[2] , lista [3] , lista[4] ]
    if ord('1') <= ord(lista[5]) <= ord('4'):
        A = ord(lista[5]) - ord('1')
    elif ord('a') <= ord(lista[5]) <= ord('d'):
        A = ord(lista[5]) - ord('a') + 4
    else:
        print 'ERROR1'
        return
    if lista[6] == '+':
        B = 0
    elif lista[6] == '-':
        B = 8
    else:
        print 'ERROR2'
        return
    returner = returner + [ A+B]
    #.append(add)
    #print returner
    return returner

def registro():
    returner = []
    archivo = open('largoplazo.txt','r')
    for y in archivo:        
        temp = json.loads(y)
        recuperador = [ temp[0] ] + normaliza2([ temp[1] , temp[2] , temp[3] ])
        tab = temp[4]
        trab = []
        for m in tab:
            Q = []
            for n in m:
                Q.append(normaliza(n))
            trab.append(Q)
        recuperador.append(trab)
        recuperador = recuperador + [ temp[5] ]
        #print recuperador
        returner = returner + [ recuperador ]
    archivo.close()
    #print returner
    return returner

def t_hor(memoria):
    returner = [ memoria[0] ]
    ch = memoria[1]
    sg = memoria[2]
    if ord('1') <= ord( memoria[1] ) <= ord('4'):
        ch = ord('4') - ord(memoria[1]) + ord('1')
    elif ord('a') <= ord( memoria[1] ) <= ord('d'):
        if memoria[2] == '+':
            s = '-'
        elif memoria[2] == '-':
            s = '+'
    returner = returner + [ chr(ch), sg , memoria[3] ]
    G = [['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']]
    for i in range(4):
        G[0][i] = memoria[4][3][i]
        G[1][i] = memoria[4][2][i]
        G[2][i] = memoria[4][1][i]
        G[3][i] = memoria[4][0][i]
    returner = returner + [ G ]
    let = memoria[5] % 8
    if memoria[5] <= 8:
        sig = 1
    else:
        sig = 0
    if 0 <= let <= 3: # si es una letra
        if sig == 1:
            sig = 0
        else:
            sig = 1
    else: # si es un numero
        let = 7 - let + 4
    returner = returner + [ 8*sig + let ]
    return returner
def t_ver(memoria):
    returner = [ memoria[0] ]
    ch = memoria[1]
    sg = memoria[2]
    if ord('a') <= ord( memoria[1] ) <= ord('d'):
        ch = ord('d') - ord(memoria[1]) + ord('a')
    elif ord('1') <= ord( memoria[1] ) <= ord('4'):
        if memoria[2] == '+':
            s = '-'
        elif memoria[2] == '-':
            s = '+'
    returner = returner + [ chr(ch), sg , memoria[3] ]
    G = [['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']]
    for i in range(4):
        G[0][i] = memoria[4][3][i]
        G[1][i] = memoria[4][2][i]
        G[2][i] = memoria[4][1][i]
        G[3][i] = memoria[4][0][i]
    returner = returner + [ G ]
    let = memoria[5] % 8
    if memoria[5] <= 8:
        sig = 1
    else:
        sig = 0
    if 4 <= let <= 7: # si es una letra
        if sig == 1:
            sig = 0
        else:
            sig = 1
    else: # si es un numero
        let = 4 - let + 0
    returner = returner + [ 8*sig + let ]
    return returner
def t_tr1(memoria):
    returner = [ memoria[0] ]
    ch = memoria[1]
    sg = memoria[2]
    if ord('a') <= ord( memoria[1] ) <= ord('d'):
        ch = ord(ch) - ord('a') + ord('1')
    elif ord('1') <= ord( memoria[1] ) <= ord('4'):
        ch = ord(ch) -ord('1') + ord('a')
    returner = returner + [ chr(ch), sg , memoria[3] ]
    G = [['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']]
    for i in range(4):
        for j in range(4):
            G[i][j] = memoria[4][j][i]
    returner = returner + [ G ]
    if 0 <= memoria[5] % 8 <= 3:
        let = memoria[5] + 4
    else:
        let = memoria[5] - 4
        returner = returner + [ let ]
    return returner
def t_tr2(memoria):
    return t_ver(t_hor(t_tr1(memoria)))

def estudia():
    experiencia = recupera('cortoplazo.txt')
    sabiduria = registro()
    recordando = []
    cinta = [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 16]
    #print experiencia
    for i in experiencia:
        recordando = recordando + [ estandariza(i) ]
    #print recordando
    for i in recordando:
        #print i[-1]
        visto = False
        for j in sabiduria:
            #print j[-1]
            if i[:-1] == j[:-1]:                
                j[-1][i[-1]] += 1
                j[-1][-1] += 1
                visto = True
                break
        if visto == False:
            #print "nuevo movimiento : "
            sabiduria = sabiduria + [ i[0:-1] + [cinta] ]
            sabiduria[-1][-1][i[-1]] = 2
            sabiduria[-1][-1][-1] = 16
    with open('largoplazo.txt','w') as f:
        for i in sabiduria:
            f.write( json.dumps( i ) )
            f.write( '\n' )
            #pass
