from database import db
from datetime import datetime

class Meal(db.Model):
    __tablename__="meals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime)
    in_diet = db.Column(db.Boolean, default=True)

    # chave estrangeira para o usuário
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relação inversa
    user = db.relationship("User", back_populates="meals")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date_time": self.date_time.isoformat() if self.date_time else None, 
            "in_diet": self.in_diet
        }