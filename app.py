from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db, migrate

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = "change-this-to-a-long-random-string"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///landscaping.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)

# Import models after db is initialized
from models import Client, User


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


# Public pages

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        error = "Invalid username or password."
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# Admin pages (login required)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    clients = Client.query.all()
    active_clients = Client.query.filter_by(status="Active").count()
    return render_template('dashboard.html', clients=clients, active_clients=active_clients)


@app.route('/add-client', methods=['POST'])
@login_required
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


# Command: flask create-admin
@app.cli.command("create-admin")
def create_admin():
    """Create the admin account (Admin / Admin123)."""
    if User.query.filter_by(username="Admin").first():
        print("Admin account already exists.")
        return
    user = User(username="Admin")
    user.set_password("Admin123")
    db.session.add(user)
    db.session.commit()
    print("Admin account created.")


if __name__ == "__main__":
    app.run(debug=True)