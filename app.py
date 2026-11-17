from flask import Flask, render_template, request, redirect, url_for
from extensions import db, migrate

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///landscaping.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Import models after db is initialized
from models import Client


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    clients = Client.query.all()
    active_clients = Client.query.filter_by(status="Active").count()
    return render_template('dashboard.html', clients=clients, active_clients=active_clients)


@app.route('/add-client', methods=['POST'])
def add_client():
    client = Client(
        name=request.form['name'],
        phone=request.form.get('phone'),
        email=request.form.get('email'),
        address=request.form.get('address'),
        service=request.form.get('service'),
        status=request.form.get('status', 'Active'),
    )
    db.session.add(client)
    db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True)