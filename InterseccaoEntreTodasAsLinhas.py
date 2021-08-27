# **********************************************************************
# PUCRS/FACIN
# COMPUTAÇÃO GRÁFICA
#
# Teste de colisão em OpenGL
#       
# Marcio Sarroglia Pinho
# pinho@inf.pucrs.br
# **********************************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
import time

N_LINHAS = 300
MAX_X = 100

ContadorInt = 0
ContChamadas = 0

linhas = []

# **********************************************************************
#  init()
#  Inicializa os parâmetros globais de OpenGL
#/ **********************************************************************
def init():
    global linhas
    global Lista_Faixas
    Lista_Faixas = []
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    linhas = [Linha() for i in range(N_LINHAS)]

    for linha in linhas:
        linha.geraLinha(MAX_X, 10)

    cria_subdivisão(3)
    
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
    
    global Lista_Faixas
    tamanho_faixas = 100/nro_divisoes
    for x in range (0,nro_divisoes):
        Lista_Faixas.append([])
        

    for x in range(0,len(linhas)):
        minimo = linhas[x].minx
        maximo = linhas[x].maxx
        
        #Programa está gerando linhas fora do plano, isso garante que a estrutura ignore partes de fora
        if linhas[x].minx < 0:
            minimo = 0
        if linhas[x].maxx > 100:
            maximo = 100


        faixa = int(minimo // tamanho_faixas)
        #Garante que uma linha que va até o limite do plano nao seja colocada na faixa "de fora"
        if faixa == nro_divisoes:
            Lista_Faixas[faixa-1].append(x)
        else:
            Lista_Faixas[faixa].append(x)

        faixa2 = int(maximo // tamanho_faixas)
        
        if faixa2 != faixa and faixa2 == nro_divisoes:
            Lista_Faixas[faixa2-1].append(x)
        elif faixa2 != faixa:
            Lista_Faixas[faixa2].append(x)
        
        #Cobrir faixas intermediarias
        if faixa2 - faixa > 1:
            for z in range(faixa+1,faixa2):
                Lista_Faixas[z].append(x)

    
def DesenhaCenario():
    global ContChamadas, ContadorInt

    PA, PB, PC, PD = Ponto(), Ponto(), Ponto(), Ponto()
    ContChamadas, ContadorInt = 0, 0
    
    # Desenha as linhas do cenário
    glLineWidth(1)
    glColor3f(1,0,0)
    
    for x in Lista_Faixas:
        for y in x:
            PA.set(linhas[y].x1, linhas[y].y1)
            PB.set(linhas[y].x2, linhas[y].y2)
            for z in x:
                PC.set(linhas[z].x1, linhas[z].y1)
                PD.set(linhas[z].x2, linhas[z].y2)

                ContChamadas += 1
                if HaInterseccao(PA, PB, PC, PD):
                    ContadorInt += 1
                    linhas[y].desenhaLinha()
                    linhas[z].desenhaLinha()
                
   

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
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
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