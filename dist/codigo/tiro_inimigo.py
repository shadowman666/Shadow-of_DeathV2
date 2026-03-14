import math
import pygame
from codigo.entidade import Entidade


class TiroInimigo(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)

        # Atributos exclusivos do Tiro do Chefao (Gosma)
        self.velocidade_tiro = 7  # Pode aumentar se quiser a gosma mais rapida
        self.dano = 10  # Garante que a gosma arranca a sua vida!

        self.direcao_x = 0
        self.direcao_y = 1

        self.imagem_original = self.superficie

    def mover(self):
        self.retangulo.centerx += int(self.direcao_x * self.velocidade_tiro)
        self.retangulo.centery += int(self.direcao_y * self.velocidade_tiro)

        # Rotaciona a gosma para a direcao em que ela esta voando
        magnitude = math.hypot(self.direcao_x, self.direcao_y)
        if magnitude != 0:
            angulo = math.degrees(math.atan2(-self.direcao_y, self.direcao_x))
            self.superficie = pygame.transform.rotate(self.imagem_original, angulo)
            centro_atual = self.retangulo.center
            self.retangulo = self.superficie.get_rect(center=centro_atual)