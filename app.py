from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load Firebase credentials from environment variables
cred = credentials.Certificate({
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT")
})

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Route to display posts
@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

# Route to add a post
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    content = request.form['content']
    add_post(title, content)
    return redirect(url_for('index'))

# Function to get posts from Firestore
def get_posts():
    posts_ref = db.collection('posts')
    docs = posts_ref.stream()
    posts = [{'title': doc.to_dict()['title'], 'content': doc.to_dict()['content']} for doc in docs]
    return posts

# Function to add a post to Firestore
def add_post(title, content):
    post = {'title': title, 'content': content}
    db.collection('posts').add(post)

if __name__ == '__main__':
    app.run(debug=True)
