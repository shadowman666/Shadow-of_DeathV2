from codigo.constantes import VELOCIDADE
from codigo.entidade import Entidade


class TiroInimigo(Entidade):
    def __init__(self, nome: str, posicao: tuple):
        super().__init__(nome, posicao)
        self.velocidade_tiro = VELOCIDADE.get(self.nome, 6)

        # Direcao padrao do ataque do inimigo
        self.direcao_x = 0
        self.direcao_y = 1

    def mover(self):
        # O tiro viaja na direcao calculada pelo chefao
        self.retangulo.centerx += int(self.direcao_x * self.velocidade_tiro)
        self.retangulo.centery += int(self.direcao_y * self.velocidade_tiro)