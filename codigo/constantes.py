import pygame

# Dimensoes da tela principal
LARGURA_TELA = 800
ALTURA_TELA = 600

# Definicao de cores em RGB
COR_PRETA = (0, 0, 0)
COR_BRANCA = (255, 255, 255)
COR_VERMELHA = (255, 0, 0)
COR_CINZA = (100, 100, 100)
COR_AMARELA = (255, 255, 128)
COR_VERDE = (0, 255, 0)

# Opcoes disponiveis no menu inicial
OPCOES_MENU = ('NOVO JOGO', 'CONTROLES', 'PONTUACAO', 'SAIR')

# Teclas de controle do jogador
TECLA_CIMA = pygame.K_w
TECLA_BAIXO = pygame.K_s
TECLA_ESQUERDA = pygame.K_a
TECLA_DIREITA = pygame.K_d
TECLA_ATIRAR = pygame.K_l

# Configuracoes de velocidade das entidades
VELOCIDADE = {
    'Jogador': 5,
    'TiroJogador': 12,
    'Zumbi': 4,
    'Chefao': 2
}

# Configuracoes de vida das entidades
VIDA = {
    'Jogador': 1000,
    'TiroJogador': 1,
    'Zumbi': 60,
    'Chefao': 2500
}

# Configuracoes de dano causado ao encostar
DANO = {
    'Jogador': 0,
    'TiroJogador': 20,
    'Zumbi': 2,
    'Chefao': 5
}

# Configuracoes de pontuacao ao derrotar o inimigo
PONTUACAO = {
    'Jogador': 0,
    'Zumbi': 100,
    'Chefao': 5000
}

# Atraso para o disparo
ATRASO_TIRO = {
    'Jogador': 5,
    'Chefao': 50
}

# Eventos customizados do pygame para controle de tempo e inimigos
EVENTO_INIMIGO = pygame.USEREVENT + 1
EVENTO_TEMPO = pygame.USEREVENT + 2

# Controle de tempo de spawn e duracao da fase
TEMPO_SPAWN = 800
PASSO_TEMPO = 100
TEMPO_FASE = 30000

# Posicoes para os textos na tela de pontuacao
POSICAO_PONTUACAO = {
    'Titulo': (LARGURA_TELA / 2, 50),
    'InserirNome': (LARGURA_TELA / 2, 80),
    'Rotulo': (LARGURA_TELA / 2, 90),
    'Nome': (LARGURA_TELA / 2, 110),
    0: (LARGURA_TELA / 2, 150),
    1: (LARGURA_TELA / 2, 170),
    2: (LARGURA_TELA / 2, 190),
    3: (LARGURA_TELA / 2, 210),
    4: (LARGURA_TELA / 2, 230),
    5: (LARGURA_TELA / 2, 250),
    6: (LARGURA_TELA / 2, 270),
    7: (LARGURA_TELA / 2, 290),
    8: (LARGURA_TELA / 2, 310),
    9: (LARGURA_TELA / 2, 330),
}