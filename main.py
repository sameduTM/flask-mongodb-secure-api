from flask import Flask
from config import jwt
from api.user import user_bp
from views.index import index_bp
from db.connectDB import connect # noqa

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "a-string-secret-at-least-256-bits-long"
jwt.init_app(app)

# Register blueprint
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.debug = True
    app.run()
