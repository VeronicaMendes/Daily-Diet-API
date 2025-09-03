from flask import Flask
from database import db
from flask_login import LoginManager

app =  Flask(__name__)
app.config['SECRET_KEY'] = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)



if __name__ == '__main__':
    app.run(debug=True)