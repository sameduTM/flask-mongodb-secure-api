import os
from api.user import user_bp
from config import jwt
from db.connectDB import connect  # noqa
from dotenv import load_dotenv
from flask import Flask
from views.index import index_bp

app = Flask(__name__)

load_dotenv()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')
jwt.init_app(app)

# Register blueprint
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
