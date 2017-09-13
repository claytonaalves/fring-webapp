from core.database import db

class Cidade(db.Model):

    id_cidade = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    uf = db.Column(db.String(2), nullable=False)

    categorias = db.relationship('Categoria', backref='cidade')

    def __init__(self, nome=None, uf=None):
        self.nome = nome
        self.uf = uf

    def __repr__(self):
        return '%s - %s' % (self.nome, self.uf)

def serializa(cidades):
    result = []
    for cidade in cidades:
        cidade_dict = {
            'id_cidade': cidade.id_cidade,
            'nome': cidade.nome,
            'uf': cidade.uf
        }
        result.append(cidade_dict)
    return result


