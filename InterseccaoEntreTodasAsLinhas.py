
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
from Celula import Celula
import time

N_LINHAS = 100
MAX_X = 100

ContadorInt = 0
ContChamadas = 0
Subdivisoes = 20

linhas = []
Lista_Faixas_X = []
Lista_Faixas_Y = []
ListaFinal = []
Cel = Celula(Subdivisoes,MAX_X)

def init():
    global linhas
    global Lista_Faixas_X
    global Subdivisoes
    global Cel
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    linhas = [Linha() for i in range(N_LINHAS)]

    for linha in linhas:
        linha.geraLinha(MAX_X, 10)
    
    Cel.cadastraLinha(linhas)
    cria_subdivisão(Subdivisoes)
    
# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    # Reseta coordenadas do sistema antes the modificala
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define os limites lógicos da área OpenGL dentro da Janela
    glOrtho(0, 100, 0, 100, 0, 1)

    # Define a área a ser ocupada pela área OpenGL dentro da Janela
    glViewport(0, 0, w, h)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ********************************************************************** */
#                                                                        */
#  Calcula a interseccao entre 2 retas (no plano "XY" Z = 0)             */
#                                                                        */
# k : ponto inicial da reta 1                                            */
# l : ponto final da reta 1                                              */
# m : ponto inicial da reta 2                                            */
# n : ponto final da reta 2                                              */
# 
# Retorna:
# 0, se não houver interseccao ou 1, caso haja                                                                       */
# int, valor do parâmetro no ponto de interseção (sobre a reta KL)       */
# int, valor do parâmetro no ponto de interseção (sobre a reta MN)       */
#                                                                        */
# ********************************************************************** */
def intersec2d(k: Ponto, l: Ponto, m: Ponto, n: Ponto):
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None # não há intersecção

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

# **********************************************************************
# HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto)
# Detecta interseccao entre os pontos
#
# **********************************************************************
def HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0


# **********************************************************************
# DesenhaLinhas()
# Desenha as linha na tela
#
# **********************************************************************
def DesenhaLinhas():
    global linhas

    glColor3f(0,1,0)

    for linha in linhas:
        linha.desenhaLinha()

# **********************************************************************
# DesenhaCenario()
# Desenha o cenario
#
# **********************************************************************
def colisao_envelope(linha1,linha2):
    if (abs(linha1.centrox - linha2.centrox) > linha1.meia_largx + linha2.meia_largx):
        return False
    elif abs(linha1.centroy - linha2.centroy) > linha1.meia_largy + linha2.meia_largy:
        return False

    return True 

def cria_subdivisão(nro_divisoes):

    global Lista_Faixas_X
    global Lista_Faixas_Y
    tamanho_faixas = MAX_X/nro_divisoes
    Lista_Faixas_X = []
    Lista_Faixas_Y = []
    global ListaFinal
    ListaFinal=[]


    for x in range (0,nro_divisoes):
        ListaFinal.append([])
        for y in range (0,nro_divisoes):
            ListaFinal[x].append([])
            
    for x in range (0,nro_divisoes):
        Lista_Faixas_X.append([])
    for x in range (0,nro_divisoes):
        Lista_Faixas_Y.append([])
