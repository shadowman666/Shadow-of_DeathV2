import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from codigo.constantes import (COR_BRANCA, COR_VERDE, LARGURA_TELA, ALTURA_TELA,
                               EVENTO_INIMIGO, EVENTO_TEMPO, TEMPO_SPAWN,
                               PASSO_TEMPO, TEMPO_FASE)

from codigo.fabrica_entidade import FabricaEntidade
from codigo.mediador_entidade import MediadorEntidade
from codigo.jogador import Jogador
from codigo.chefao import Chefao
from codigo.inimigo import Inimigo


class Fase:
    def __init__(self, janela: Surface, nome: str, modo_jogo: str, pontos_jogador: list[int]):
        self.tempo_limite = TEMPO_FASE
        self.janela = janela
        self.nome = nome
        self.modo_jogo = modo_jogo
        self.lista_entidades = []
        self.boss_ja_nasceu = False

        self.jogador = FabricaEntidade.obter_entidade('Jogador')
        self.jogador.pontuacao = pontos_jogador[0]
        self.lista_entidades.append(self.jogador)

        pygame.time.set_timer(EVENTO_INIMIGO, TEMPO_SPAWN)
        pygame.time.set_timer(EVENTO_TEMPO, PASSO_TEMPO)

        self.mascara_escuridao = Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)

    def executar(self, pontos_jogador: list[int]):

        if self.nome == 'Fase1':
            try:
                pygame.mixer_music.load('./asset/Fase1.wav')
                pygame.mixer_music.set_volume(1.0)
                pygame.mixer_music.play(-1)
            except pygame.error as erro_musica:
                print(f"Aviso - Erro de áudio na fase {self.nome}: {erro_musica}")
        elif self.nome == 'FaseChefao':
            try:
                pygame.mixer_music.stop()
                pygame.mixer_music.load('./asset/FaseChefao.wav')
                pygame.mixer_music.set_volume(1.0)
                pygame.mixer_music.play(-1)
            except pygame.error as erro_musica:
                print(f"Aviso - Erro de áudio na fase {self.nome}: {erro_musica}")

        relogio = pygame.time.Clock()

        while True:
            relogio.tick(60)
            self.janela.fill((0, 0, 0))

            if self.nome != 'FaseChefao':
                self.mascara_escuridao.fill((0, 0, 0, 230))

            vida_jogador = 0
            pontos_hud = 0
            jogador_vivo_hud = False
            vida_boss = None

            for entidade in self.lista_entidades:
                self.janela.blit(source=entidade.superficie, dest=entidade.retangulo)
                entidade.mover()

                if isinstance(entidade, (Jogador, Inimigo, Chefao)):
                    tiro = entidade.atirar()
                    if tiro is not None:
                        self.lista_entidades.append(tiro)
                        if isinstance(entidade, Jogador):
                            try:
                                som_tiro = pygame.mixer.Sound('./asset/tiro_jogador.wav')
                                som_tiro.set_volume(0.4)
                                pygame.mixer.Channel(2).play(som_tiro)
                            except pygame.error:
                                pass
                        elif isinstance(entidade, Chefao):
                            try:
                                som_gosma = pygame.mixer.Sound('./asset/tiro_chefao.wav')
                                som_gosma.set_volume(0.4)
                                pygame.mixer.Channel(3).play(som_gosma)
                            except pygame.error:
                                pass

                if entidade.nome == 'Jogador':
                    vida_jogador = entidade.vida
                    pontos_hud = entidade.pontuacao
                    pontos_jogador[0] = entidade.pontuacao
                    jogador_vivo_hud = True

                    if self.nome != 'FaseChefao':
                        posicao_jogador = (entidade.retangulo.centerx, entidade.retangulo.centery)
                        pygame.draw.circle(self.mascara_escuridao, (0, 0, 0, 0), posicao_jogador, 150)

                if isinstance(entidade, Chefao):
                    vida_boss = entidade.vida

            if self.nome != 'FaseChefao':
                self.janela.blit(self.mascara_escuridao, (0, 0))

            if jogador_vivo_hud:
                texto_status = f'Vida: {vida_jogador} | Pontos: {pontos_hud}'
                self.texto_fase(14, texto_status, COR_VERDE, (10, 25))

            if self.nome == 'FaseChefao':
                self.texto_fase(14, 'BOSS - O tempo é infinito. Sobreviva!', COR_BRANCA, (10, 5))

                if vida_boss is not None and vida_boss > 0:
                    largura_barra = 400
                    altura_barra = 20
                    pos_x = (LARGURA_TELA / 2) - (largura_barra / 2)
                    pos_y = 50

                    pygame.draw.rect(self.janela, (100, 100, 100), (pos_x, pos_y, largura_barra, altura_barra))
                    largura_hp = max(0, min(vida_boss * 4, largura_barra))
                    pygame.draw.rect(self.janela, (255, 0, 0), (pos_x, pos_y, largura_hp, altura_barra))

                    self.texto_fase(16, f'HP BOSS: {vida_boss}', COR_BRANCA, (pos_x + 140, pos_y + 2))
            else:
                tempo_segundos = self.tempo_limite / 1000
                self.texto_fase(14, f'{self.nome} - Tempo: {tempo_segundos:.1f}s', COR_BRANCA, (10, 5))

            self.texto_fase(14, f'FPS: {relogio.get_fps():.0f}', COR_BRANCA, (10, ALTURA_TELA - 35))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == EVENTO_INIMIGO:
                    jogador_atual = next((e for e in self.lista_entidades if isinstance(e, Jogador)), None)

                    if self.nome == 'FaseChefao':
                        if not self.boss_ja_nasceu:
                            self.lista_entidades.append(FabricaEntidade.obter_entidade('Chefao', alvo=jogador_atual))
                            self.boss_ja_nasceu = True
                    else:
                        self.lista_entidades.append(FabricaEntidade.obter_entidade('Zumbi', alvo=jogador_atual))

                if evento.type == EVENTO_TEMPO:
                    if self.nome != 'FaseChefao':
                        self.tempo_limite -= PASSO_TEMPO
                        if self.tempo_limite <= 0:
                            return True

                jogador_vivo = any(isinstance(e, Jogador) for e in self.lista_entidades)
                if not jogador_vivo:
                    return False

            if self.nome == 'FaseChefao' and self.boss_ja_nasceu:
                boss_vivo = any(isinstance(e, Chefao) for e in self.lista_entidades)
                if not boss_vivo:
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return True

            pygame.display.flip()
            MediadorEntidade.verificar_colisao(lista_entidades=self.lista_entidades)
            MediadorEntidade.verificar_vida(lista_entidades=self.lista_entidades)

    def texto_fase(self, tamanho_texto: int, texto: str, cor_texto: tuple, posicao_texto: tuple):
        fonte_texto: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=tamanho_texto)
        superficie_texto: Surface = fonte_texto.render(texto, True, cor_texto).convert_alpha()
        retangulo_texto: Rect = superficie_texto.get_rect(left=posicao_texto[0], top=posicao_texto[1])
        self.janela.blit(source=superficie_texto, dest=retangulo_texto)