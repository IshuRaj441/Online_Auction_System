from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from auth import auth
from admin import admin
from sockets import socketio, init_sockets

app = Flask(__name__)
app.config["SECRET_KEY"] = "prod-secret"
app.config["JWT_SECRET_KEY"] = "jwt-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)
JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(admin)

init_sockets(app)

if __name__ == "__main__":
    socketio.run(app, debug=True)
