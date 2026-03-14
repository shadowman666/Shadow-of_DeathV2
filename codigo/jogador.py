import pygame
import math
from codigo.constantes import (VELOCIDADE, LARGURA_TELA, ALTURA_TELA,
                               TECLA_CIMA, TECLA_BAIXO, TECLA_ESQUERDA,
                               TECLA_DIREITA, TECLA_ATIRAR, ATRASO_TIRO)
from codigo.entidade import Entidade
from codigo.tiro_jogador import TiroJogador


class Jogador(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)
        self.atraso_tiro = ATRASO_TIRO.get(self.nome, 15)

        self.direcao_x = 1
        self.direcao_y = 0

        self.imagem_original = self.superficie

    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()
        moveu_x = 0
        moveu_y = 0

        if teclas_pressionadas[TECLA_CIMA] and self.retangulo.top > 0:
            self.retangulo.centery -= VELOCIDADE[self.nome]
            moveu_y = -1

        if teclas_pressionadas[TECLA_BAIXO] and self.retangulo.bottom < ALTURA_TELA:
            self.retangulo.centery += VELOCIDADE[self.nome]
            moveu_y = 1

        if teclas_pressionadas[TECLA_ESQUERDA] and self.retangulo.left > 0:
            self.retangulo.centerx -= VELOCIDADE[self.nome]
            moveu_x = -1

        if teclas_pressionadas[TECLA_DIREITA] and self.retangulo.right < LARGURA_TELA:
            self.retangulo.centerx += VELOCIDADE[self.nome]
            moveu_x = 1

        if moveu_x != 0 or moveu_y != 0:
            self.direcao_x = moveu_x
            self.direcao_y = moveu_y

            angulo = math.degrees(math.atan2(-self.direcao_y, self.direcao_x))
            self.superficie = pygame.transform.rotate(self.imagem_original, angulo)

            centro_atual = self.retangulo.center
            self.retangulo = self.superficie.get_rect(center=centro_atual)

    def atirar(self):
        self.atraso_tiro -= 1

        if self.atraso_tiro <= 0:
            self.atraso_tiro = ATRASO_TIRO.get(self.nome, 15)
            teclas_pressionadas = pygame.key.get_pressed()

            if teclas_pressionadas[TECLA_ATIRAR]:
                # 💡 MATEMATICA PARA A BALA SAIR DO CANO DA ARMA
                distancia_frente = 10  # O quao longe do peito a ponta da arma esta
                distancia_lado = 20  # O quao para o lado (ombro direito) a arma esta

                # Normaliza o vetor de direcao
                magnitude = math.hypot(self.direcao_x, self.direcao_y)
                if magnitude != 0:
                    dir_x = self.direcao_x / magnitude
                    dir_y = self.direcao_y / magnitude
                else:
                    dir_x = 1
                    dir_y = 0

                # Calcula o vetor perpendicular (para empurrar a bala para a direita do boneco)
                perp_x = -dir_y
                perp_y = dir_x

                # Aplica o calculo na posicao atual
                pos_x = self.retangulo.centerx + int(dir_x * distancia_frente + perp_x * distancia_lado)
                pos_y = self.retangulo.centery + int(dir_y * distancia_frente + perp_y * distancia_lado)

                tiro = TiroJogador(nome='TiroJogador', posicao=(pos_x, pos_y))
                tiro.direcao_x = self.direcao_x
                tiro.direcao_y = self.direcao_y
                return tiro

        return None