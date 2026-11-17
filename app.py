
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///landscaping.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize migrations
migrate = Migrate(app, db)

# Import models
from models import Client


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/test-db')
def test_db():
    new_client = Client(
        name="John Smith",
        phone="1234567890",
        address="123 Main Street",
        service="Lawn Mowing"
    )

    db.session.add(new_client)
    db.session.commit()

    return "Client successfully added!"

if __name__ == "__main__":
    app.run(debug=True)
