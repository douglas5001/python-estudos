class Usuario():
    def __init__(self, id, nome, data_nascimento):
        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento

    def converte_em_json(self):
        return {
            'id':self.id,
            'nome':self.nome,
            'data_nascimento':self.data_nascimento,
        }
        
    