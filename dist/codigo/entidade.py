from abc import ABC, abstractmethod
import pygame
from codigo.constantes import VIDA, DANO, PONTUACAO


class Entidade(ABC):
    def __init__(self, nome: str, posicao: tuple):
        self.nome = nome

        try:
            self.superficie = pygame.image.load(f'./asset/{nome}.png').convert_alpha()
        except (FileNotFoundError, pygame.error):  # <--- CORREÇÃO AQUI
            self.superficie = pygame.Surface((40, 40))
            self.superficie.fill((255, 0, 0))

        self.retangulo = self.superficie.get_rect(left=posicao[0], top=posicao[1])
        self.velocidade = 0

        self.vida = VIDA.get(self.nome, 100)
        self.dano = DANO.get(self.nome, 0)
        self.pontuacao = PONTUACAO.get(self.nome, 0)
        self.ultimo_dano = 'Nenhum'

    @abstractmethod
    def mover(self):
        pass