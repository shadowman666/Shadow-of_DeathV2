import math
from codigo.constantes import VELOCIDADE
from codigo.entidade import Entidade


class TiroJogador(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)
        # Direcao padrao inicial do projetil
        self.direcao_x = 1
        self.direcao_y = 0

    def mover(self):
        # Garante que o tiro ande na mesma velocidade mesmo atirando na diagonal
        magnitude = math.hypot(self.direcao_x, self.direcao_y)

        if magnitude != 0:
            self.retangulo.centerx += int((self.direcao_x / magnitude) * VELOCIDADE[self.nome])
            self.retangulo.centery += int((self.direcao_y / magnitude) * VELOCIDADE[self.nome])