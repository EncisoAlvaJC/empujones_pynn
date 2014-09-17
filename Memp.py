###################################################################
## MENACE_empujones, por Julio Enciso septiembre 2014
##
## Version sin prueba de errores, con fines de prueba
###################################################################

T = [['_','_','_','_'],['_','_','_','_'],['_','_','_','_'],['_','_','_','_']]
ficha1 = 'x'
ficha2 = 'o'

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
                print "El jugador"
                if candidato == ficha1:
                    print "humano"
                    gano0 = True
                else:
                    print "computadora"
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
            G =[]
            for i in T:
                G.append(i)
            for i in G:
                for j in G:
                    if j == ficha1:
                        j = ficha2
                    elif j == ficha2:
                        j = ficha1
            if f_ant == ficha1:
                f_ant_p = ficha2
            elif f_ant == ficha2:
                f_ant_p = ficha1
            else:
                f_ant_p = '_'
            LIST0.write(repr([n_fichas,l_ant,s_ant,f_ant_p,G,temp[0],temp[1]]))
            LIST0.write('\n')
            #del G
            #del f_ant_p
        else:
            G =[]
            for i in T:
                G.append(i)
            LIST1.write(repr([n_fichas,l_ant,s_ant,f_ant,G,temp[0],temp[1]]))
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

    for i in T:
        for j in i:
            j = '_'

    print "hora de recordar"
    # hora de recordar
    #if w0 == True:
        #for i in LIST0:
            #print i
            #MEMORIA.write(repr(i))
            #MEMORIA.write("\n")
    #if w1 == True:
        #for i in LIST1:
            #print i
            #MEMORIA.write(repr(i))
            #MEMORIA.write("\n")
    #MEMORIA.close()
    LIST0.close()
    LIST1.close()

    print
    print "ESTADO : JUEGO FINALIZADO"

def distribuye(nombre):
    archivo = open(nombre,'r')
    for i in archivo:
        for j in i:
            print j
        print
