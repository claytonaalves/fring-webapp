from flask import Blueprint, flash, redirect, render_template
from app import db
from app.auth.forms import CadastroForm
from app.anunciantes.models import Anunciante
from app.cidades.models import Cidade

auth = Blueprint('auth', __name__, url_prefix='/cadastro')

@auth.route('/', methods=['GET', 'POST'])
def index():
    form = CadastroForm()
    if form.validate_on_submit():
        salva_cadastro_anunciante(form)
        flash('Cadastro efetuado!')
        return redirect('/')
    return render_template('auth/cadastro.html', form=form)

def salva_cadastro_anunciante(form):
    anunciante = Anunciante()
    anunciante.nome_fantasia = form.nome_fantasia.data
    anunciante.razao_social = form.razao_social.data
    anunciante.id_cidade = int(form.cidade.data)
    anunciante.id_categoria = int(form.categoria.data)
    anunciante.telefone = form.telefone.data
    anunciante.celular = form.celular.data
    anunciante.logradouro = form.logradouro.data
    anunciante.numero = form.numero.data
    anunciante.bairro = form.numero.data
    anunciante.email = form.email.data
    anunciante.senha = form.senha.data
    db.session.add(anunciante)
    db.session.commit()
