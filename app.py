from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2083), nullable=False)
    shortened_url = db.Column(db.String(20), unique=True, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

def generate_shortened_url():
    length = 6
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(length))
        if not URL.query.filter_by(shortened_url=short_url).first():
            return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        if original_url:
            short_url = generate_shortened_url()
            new_url = URL(original_url=original_url, shortened_url=short_url)
            db.session.add(new_url)
            db.session.commit()
            flash(f'Shortened URL created: {request.host_url}{short_url}', 'success')
        else:
            flash('Please enter a valid URL', 'danger')
    return render_template('index.html')

@app.route('/<shortened_url>')
def redirect_to_url(shortened_url):
    url_entry = URL.query.filter_by(shortened_url=shortened_url).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
