class Produto():
  def __init__(self, id, nome, categoria, preco):
    self.id
    self.nome
    self.categoria
    self.preco

    def conversao_em_json(self):
      return {
        "id":self.id,
        "nome":self.nome,
        "categoria":self.categoria,
        "preco":self.preco,
      }