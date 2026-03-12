import sqlite3


class BancoProxy:
    def __init__(self, nome_banco: str):
        self.nome_banco = nome_banco
        self.conexao = sqlite3.connect(nome_banco)

        # Cria a tabela de dados caso ela ainda nao exista no banco local
        self.conexao.execute('''
                                CREATE TABLE IF NOT EXISTS dados(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nome TEXT NOT NULL,
                                pontuacao INTEGER NOT NULL,
                                data TEXT NOT NULL)
                             ''')

    def salvar(self, dicionario_pontuacao: dict):
        # Insere o novo recorde do jogador no banco de dados
        consulta = 'INSERT INTO dados (nome, pontuacao, data) VALUES (:nome, :pontuacao, :data)'
        self.conexao.execute(consulta, dicionario_pontuacao)
        self.conexao.commit()

    def recuperar_top10(self) -> list:
        # Busca as 10 maiores pontuacoes ordenadas da maior para a menor
        consulta = 'SELECT * FROM dados ORDER BY pontuacao DESC LIMIT 10'
        return self.conexao.execute(consulta).fetchall()

    def fechar(self):
        # Encerra a conexao com o banco de dados para liberar memoria
        return self.conexao.close()