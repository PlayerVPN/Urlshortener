import os
from flask import Flask, request, redirect, render_template, jsonify
import secrets

app = Flask(__name__)

# Generate a secure secret key (For production, consider generating this externally)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))  # Fallback to a generated key

# A simple dictionary to store the URLs
url_mapping = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    if original_url not in url_mapping:
        short_id = secrets.token_urlsafe(6)  # Generate a short ID
        url_mapping[short_id] = original_url
    else:
        for short_id, url in url_mapping.items():
            if url == original_url:
                break
    return jsonify(short_url=f"http://localhost:5000/{short_id}")

@app.route('/<short_id>')
def redirect_to_url(short_id):
    original_url = url_mapping.get(short_id)
    if original_url:
        return redirect(original_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
