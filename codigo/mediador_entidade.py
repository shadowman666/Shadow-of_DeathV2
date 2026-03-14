import pygame
from codigo.constantes import LARGURA_TELA, ALTURA_TELA
from codigo.inimigo import Inimigo
from codigo.chefao import Chefao
from codigo.jogador import Jogador
from codigo.tiro_jogador import TiroJogador
from codigo.tiro_inimigo import TiroInimigo


class MediadorEntidade:

    @staticmethod
    def __tocar_som(caminho_som: str, id_canal: int = -1):
        # Tenta tocar o efeito sonoro em wav e avisa no console se falhar
        try:
            som = pygame.mixer.Sound(caminho_som)
            if id_canal != -1:
                # Usa um canal especifico para impedir que o som fique sobreposto e alto
                pygame.mixer.Channel(id_canal).play(som)
            else:
                # Toca em qualquer canal livre
                som.play()
        except Exception as erro_som:
            print(f"Aviso - Falha ao tocar o som {caminho_som}: {erro_som}")

    @staticmethod
    def __verificar_colisao_janela(entidade):
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

                # Aplica o dano cruzado
                ent1.vida -= ent2.dano
                ent2.vida -= ent1.dano
                ent1.ultimo_dano = ent2.nome
                ent2.ultimo_dano = ent1.nome

                # Toca o dano APENAS do Jogador no Canal 0
                if isinstance(ent1, Jogador) and ent1.vida > 0:
                    MediadorEntidade.__tocar_som('./asset/dano_jogador.wav', id_canal=0)
                elif isinstance(ent2, Jogador) and ent2.vida > 0:
                    MediadorEntidade.__tocar_som('./asset/dano_jogador.wav', id_canal=0)

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

                # Trata a morte do Zumbi (Inimigo comum)
                if isinstance(entidade, Inimigo):
                    MediadorEntidade.__dar_pontuacao(entidade, lista_entidades)
                    MediadorEntidade.__tocar_som('./asset/morte_monstro.wav', id_canal=1)

                # Trata a morte do Chefao com um som exclusivo
                elif isinstance(entidade, Chefao):
                    MediadorEntidade.__dar_pontuacao(entidade, lista_entidades)
                    MediadorEntidade.__tocar_som('./asset/morte_chefao.wav', id_canal=1)

                # Trata a morte do Jogador
                elif isinstance(entidade, Jogador):
                    # Puxa o freio de emergencia para silenciar a arena
                    pygame.mixer.stop()
                    MediadorEntidade.__tocar_som('./asset/morte_jogador.wav', id_canal=0)

                lista_entidades.remove(entidade)