import random
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
from codigo.inimigo import Inimigo


class Fase:
    def __init__(self, janela: Surface, nome: str, modo_jogo: str, pontos_jogador: list[int]):
        self.tempo_limite = TEMPO_FASE
        self.janela = janela
        self.nome = nome
        self.modo_jogo = modo_jogo
        self.lista_entidades = []

        # Carrega as imagens de fundo da fase
        self.lista_entidades.extend(FabricaEntidade.obter_entidade(self.nome + 'Fundo'))

        # Instancia o jogador e recupera a pontuacao dele das fases anteriores
        self.jogador = FabricaEntidade.obter_entidade('Jogador')
        self.jogador.pontuacao = pontos_jogador[0]
        self.lista_entidades.append(self.jogador)

        # Configura os temporizadores de surgimento de inimigos e contagem de tempo
        pygame.time.set_timer(EVENTO_INIMIGO, TEMPO_SPAWN)
        pygame.time.set_timer(EVENTO_TEMPO, PASSO_TEMPO)

        # Superficie preta com suporte a transparencia para o efeito de escuridao
        self.mascara_escuridao = Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)

    def executar(self, pontos_jogador: list[int]):
        # Carrega a musica especifica da fase
        try:
            pygame.mixer_music.load(f'./asset/{self.nome}.mp3')
            pygame.mixer_music.set_volume(0.3)
            pygame.mixer_music.play(-1)
        except (FileNotFoundError, pygame.error):
            pass

        relogio = pygame.time.Clock()

        while True:
            relogio.tick(60)

            # Pinta a mascara de escuridao (Preto com 230 de opacidade)
            self.mascara_escuridao.fill((0, 0, 0, 230))

            # Desenha e processa as entidades
            for entidade in self.lista_entidades:
                self.janela.blit(source=entidade.superficie, dest=entidade.retangulo)
                entidade.mover()

                # Executa a logica de tiro caso a entidade possa atirar
                if isinstance(entidade, (Jogador, Inimigo)):
                    tiro = entidade.atirar()
                    if tiro is not None:
                        self.lista_entidades.append(tiro)

                # Atualiza a interface (HUD) do jogador e faz o recorte da lanterna
                if entidade.nome == 'Jogador':
                    texto_status = f'Vida: {entidade.vida} | Pontos: {entidade.pontuacao}'
                    self.texto_fase(14, texto_status, COR_VERDE, (10, 25))
                    pontos_jogador[0] = entidade.pontuacao

                    # Desenha um circulo transparente na mascara de escuridao sobre o jogador
                    posicao_jogador = (entidade.retangulo.centerx, entidade.retangulo.centery)
                    pygame.draw.circle(self.mascara_escuridao, (0, 0, 0, 0), posicao_jogador, 150)

            # Aplica a escuridao sobre a janela do jogo
            self.janela.blit(self.mascara_escuridao, (0, 0))

            # Captura de eventos do teclado e do sistema
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Evento para criar um novo inimigo no cenario
                if evento.type == EVENTO_INIMIGO:
                    # Busca o jogador atual na lista para passar como alvo (previne erros se o jogador morrer)
                    jogador_atual = None
                    for entidade in self.lista_entidades:
                        if isinstance(entidade, Jogador):
                            jogador_atual = entidade
                            break

                    if self.nome == 'FaseChefao':
                        # Passa o jogador como alvo para o chefao perseguir
                        self.lista_entidades.append(FabricaEntidade.obter_entidade('Chefao', alvo=jogador_atual))
                    else:
                        # Passa o jogador como alvo para o zumbi perseguir
                        self.lista_entidades.append(FabricaEntidade.obter_entidade('Zumbi', alvo=jogador_atual))

                # Evento para decrementar o tempo da fase
                if evento.type == EVENTO_TEMPO:
                    self.tempo_limite -= PASSO_TEMPO
                    if self.tempo_limite <= 0:
                        return True

                # Verifica se o jogador continua vivo na lista de entidades
                jogador_vivo = False
                for entidade in self.lista_entidades:
                    if isinstance(entidade, Jogador):
                        jogador_vivo = True
                        break

                # Game over: Retorna Falso para quebrar o loop das fases no jogo.py
                if not jogador_vivo:
                    return False

            # Exibe os textos de tempo e FPS que ficam sobre a escuridao
            tempo_segundos = self.tempo_limite / 1000
            self.texto_fase(14, f'{self.nome} - Tempo: {tempo_segundos:.1f}s', COR_BRANCA, (10, 5))
            self.texto_fase(14, f'FPS: {relogio.get_fps():.0f}', COR_BRANCA, (10, ALTURA_TELA - 35))

            pygame.display.flip()

            # Verifica as colisoes e remove entidades mortas
            MediadorEntidade.verificar_colisao(lista_entidades=self.lista_entidades)
            MediadorEntidade.verificar_vida(lista_entidades=self.lista_entidades)

    def texto_fase(self, tamanho_texto: int, texto: str, cor_texto: tuple, posicao_texto: tuple):
        # Renderiza a fonte na tela nas posicoes indicadas
        fonte_texto: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=tamanho_texto)
        superficie_texto: Surface = fonte_texto.render(texto, True, cor_texto).convert_alpha()
        retangulo_texto: Rect = superficie_texto.get_rect(left=posicao_texto[0], top=posicao_texto[1])
        self.janela.blit(source=superficie_texto, dest=retangulo_texto)