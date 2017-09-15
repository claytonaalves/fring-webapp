import os
import json

import database
import firebase

from flask import Blueprint, Response, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename

PASTA_FOTOS_PUBLICACOES = "/home/clayton/working/fring-backend/fotos"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

publicacoes_blueprint = Blueprint("publicacoes", __name__)


# publicacoes?desde=12345678
@publicacoes_blueprint.route('/', methods=['GET', 'POST'])
def index_publicacoes():
    if request.method == 'GET':
        return obtem_publicacoes_deste()
    else:
        return salva_publicacao()

def salva_publicacao():
    publicacao = request.json
    database.salva_publicacao(publicacao)
    #firebase.publica_anuncio_test(anuncio)
    return Response(json.dumps(publicacao), mimetype='application/json')

def obtem_publicacoes_desde():
    guid = request.args.get("guid", "") 
    inicio = request.args.get("desde", "")
    categorias = request.args.get("categorias", "").split(",")
    guid_anunciante = request.args.get("guid_anunciante", "")
    if guid:
        publicacoes = database.obtem_publicacao(guid)
    elif inicio:
        publicacoes = database.obtem_publicacoes_desde(inicio, categorias)
    elif guid_anunciante:
        publicacoes = database.obtem_publicacoes_por_anunciante(guid_anunciante)
    else:
        publicacoes = database.obtem_publicacoes()
    return Response(json.dumps(publicacoes), mimetype="application/json")

@publicacoes_blueprint.route('/<guid_publicacao>')
def obtem_publicacao(guid_publicacao):
    publicacao = database.obtem_publicacao(guid_publicacao)
    return Response(json.dumps(publicacao), mimetype='application/json')

@publicacoes_blueprint.route('/fotos', methods=["GET", "POST"])
def foto_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(PASTA_FOTOS_PUBLICACOES, filename))
            return redirect(url_for('.foto_publicacao', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
    <p><input type=file name=file>
     <input type=submit value=Upload>
    </form>
    '''

@publicacoes_blueprint.route('/foto/<filename>')
def foto_publicacao(filename):
    return send_from_directory(PASTA_FOTOS_PUBLICACOES, filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

