import sys
from datetime import datetime
import pygame
from pygame import Surface, Rect, KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from codigo.constantes import LARGURA_TELA, ALTURA_TELA, COR_AMARELA, COR_BRANCA, POSICAO_PONTUACAO
from codigo.banco_proxy import BancoProxy


class Pontuacao:
    def __init__(self, janela: Surface):
        self.janela = janela

        try:
            self.superficie = pygame.image.load('./asset/ScoreBg.png').convert_alpha()
            self.superficie = pygame.transform.scale(self.superficie, (LARGURA_TELA, ALTURA_TELA))
        except (FileNotFoundError, pygame.error):  # <--- CORREÇÃO AQUI
            self.superficie = Surface((LARGURA_TELA, ALTURA_TELA))
            self.superficie.fill((0, 0, 0))

        self.retangulo = self.superficie.get_rect(left=0, top=0)

    def salvar(self, modo_jogo: str, pontos_jogador: list[int]):
        try:
            pygame.mixer_music.load('./asset/Score.mp3')
            pygame.mixer_music.play(-1)
        except (FileNotFoundError, pygame.error):  # <--- CORREÇÃO AQUI
            pass

        banco_proxy = BancoProxy('BancoPontuacao')
        nome_jogador = ''

        while True:
            self.janela.blit(source=self.superficie, dest=self.retangulo)
            self.texto_pontuacao(48, 'VITORIA!!', COR_AMARELA, POSICAO_PONTUACAO['Titulo'])

            instrucao = 'Digite seu nome (4 letras) e de ENTER:'
            pontos = pontos_jogador[0]

            self.texto_pontuacao(20, instrucao, COR_BRANCA, POSICAO_PONTUACAO['InserirNome'])

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == KEYDOWN:
                    if evento.key == K_RETURN and len(nome_jogador) == 4:
                        dados = {'nome': nome_jogador, 'pontuacao': pontos, 'data': obter_data_formatada()}
                        banco_proxy.salvar(dados)
                        self.mostrar()
                        return
                    elif evento.key == K_BACKSPACE:
                        nome_jogador = nome_jogador[:-1]
                    else:
                        if len(nome_jogador) < 4:
                            nome_jogador += evento.unicode.upper()

            self.texto_pontuacao(30, nome_jogador, COR_BRANCA, POSICAO_PONTUACAO['Nome'])
            pygame.display.flip()

    def mostrar(self):
        try:
            pygame.mixer_music.load('./asset/Score.mp3')
            pygame.mixer_music.play(-1)
        except (FileNotFoundError, pygame.error):  # <--- CORREÇÃO AQUI
            pass

        self.janela.blit(source=self.superficie, dest=self.retangulo)
        self.texto_pontuacao(48, 'TOP 10 PONTUACOES', COR_AMARELA, POSICAO_PONTUACAO['Titulo'])
        self.texto_pontuacao(20, 'NOME     PONTOS          DATA      ', COR_AMARELA, POSICAO_PONTUACAO['Rotulo'])

        banco_proxy = BancoProxy('BancoPontuacao')
        lista_pontuacoes = banco_proxy.recuperar_top10()
        banco_proxy.fechar()

        for pontuacao in lista_pontuacoes:
            id_banco, nome, pontos, data = pontuacao
            texto_linha = f'{nome}     {pontos:05d}           {data}'
            indice_posicao = lista_pontuacoes.index(pontuacao)
            self.texto_pontuacao(20, texto_linha, COR_AMARELA, POSICAO_PONTUACAO[indice_posicao])

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == KEYDOWN:
                    if evento.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def texto_pontuacao(self, tamanho_texto: int, texto: str, cor_texto: tuple, posicao_centro: tuple):
        fonte_texto: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=tamanho_texto)
        superficie_texto: Surface = fonte_texto.render(texto, True, cor_texto).convert_alpha()
        retangulo_texto: Rect = superficie_texto.get_rect(center=posicao_centro)
        self.janela.blit(source=superficie_texto, dest=retangulo_texto)


def obter_data_formatada():
    data_atual = datetime.now()
    hora = data_atual.strftime("%H:%M")
    data = data_atual.strftime("%d/%m/%y")
    return f"{hora} - {data}"