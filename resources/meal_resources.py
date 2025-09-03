from flask import Blueprint, request, jsonify
from database import db
from models.meal import Meal
from flask_login import login_required, current_user
from datetime import datetime

meal_bp = Blueprint('meal_bp', __name__)

@meal_bp.route('/meals', methods=["POST"])
@login_required
def create_meal():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    date_time = data.get("date_time")
    in_diet = data.get("in_diet", True)

    if not name:
        return jsonify({"message": "O campo 'name' é obrigatório"}), 400
    
    try:
        date_time = datetime.fromisoformat(date_time) if date_time else datetime.now()
    except ValueError:
        return jsonify({"message": "Formato inválido de data. Use ISO 8601"}), 400
    
    meal = Meal(
        name=name,
        description=description,
        date_time=date_time,
        in_diet=in_diet,
        user_id=current_user.id
        )
    
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeição criada com sucesso", "id": meal.id}), 201

@meal_bp.route('/meals', methods=["GET"])
@login_required
def list_meals():
    meals = Meal.query.filter_by(user_id=current_user.id).all()

    return jsonify([meal.to_dict() for meal in meals]), 200


@meal_bp.route('/meals/<int:id_meal>', methods=["GET"])
@login_required
def get_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if not meal or meal.user_id != current_user.id:
        return jsonify({"message": "Refeição não encontrada"}), 404

    return jsonify(meal.to_dict()), 200


@meal_bp.route('/meals/<int:id_meal>', methods=["PUT"])
@login_required
def update_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if not meal or meal.user_id != current_user.id:
        return jsonify({"message": "Refeição não encontrada"}), 404

    data = request.json
    meal.name = data.get("name", meal.name)
    meal.description = data.get("description", meal.description)
    meal.in_diet = data.get("in_diet", meal.in_diet)
    date_time = data.get("date_time")
    
    if date_time:
        try:
            meal.date_time = datetime.fromisoformat(date_time)
        except ValueError:
            return jsonify({"message": "Formato inválido de data. Use ISO 8601"}), 400
    

    db.session.commit()
    return jsonify({"message": "Refeição atualizada com sucesso"}), 200
    

@meal_bp.route('/meals/<int:id_meal>', methods=["DELETE"])
@login_required
def delete_meal(id_meal):
    meal = Meal.query.get(id_meal)

    if not meal or meal.user_id != current_user.id:
        return jsonify({"message": "Refeição não encontrada"}), 404

    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso"}), 200