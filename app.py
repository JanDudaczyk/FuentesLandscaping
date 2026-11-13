from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
 return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
 return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)