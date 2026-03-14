import math
import pygame
from codigo.entidade import Entidade
from codigo.tiro_inimigo import TiroInimigo


class Chefao(Entidade):
    def __init__(self, nome: str, posicao: tuple, alvo: Entidade = None):
        super().__init__(nome, posicao)
        self.alvo = alvo

        # 120 frames = 2 segundos cravados (a 60 FPS)
        self.atraso_tiro = 120

        # Atributos exclusivos do corpo do Chefao
        self.velocidade_chefao = 2
        self.dano = 1  # Garante que encostar nele tira a sua vida!

        self.imagem_original = self.superficie

    def mover(self):
        if not self.alvo:
            return

        distancia_x = self.alvo.retangulo.centerx - self.retangulo.centerx
        distancia_y = self.alvo.retangulo.centery - self.retangulo.centery
        magnitude = math.hypot(distancia_x, distancia_y)

        if magnitude != 0:
            self.retangulo.centerx += int((distancia_x / magnitude) * self.velocidade_chefao)
            self.retangulo.centery += int((distancia_y / magnitude) * self.velocidade_chefao)

            angulo = math.degrees(math.atan2(-distancia_y, distancia_x))
            self.superficie = pygame.transform.rotate(self.imagem_original, angulo)

            centro_atual = self.retangulo.center
            self.retangulo = self.superficie.get_rect(center=centro_atual)

    def atirar(self):
        self.atraso_tiro -= 1

        # Quando zerar os 2 segundos, ele atira
        if self.atraso_tiro <= 0 and self.alvo:
            self.atraso_tiro = 120  # Reseta o cronometro para mais 2 segundos
            tiro = TiroInimigo(nome='TiroChefao', posicao=(self.retangulo.centerx, self.retangulo.centery))

            distancia_x = self.alvo.retangulo.centerx - self.retangulo.centerx
            distancia_y = self.alvo.retangulo.centery - self.retangulo.centery
            magnitude = math.hypot(distancia_x, distancia_y)

            if magnitude != 0:
                tiro.direcao_x = distancia_x / magnitude
                tiro.direcao_y = distancia_y / magnitude
            else:
                tiro.direcao_x = 0
                tiro.direcao_y = 1

            return tiro

        return None