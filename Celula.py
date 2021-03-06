from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
import time

class Celula:
    
    def __init__(self, tamanho, tam_max):

        self.ListaDeInteiros = []
        self.tamanho = tamanho
        self.tam_max = tam_max
        for x in range (0,tamanho):
            self.ListaDeInteiros.append([])
            for y in range (0,tamanho):
                self.ListaDeInteiros[x].append([])

    def cadastraLinha(self,linha):

        indice = 0
        tamanho_celula_x = self.tam_max/self.tamanho

        for x in linha:
            minx = x.minx
            miny = x.miny
            maxx = x.maxx
            maxy = x.maxy

            if maxx > self.tam_max:
                maxx = self.tam_max
            if maxy > self.tam_max:
                maxy = self.tam_max
            if miny < 0:
                miny=0
            if minx < 0:
                minx = 0

            minx = minx//tamanho_celula_x
            maxx = maxx//tamanho_celula_x
            miny = miny//tamanho_celula_x
            maxy = maxy//tamanho_celula_x

            z = int(minx)
            while z <= int(maxx):
                y = int(miny)
                while y <= int(maxy):
                    if y == self.tamanho and z == self.tamanho:
                        self.ListaDeInteiros[z-1][y-1].append(indice)
                    elif y == self.tamanho:
                        self.ListaDeInteiros[z][y-1].append(indice)
                    elif z == self.tamanho:
                        self.ListaDeInteiros[z-1][y].append(indice)
                    else:
                        self.ListaDeInteiros[z][y].append(indice)
                    y = y+1
                z = z + 1
            indice+=1


    def candidatos(self,linha,i, N_LINHAS):
        candidatos = []
        for x in range (0,N_LINHAS):
            candidatos.append(False)
        indice = 0
        tamanho_celula_x = self.tam_max/self.tamanho

        minx = linha.minx
        miny = linha.miny
        maxx = linha.maxx
        maxy = linha.maxy

        if maxx > self.tam_max:
            maxx = self.tam_max
        if maxy > self.tam_max:
            maxy = self.tam_max
        if miny < 0:
            miny=0
        if minx < 0:
            minx = 0

        minx = minx//tamanho_celula_x
        maxx = maxx//tamanho_celula_x
        miny = miny//tamanho_celula_x
        maxy = maxy//tamanho_celula_x

        z = int(minx)
        while z <= int(maxx):
            y = int(miny)
            while y <= int(maxy):
                if y == self.tamanho and z == self.tamanho:
                    for j in range (0,N_LINHAS):
                        if j in self.ListaDeInteiros[z-1][y-1]:
                            candidatos[j] = True
                elif y == self.tamanho:
                    for j in range (0,N_LINHAS):
                        if j in self.ListaDeInteiros[z][y-1]:
                            candidatos[j] = True
                elif z == self.tamanho:
                    for j in range (0,N_LINHAS):
                        if j in self.ListaDeInteiros[z-1][y]:
                            candidatos[j] = True
                else:
                    for j in range (0,N_LINHAS):
                        if j in self.ListaDeInteiros[z][y]:
                            candidatos[j] = True
                y = y+1
            z = z+1
        return candidatos

    def getLinhas(self):

        return self.ListaDeInteiros        