import math
from codigo.constantes import VELOCIDADE, ATRASO_TIRO
from codigo.entidade import Entidade
from codigo.tiro_inimigo import TiroInimigo


class Chefao(Entidade):
    def __init__(self, nome: str, posicao: tuple, alvo: Entidade = None):
        super().__init__(nome, posicao)
        self.alvo = alvo
        self.atraso_tiro = ATRASO_TIRO.get(self.nome, 50)

    def mover(self):
        if not self.alvo:
            return

        # O chefao persegue o jogador pela arena de forma similar ao zumbi, porem mais lento
        distancia_x = self.alvo.retangulo.centerx - self.retangulo.centerx
        distancia_y = self.alvo.retangulo.centery - self.retangulo.centery
        magnitude = math.hypot(distancia_x, distancia_y)

        if magnitude != 0:
            self.retangulo.centerx += int((distancia_x / magnitude) * VELOCIDADE.get(self.nome, 2))
            self.retangulo.centery += int((distancia_y / magnitude) * VELOCIDADE.get(self.nome, 2))

    def atirar(self):
        self.atraso_tiro -= 1

        if self.atraso_tiro <= 0 and self.alvo:
            self.atraso_tiro = ATRASO_TIRO.get(self.nome, 50)
            tiro = TiroInimigo(nome='TiroChefao', posicao=(self.retangulo.centerx, self.retangulo.centery))

            # Calcula a trajetoria do tiro para ir diretamente onde o jogador esta agora
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