#Faixa Vertical
    
    for x in range(0,len(linhas)):
        minimo = linhas[x].miny
        maximo = linhas[x].maxy

        #Programa está gerando linhas fora do plano, isso garante que a estrutura ignore partes de fora
        if linhas[x].miny < 0:
            minimo = 0
        if linhas[x].maxy > MAX_X:
            maximo = MAX_X


        faixa = int(minimo // tamanho_faixas)
        #Garante que uma linha que va até o limite do plano nao seja colocada na faixa "de fora"
        if faixa == nro_divisoes:
            Lista_Faixas_Y[faixa-1].append(x)
        else:
            Lista_Faixas_Y[faixa].append(x)

        faixa2 = int(maximo // tamanho_faixas)

        if faixa2 != faixa and faixa2 == nro_divisoes:
            Lista_Faixas_Y[faixa2-1].append(x)
        elif faixa2 != faixa:
            Lista_Faixas_Y[faixa2].append(x)

        #Cobrir faixas intermediarias
        if faixa2 - faixa > 1:
            for z in range(faixa+1,faixa2):
                Lista_Faixas_Y[z].append(x)
    
#Faixa Horizontal

    for x in range(0,len(linhas)):
        minimo = linhas[x].minx
        maximo = linhas[x].maxx

        #Programa está gerando linhas fora do plano, isso garante que a estrutura ignore partes de fora
        if linhas[x].minx < 0:
            minimo = 0
        if linhas[x].maxx > MAX_X:
            maximo = MAX_X


        faixa = int(minimo // tamanho_faixas)
        #Garante que uma linha que va até o limite do plano nao seja colocada na faixa "de fora"
        if faixa == nro_divisoes:
            Lista_Faixas_X[faixa-1].append(x)
        else:
            Lista_Faixas_X[faixa].append(x)

        faixa2 = int(maximo // tamanho_faixas)

        if faixa2 != faixa and faixa2 == nro_divisoes:
            Lista_Faixas_X[faixa2-1].append(x)
        elif faixa2 != faixa:
            Lista_Faixas_X[faixa2].append(x)

        #Cobrir faixas intermediarias
        if faixa2 - faixa > 1:
            for z in range(faixa+1,faixa2):
                Lista_Faixas_X[z].append(x)

    #Junta as duas faixas (horizontal e vertical), formando a final.
    for x in range (0,nro_divisoes):
        for y in range (0,nro_divisoes):
            ListaFinal[x][y] = list(set(Lista_Faixas_X[x]) & set(Lista_Faixas_Y[y]))
        


def DesenhaCenario():
    global ContChamadas, ContadorInt

    PA, PB, PC, PD = Ponto(), Ponto(), Ponto(), Ponto()
    ContChamadas, ContadorInt = 0, 0
    
    # Desenha as linhas do cenário
    glLineWidth(1)
    glColor3f(1,0,0)

    #Celula com classe
    """for x in Cel.ListaDeInteiros:
        for z in x:
            for i in z:
                PA.set(linhas[i].x1, linhas[i].y1)
                PB.set(linhas[i].x2, linhas[i].y2)
                for a in z:
                    PC.set(linhas[a].x1, linhas[a].y1)
                    PD.set(linhas[a].x2, linhas[a].y2)
                    ContChamadas += 1
                    if HaInterseccao(PA, PB, PC, PD):
                        ContadorInt += 1
                        linhas[i].desenhaLinha()
                        linhas[a].desenhaLinha()"""
    
    #Versão sem classe que fiz antes
    """for x in ListaFinal:
        for y in x:
            for z in y:
                PA.set(linhas[z].x1, linhas[z].y1)
                PB.set(linhas[z].x2, linhas[z].y2)
                for a in y:
                    PC.set(linhas[a].x1, linhas[a].y1)
                    PD.set(linhas[a].x2, linhas[a].y2)
                    ContChamadas += 1
                    if HaInterseccao(PA, PB, PC, PD):
                        ContadorInt += 1
                        linhas[z].desenhaLinha()
                        linhas[a].desenhaLinha()
                        """

        #Colisão com envelope
    """
    for i in range(N_LINHAS):
        PA.set(linhas[i].x1, linhas[i].y1)
        PB.set(linhas[i].x2, linhas[i].y2)
        for j in range(N_LINHAS):
            PC.set(linhas[j].x1, linhas[j].y1)
            PD.set(linhas[j].x2, linhas[j].y2)

            if colisao_envelope(linhas[i],linhas[j]):
                ContChamadas += 1
                if HaInterseccao(PA, PB, PC, PD):
                    ContadorInt += 1
                    linhas[i].desenhaLinha()
                    linhas[j].desenhaLinha()
        """
# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    DesenhaLinhas()
    DesenhaCenario()
    
    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualização da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()

    if TempoTotal > 5.0:
        print(f'Tempo Acumulado: {TempoTotal} segundos.')
        print(f'Nros de Frames sem desenho: {int(nFrames)}')
        print(f'FPS(sem desenho): {int(nFrames/TempoTotal)}')
        
        TempoTotal = 0
        nFrames = 0
        
        print(f'Contador de Intersecoes Existentes: {ContadorInt/2.0}')
        print(f'Contador de Chamadas: {ContChamadas}')
        print( f'Subdivisões', Subdivisoes)

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        init()

    # Força o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
#
#
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global Subdivisoes
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        if Subdivisoes < 50:
            Subdivisoes += 1
            cria_subdivisão(Subdivisoes)
        else:
            pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        if Subdivisoes > 2:
            Subdivisoes -= 1
            cria_subdivisão(Subdivisoes)
        else :
            pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        pass

    glutPostRedisplay()


def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de título da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Algorimos de Cálculo de Colisão")

# executa algumas inicializações
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# será chamada automaticamente quando
# for necessário redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# será chamada automaticamente quando
# o usuário alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# será chamada automaticamente sempre
# o usuário pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" será chamada
# automaticamente sempre o usuário
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass