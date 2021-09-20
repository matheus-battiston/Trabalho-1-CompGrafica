# ************************************************
#   Linha.py
#   Define a classe Linha
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto

from random import randint as rand

""" Classe Linha """
class Linha:
    def __init__(self, centrox: float = 0, centroy: float = 0, meia_largx: float = 0, meia_largy: float = 0, minx: float = 0, miny: float = 0, maxx: float = 0, maxy: float = 0, x1: float = 0, y1: float = 0, x2: float = 0, y2: float = 0):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.centrox = centrox
        self.centroy = centroy
        self.meia_largx = meia_largx
        self.meia_largy = meia_largy

    """ Gera uma linha com tamanho 'tamMax' dentro de um limite 'limite'. Armazena os valores nas variaveis x1,x2,y1,y2."""
    def geraLinha(self, limite: int, tamMax: int):
        self.x1 = (rand(0, limite)*10) / 10.0
        self.y1 = (rand(0, limite)*10) / 10.0
        

        deltaX = rand(0, limite) / limite
        deltaY = rand(0, limite) / limite

        if (rand(0, 1) % 2):
            self.x2 = self.x1 + deltaX * tamMax
        else:
            self.x2 = self.x1 - deltaX * tamMax

        if (rand(0, 2) % 2):
            self.y2 = self.y1 + deltaY * tamMax
        else:
            self.y2 = self.y1 - deltaY * tamMax
            
        self.maxx = max(self.x1, self.x2)
        self.minx = min (self.x1, self.x2)
        self.maxy = max (self.y1, self.y2)
        self.miny = min(self.y1,self.y2)
        self.centrox = (self.maxx + self.minx)/2
        self.centroy = (self.maxy + self.miny)/2
        self.meia_largx = (self.maxx - self.minx)/2
        self.meia_largy = (self.maxy - self.miny)/2

    """ Desenha a linha na tela atual """
    def desenhaLinha(self):
        glBegin(GL_LINES)
        
        glVertex2f(self.x1, self.y1)
        glVertex2f(self.x2, self.y2)
    
        glEnd()