from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import requests
import mysql.connector
import json

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/desafioStarW'
db = SQLAlchemy(app)


class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    clima = db.Column(db.String(100))
    terreno = db.Column(db.String(100))

def to_json(self):
        return {"id": self.id, "nome": self.nome, "clima": self.clima, "terreno": self.terreno}


# Selecionar Tudo
@app.route("/planetas", methods=["GET"])
def seleciona_planeta():
    planetas_objetos = Planetas.query.all()
    planetas_json = [planetas.to_json() for planetas in planetas_objetos]

    return gera_response(200, "planetas", planetas_json)

# Selecionar Individual
@app.route("/planetas/<id>", methods=["GET"])
def seleciona_planetas(id):
    planetas_objetos = Planetas.query.filter_by(id=id).first()
    planetas_json = planetas.to_json.to_json()

    return gera_response(200, "planetas", planetas_json)


# Cadastrar
@app.route("/planetas", methods=["POST"])
def cria_planetas():
    body = request.get_json()

    try:
        planetas = Planetas(nome=body["nome"], clima=body["clima"], terreno=body["terreno"])
        db.session.add(planetas)
        db.session.commit()
        return gera_response(201, "planetas", planetas.to_json(), "Criado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "planetas", {}, "Erro ao cadastrar")


# Atualizar
@app.route("/planetas/<id>", methods=["PUT"])
def atualiza_planetas(id):
    planetas_objetos = Planetas.query.filter_by(id=id).first()
    response = requests.get(
        'https://swapi.dev/api/planets/')
    body = response.json()

    try:
        if ('nome' in body):
            planetas_objeto.nome = body['nome']
        if ('clima' in body):
            planetas_objeto.email = body['clima']
        if ('terreno' in body):
            planetas_objeto.email = body['terreno']

        db.session.add(planetas_objeto)
        db.session.commit()
        return gera_response(200, "planetas", planetas_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "planetas", {}, "Erro ao atualizar")


# Deletar
@app.route("/planetas/<id>", methods=["DELETE"])
def deleta_planetas(id):
    planetas_objeto = Planetas.query.filter_by(id=id).first()

    try:
        db.session.delete(planetas_objeto)
        db.session.commit()
        return gera_response(200, "planetas", planetas_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "planetas", {}, "Erro ao deletar")


def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if (mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

