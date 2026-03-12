import sys
import pygame
from codigo.constantes import LARGURA_TELA, ALTURA_TELA, OPCOES_MENU
from codigo.fase import Fase
from codigo.menu import Menu
from codigo.pontuacao import Pontuacao


class Jogo:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode(size=(LARGURA_TELA, ALTURA_TELA))

    def executar(self):
        while True:
            pontuacao = Pontuacao(self.janela)
            menu = Menu(self.janela)
            retorno_menu = menu.executar()

            # Inicia o jogo no modo Single Player
            if retorno_menu == OPCOES_MENU[0]:
                pontos_jogador = [0]

                # Executa a Fase 1
                fase_1 = Fase(self.janela, 'Fase1', retorno_menu, pontos_jogador)
                passou_fase_1 = fase_1.executar(pontos_jogador)

                if passou_fase_1:
                    # Executa a Fase 2 se passou da Fase 1
                    fase_2 = Fase(self.janela, 'Fase2', retorno_menu, pontos_jogador)
                    passou_fase_2 = fase_2.executar(pontos_jogador)

                    if passou_fase_2:
                        # Executa a Fase do Chefao no final
                        fase_chefao = Fase(self.janela, 'FaseChefao', retorno_menu, pontos_jogador)
                        passou_chefao = fase_chefao.executar(pontos_jogador)

                        if passou_chefao:
                            # Vitoria total: dobra a pontuacao e salva
                            pontos_jogador[0] *= 2
                            pontuacao.salvar(retorno_menu, pontos_jogador)

            # Vai para a tela de pontuacao (Score)
            elif retorno_menu == OPCOES_MENU[1]:
                pontuacao.mostrar()

            # Encerra o jogo
            elif retorno_menu == OPCOES_MENU[2]:
                pygame.quit()
                quit()

            else:
                pygame.quit()
                sys.exit()