import sys
import pygame
from codigo.jogo import Jogo

# Inicializa os modulos do pygame
pygame.init()

# Instancia e executa o jogo principal
if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()