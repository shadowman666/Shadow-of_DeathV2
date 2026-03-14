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
        except pygame.error:
            self.superficie = Surface((LARGURA_TELA, ALTURA_TELA))
            self.superficie.fill((0, 0, 0))

        self.retangulo = self.superficie.get_rect(left=0, top=0)

    def salvar(self, _modo_jogo: str, pontos_jogador: list[int], vitoria: bool = True):
        try:
            pygame.mixer_music.stop()
            musica_final = './asset/Score.wav' if vitoria else './asset/GameOver.wav'
            pygame.mixer_music.load(musica_final)
            pygame.mixer_music.set_volume(1.0)
            pygame.mixer_music.play(-1)
        except pygame.error:
            pass

        banco_proxy = BancoProxy('BancoPontuacao')
        nome_jogador = ''
        pontos = pontos_jogador[0]

        titulo = 'VITORIA!!' if vitoria else 'FIM DE JOGO'
        cor_titulo = COR_AMARELA if vitoria else (255, 0, 0)

        if vitoria:
            fundo_atual = self.superficie
        else:
            try:
                fundo_atual = pygame.image.load('./asset/GameOverBg.png').convert_alpha()
                fundo_atual = pygame.transform.scale(fundo_atual, (LARGURA_TELA, ALTURA_TELA))
            except pygame.error:
                fundo_atual = Surface((LARGURA_TELA, ALTURA_TELA))
                fundo_atual.fill((0, 0, 0))

        retangulo_fundo = fundo_atual.get_rect(left=0, top=0)

        while True:
            # Limpeza de tela necessaria para o input de texto nao sobrepor frames antigos
            self.janela.fill((0, 0, 0))
            self.janela.blit(source=fundo_atual, dest=retangulo_fundo)

            if vitoria:
                self.texto_pontuacao(48, titulo, cor_titulo, POSICAO_PONTUACAO['Titulo'])

                posicao_demo = (POSICAO_PONTUACAO['Titulo'][0], POSICAO_PONTUACAO['Titulo'][1] + 60)
                self.texto_pontuacao(25, "OBRIGADO POR JOGAR ESTA DEMO!!!", (0, 255, 0), posicao_demo)

                # Ajuste apenas aqui: movido para baixo para nao sobrepor o texto verde
                self.texto_pontuacao(20, 'Digite seu nome (4 letras) e de ENTER:', COR_BRANCA, (LARGURA_TELA / 2, 400))
                self.texto_pontuacao(40, nome_jogador, COR_BRANCA, (LARGURA_TELA / 2, 470))

            else:
                # Mantido exatamente como no seu codigo original
                self.texto_pontuacao(48, titulo, cor_titulo, POSICAO_PONTUACAO['Titulo'])

                posicao_demo = (POSICAO_PONTUACAO['Titulo'][0], POSICAO_PONTUACAO['Titulo'][1] + 60)
                self.texto_pontuacao(25, "OBRIGADO POR JOGAR ESTA DEMO!!!", (0, 255, 0), posicao_demo)

                self.texto_pontuacao(22, f'PONTUACAO FINAL: {pontos}', COR_BRANCA, (LARGURA_TELA / 2, 150))
                self.texto_pontuacao(20, 'Digite seu nome (4 letras) e de ENTER:', COR_BRANCA, (LARGURA_TELA / 2, 170))
                self.texto_pontuacao(40, nome_jogador, COR_AMARELA, (LARGURA_TELA / 2, 200))

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
                            if evento.unicode.isalnum():
                                nome_jogador += evento.unicode.upper()

            pygame.display.flip()

    def mostrar(self):
        try:
            pygame.mixer_music.load('./asset/Score.wav')
            pygame.mixer_music.play(-1)
        except pygame.error:
            pass

        self.janela.blit(source=self.superficie, dest=self.retangulo)

        self.texto_pontuacao(48, 'TOP 10 PONTUACOES', COR_AMARELA, POSICAO_PONTUACAO['Titulo'])
        self.texto_pontuacao(20, 'NOME     PONTOS          DATA      ', COR_AMARELA, POSICAO_PONTUACAO['Rotulo'])

        banco_proxy = BancoProxy('BancoPontuacao')
        lista_pontuacoes = banco_proxy.recuperar_top10()
        banco_proxy.fechar()

        cor_dados = (0, 255, 255)

        for pontuacao in lista_pontuacoes:
            id_banco, nome, pontos, data = pontuacao
            texto_linha = f'{nome}     {pontos:05d}           {data}'
            indice_posicao = lista_pontuacoes.index(pontuacao)
            self.texto_pontuacao(20, texto_linha, cor_dados, POSICAO_PONTUACAO[indice_posicao])

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == KEYDOWN:
                    if evento.key in [K_ESCAPE, K_RETURN]:
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