import random
from codigo.constantes import LARGURA_TELA, ALTURA_TELA
from codigo.fundo import Fundo
from codigo.jogador import Jogador
from codigo.inimigo import Inimigo
from codigo.chefao import Chefao


class FabricaEntidade:
    @staticmethod
    def obter_entidade(nome_entidade: str, alvo=None):
        match nome_entidade:
            case 'Fase1Fundo' | 'Fase2Fundo' | 'FaseChefaoFundo':
                lista_fundo = []
                for i in range(7):
                    lista_fundo.append(Fundo(f'{nome_entidade}{i}', (0, 0)))
                    lista_fundo.append(Fundo(f'{nome_entidade}{i}', (LARGURA_TELA, 0)))
                return lista_fundo

            case 'Jogador':
                # O jogador agora nasce bem no centro da arena de terror
                return Jogador('Jogador', (LARGURA_TELA / 2, ALTURA_TELA / 2))

            case 'Zumbi':
                # Escolhe uma borda aleatoria (cima, baixo, esquerda ou direita) para o zumbi nascer
                borda = random.choice(['cima', 'baixo', 'esquerda', 'direita'])

                if borda == 'cima':
                    pos_x = random.randint(0, LARGURA_TELA)
                    pos_y = -40
                elif borda == 'baixo':
                    pos_x = random.randint(0, LARGURA_TELA)
                    pos_y = ALTURA_TELA + 40
                elif borda == 'esquerda':
                    pos_x = -40
                    pos_y = random.randint(0, ALTURA_TELA)
                else:
                    pos_x = LARGURA_TELA + 40
                    pos_y = random.randint(0, ALTURA_TELA)

                return Inimigo('Zumbi', (pos_x, pos_y), alvo)

            case 'Chefao':
                # O chefao sempre vai nascer do topo, fora da visao da lanterna
                return Chefao('Chefao', (LARGURA_TELA / 2, -100), alvo)