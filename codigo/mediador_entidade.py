import pygame
from codigo.constantes import LARGURA_TELA, ALTURA_TELA
from codigo.inimigo import Inimigo
from codigo.chefao import Chefao
from codigo.jogador import Jogador
from codigo.tiro_jogador import TiroJogador
from codigo.tiro_inimigo import TiroInimigo


class MediadorEntidade:

    @staticmethod
    def __tocar_som(caminho_som: str):
        try:
            som = pygame.mixer.Sound(caminho_som)
            som.play()
        except (FileNotFoundError, pygame.error):
            pass

    @staticmethod
    def __verificar_colisao_janela(entidade):
        # Inimigos não morrem mais ao sair da tela, pois nascem fora dela.
        # Apenas tiros perdidos sao destruidos ao sair da visao para poupar memoria.
        if isinstance(entidade, (TiroJogador, TiroInimigo)):
            if (entidade.retangulo.right <= 0 or entidade.retangulo.left >= LARGURA_TELA or
                    entidade.retangulo.bottom <= 0 or entidade.retangulo.top >= ALTURA_TELA):
                entidade.vida = 0

    @staticmethod
    def __verificar_colisao_entidade(ent1, ent2):
        interacao_valida = False

        if isinstance(ent1, (Inimigo, Chefao)) and isinstance(ent2, TiroJogador):
            interacao_valida = True
        elif isinstance(ent1, TiroJogador) and isinstance(ent2, (Inimigo, Chefao)):
            interacao_valida = True
        elif isinstance(ent1, Jogador) and isinstance(ent2, TiroInimigo):
            interacao_valida = True
        elif isinstance(ent1, TiroInimigo) and isinstance(ent2, Jogador):
            interacao_valida = True
        elif isinstance(ent1, Jogador) and isinstance(ent2, (Inimigo, Chefao)):
            interacao_valida = True
        elif isinstance(ent1, (Inimigo, Chefao)) and isinstance(ent2, Jogador):
            interacao_valida = True

        if interacao_valida:
            if (ent1.retangulo.right >= ent2.retangulo.left and
                    ent1.retangulo.left <= ent2.retangulo.right and
                    ent1.retangulo.bottom >= ent2.retangulo.top and
                    ent1.retangulo.top <= ent2.retangulo.bottom):

                ent1.vida -= ent2.dano
                ent2.vida -= ent1.dano
                ent1.ultimo_dano = ent2.nome
                ent2.ultimo_dano = ent1.nome

                if isinstance(ent1, Jogador) or isinstance(ent2, Jogador):
                    MediadorEntidade.__tocar_som('./asset/dano_jogador.mp3')
                if isinstance(ent1, (Inimigo, Chefao)) or isinstance(ent2, (Inimigo, Chefao)):
                    MediadorEntidade.__tocar_som('./asset/dano_monstro.mp3')

    @staticmethod
    def __dar_pontuacao(inimigo, lista_entidades: list):
        if inimigo.ultimo_dano == 'TiroJogador':
            for entidade in lista_entidades:
                if entidade.nome == 'Jogador':
                    entidade.pontuacao += inimigo.pontuacao

    @staticmethod
    def verificar_colisao(lista_entidades: list):
        for i in range(len(lista_entidades)):
            entidade1 = lista_entidades[i]
            MediadorEntidade.__verificar_colisao_janela(entidade1)
            for j in range(i + 1, len(lista_entidades)):
                entidade2 = lista_entidades[j]
                MediadorEntidade.__verificar_colisao_entidade(entidade1, entidade2)

    @staticmethod
    def verificar_vida(lista_entidades: list):
        for entidade in lista_entidades.copy():
            if entidade.vida <= 0:
                if isinstance(entidade, (Inimigo, Chefao)):
                    MediadorEntidade.__dar_pontuacao(entidade, lista_entidades)
                    MediadorEntidade.__tocar_som('./asset/morte_monstro.mp3')
                elif isinstance(entidade, Jogador):
                    MediadorEntidade.__tocar_som('./asset/morte_jogador.mp3')

                lista_entidades.remove(entidade)