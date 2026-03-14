import math
import pygame
from codigo.constantes import VELOCIDADE
from codigo.entidade import Entidade


class TiroJogador(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)
        self.direcao_x = 1
        self.direcao_y = 0

        self.imagem_original = self.superficie

    def mover(self):
        magnitude = math.hypot(self.direcao_x, self.direcao_y)

        if magnitude != 0:
            self.retangulo.centerx += int((self.direcao_x / magnitude) * VELOCIDADE[self.nome])
            self.retangulo.centery += int((self.direcao_y / magnitude) * VELOCIDADE[self.nome])

            angulo = math.degrees(math.atan2(-self.direcao_y, self.direcao_x))

            self.superficie = pygame.transform.rotate(self.imagem_original, angulo)

            centro_atual = self.retangulo.center
            self.retangulo = self.superficie.get_rect(center=centro_atual)