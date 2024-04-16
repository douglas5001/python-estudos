class Filmes():
    def __init__(self,id, nome,descricao,ano):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ano = ano

    def converte_em_json(self):
        return {
            "id":self.id,
            "nome":self.nome,
            "descricao":self.descricao,
            "ano":self.ano
        }