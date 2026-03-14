import pygame
from codigo.constantes import LARGURA_TELA, TECLA_ESQUERDA, TECLA_DIREITA
from codigo.entidade import Entidade


class Fundo(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)

    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()

        # O fundo se move na direcao contraria ao jogador para criar a ilusao de deslocamento (camera)
        if teclas_pressionadas[TECLA_DIREITA]:
            self.retangulo.centerx -= 2
        if teclas_pressionadas[TECLA_ESQUERDA]:
            self.retangulo.centerx += 2

        # Verifica se a imagem do fundo saiu pela esquerda e a reposiciona no final da direita
        if self.retangulo.right <= 0:
            self.retangulo.left = LARGURA_TELA

        # Verifica se a imagem do fundo saiu pela direita e a reposiciona no final da esquerda
        elif self.retangulo.left >= LARGURA_TELA:
            self.retangulo.right = 0