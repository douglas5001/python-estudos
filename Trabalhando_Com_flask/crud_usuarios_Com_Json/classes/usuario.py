class Usuario():
    def __init__(self, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha
        
    def converte_em_json(self):
        return {
            self.id:'id',
            self.nome:'nome',
            self.senha:'senha'
        }
    