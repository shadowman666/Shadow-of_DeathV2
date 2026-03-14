import math
from codigo.constantes import VELOCIDADE
from codigo.entidade import Entidade


class Inimigo(Entidade):
    # Agora o inimigo recebe o jogador como alvo na hora em que nasce
    def __init__(self, nome: str, posicao: tuple, alvo: Entidade = None):
        super().__init__(nome, posicao)
        self.alvo = alvo

    def mover(self):
        # Se nao houver alvo, o zumbi fica parado
        if not self.alvo:
            return

        # Calcula a distancia e a direcao exata entre o zumbi e o jogador
        distancia_x = self.alvo.retangulo.centerx - self.retangulo.centerx
        distancia_y = self.alvo.retangulo.centery - self.retangulo.centery
        magnitude = math.hypot(distancia_x, distancia_y)

        # Move o zumbi na direcao do jogador baseada na velocidade dele
        if magnitude != 0:
            self.retangulo.centerx += int((distancia_x / magnitude) * VELOCIDADE.get(self.nome, 4))
            self.retangulo.centery += int((distancia_y / magnitude) * VELOCIDADE.get(self.nome, 4))

    def atirar(self):
        return None