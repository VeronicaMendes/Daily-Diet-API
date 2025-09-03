from flask import Blueprint, request, jsonify
from database import db 
from models.user import User
from flask_login import login_user, current_user, logout_user, login_required

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Usuário e senha são obrigatórios"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return jsonify({"message": "Autenticação realizada com sucesso"}), 200

    return jsonify({"message": "Credenciais inválidas"}), 400


@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})

@user_bp.route('/user', methods=["POST"])
def creat_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Dados invalidos"}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    

@user_bp.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if not user: 
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    return {"username": user.username}
    

@user_bp.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    user.password = data.get("password")
    db.session.commit()

    return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"}), 200

@user_bp.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user != current_user.id:
        return jsonify({"message": "Deleção não permitida"}), 403

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Usuário {id_user} deletado com sucesso!"}), 200