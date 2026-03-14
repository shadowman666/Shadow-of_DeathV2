import sys
import pygame
from codigo.constantes import LARGURA_TELA, ALTURA_TELA, OPCOES_MENU, COR_BRANCA, COR_AMARELA
from codigo.fase import Fase
from codigo.menu import Menu
from codigo.pontuacao import Pontuacao


class Jogo:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode(size=(LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Shadow of Death")

    def tela_transicao(self, texto: str):
        self.janela.fill((0, 0, 0))
        fonte = pygame.font.SysFont(name="Lucida Sans Typewriter", size=60)
        texto_render = fonte.render(texto, True, COR_BRANCA)
        retangulo = texto_render.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))
        self.janela.blit(texto_render, retangulo)
        pygame.display.flip()
        pygame.time.delay(2000)

    def tela_controles(self):
        while True:
            self.janela.fill((0, 0, 0))
            fonte_titulo = pygame.font.SysFont(name="Lucida Sans Typewriter", size=50)
            fonte_texto = pygame.font.SysFont(name="Lucida Sans Typewriter", size=25)

            titulo = fonte_titulo.render("CONTROLES", True, COR_AMARELA)
            self.janela.blit(titulo, (LARGURA_TELA / 2 - 130, 100))

            instrucoes = [
                "W - Mover para Cima",
                "S - Mover para Baixo",
                "A - Mover para Esquerda",
                "D - Mover para Direita",
                "L - Atirar",
                "ESC   - Voltar ao Menu",
                "ENTER - Confirmar"
            ]

            for i, linha in enumerate(instrucoes):
                texto_render = fonte_texto.render(linha, True, COR_BRANCA)
                self.janela.blit(texto_render, (150, 220 + (i * 40)))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                        return

    def executar(self):
        while True:
            pontuacao = Pontuacao(self.janela)
            menu = Menu(self.janela)
            retorno_menu = menu.executar()

            if retorno_menu == OPCOES_MENU[0]:
                pontos_jogador = [0]
                fases = ['Fase1', 'Fase2', 'FaseChefao']
                vitoria_total = True

                for nome_fase in fases:
                    if nome_fase == 'Fase1':
                        self.tela_transicao("FASE 1")
                    elif nome_fase == 'Fase2':
                        self.tela_transicao("FASE 2")
                    elif nome_fase == 'FaseChefao':
                        self.tela_transicao("BOSS")

                    fase = Fase(self.janela, nome_fase, retorno_menu, pontos_jogador)
                    passou_fase = fase.executar(pontos_jogador)

                    if not passou_fase:
                        vitoria_total = False
                        pontuacao.salvar(retorno_menu, pontos_jogador, vitoria=False)
                        break

                if vitoria_total:
                    pontos_jogador[0] *= 2
                    pontuacao.salvar(retorno_menu, pontos_jogador, vitoria=True)

            elif retorno_menu == OPCOES_MENU[1]:
                self.tela_controles()

            elif retorno_menu == OPCOES_MENU[2]:
                pontuacao.mostrar()

            elif retorno_menu == OPCOES_MENU[3]:
                pygame.quit()
                sys.exit()