class Pokemon():
    def __init__(self, id, nome, descricao, data_ano):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_ano = data_ano

    def converte_em_json(self):
        return {
            'id': self.id,
            'nome': self.nome.lower(),
            'descricao': self.descricao.lower(),
            'data_ano': self.data_ano
        }
