from flask import Flask, render_template, \
    request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Blog Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    # Unique ID for each post
    title = db.Column(db.String(100), nullable=False)  
    # Post title
    content = db.Column(db.Text, nullable=False)  
    # Post content

# Create the database tables
with app.app_context():
    db.create_all()

# ----------------------
# Routes / CRUD Operations
# ----------------------

# Home page – List all posts
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# Create a new post
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# Edit an existing post
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

# Delete a post
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))
