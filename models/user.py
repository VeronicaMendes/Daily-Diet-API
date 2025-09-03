from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    # relação com refeições
    meals = db.relationship(
        "Meal",
        back_populates="user",
        cascade="all, delete-orphan"
    )