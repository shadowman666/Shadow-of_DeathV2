import pygame
from codigo.constantes import (VELOCIDADE, LARGURA_TELA, ALTURA_TELA,
                               TECLA_CIMA, TECLA_BAIXO, TECLA_ESQUERDA,
                               TECLA_DIREITA, TECLA_ATIRAR, ATRASO_TIRO)
from codigo.entidade import Entidade
from codigo.tiro_jogador import TiroJogador


class Jogador(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)
        self.atraso_tiro = ATRASO_TIRO.get(self.nome, 15)

        # Guarda a ultima direcao em que o jogador andou para saber para onde atirar
        self.direcao_x = 1
        self.direcao_y = 0

    def mover(self):
        teclas_pressionadas = pygame.key.get_pressed()
        moveu_x = 0
        moveu_y = 0

        # Movimenta o jogador e guarda a direcao do movimento
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

        # Atualiza a mira se o jogador tiver se movido
        if moveu_x != 0 or moveu_y != 0:
            self.direcao_x = moveu_x
            self.direcao_y = moveu_y

    def atirar(self):
        self.atraso_tiro -= 1

        if self.atraso_tiro <= 0:
            self.atraso_tiro = ATRASO_TIRO.get(self.nome, 15)
            teclas_pressionadas = pygame.key.get_pressed()

            if teclas_pressionadas[TECLA_ATIRAR]:
                tiro = TiroJogador(nome='TiroJogador', posicao=(self.retangulo.centerx, self.retangulo.centery))
                # Passa a direcao atual do jogador para o projetil saber para onde ir
                tiro.direcao_x = self.direcao_x
                tiro.direcao_y = self.direcao_y
                return tiro

        return None