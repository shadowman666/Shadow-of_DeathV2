import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from codigo.constantes import (LARGURA_TELA, ALTURA_TELA, COR_VERMELHA,
                               COR_BRANCA, COR_CINZA, COR_PRETA, OPCOES_MENU)


class Menu:
    def __init__(self, janela: Surface):
        self.janela = janela
        # Tenta carregar a imagem de fundo do menu
        try:
            self.superficie = pygame.image.load('./asset/MenuBg.png').convert_alpha()
            self.superficie = pygame.transform.scale(self.superficie, (LARGURA_TELA, ALTURA_TELA))
        except (FileNotFoundError, pygame.error):  # <--- CORREÇÃO AQUI
            self.superficie = Surface((LARGURA_TELA, ALTURA_TELA))
            self.superficie.fill(COR_PRETA)

        self.retangulo = self.superficie.get_rect(left=0, top=0)

    def executar(self):
        opcao_menu = 0

        # Tenta iniciar a musica de fundo do menu
        try:
            pygame.mixer_music.load('./asset/Menu.mp3')
            pygame.mixer_music.play(-1)
        except (FileNotFoundError, pygame.error):  # <--- CORREÇÃO AQUI
            pass

        while True:
            self.janela.blit(source=self.superficie, dest=self.retangulo)

            self.texto_menu(70, "Shadow", COR_VERMELHA, ((LARGURA_TELA / 2), 100))
            self.texto_menu(70, "of Death", COR_VERMELHA, ((LARGURA_TELA / 2), 160))

            for i in range(len(OPCOES_MENU)):
                if i == opcao_menu:
                    self.texto_menu(30, OPCOES_MENU[i], COR_VERMELHA, ((LARGURA_TELA / 2), 300 + 40 * i))
                else:
                    self.texto_menu(30, OPCOES_MENU[i], COR_BRANCA, ((LARGURA_TELA / 2), 300 + 40 * i))

            instrucoes = "CONTROLES: W A S D - Mover | L - Atirar"
            self.texto_menu(20, instrucoes, COR_CINZA, ((LARGURA_TELA / 2), ALTURA_TELA - 30))

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                        if opcao_menu < len(OPCOES_MENU) - 1:
                            opcao_menu += 1
                        else:
                            opcao_menu = 0
                    if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                        if opcao_menu > 0:
                            opcao_menu -= 1
                        else:
                            opcao_menu = len(OPCOES_MENU) - 1
                    if evento.key == pygame.K_RETURN:
                        return OPCOES_MENU[opcao_menu]

    def texto_menu(self, tamanho_texto: int, texto: str, cor_texto: tuple, posicao_centro: tuple):
        fonte_texto: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=tamanho_texto)
        superficie_texto: Surface = fonte_texto.render(texto, True, cor_texto).convert_alpha()
        retangulo_texto: Rect = superficie_texto.get_rect(center=posicao_centro)
        self.janela.blit(source=superficie_texto, dest=retangulo_texto)