"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/")
def redirect_to_users():
    """Redirect user to list_users."""

    return redirect('/users')


@app.route("/users")
def list_users():
    """show all users"""

    users = User.query.all()
    return render_template("list_users.html", users=users)


@app.route('/users/new')
def render_create_user_page():
    """show an add form for users"""

    return render_template("create_user.html")


@app.route('/users/new', methods=["POST"])
def add_user():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    new_user = User(
        first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show info about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_user_edit_form(user_id):
    """Process the edit form, returning the user to the /users page."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    # can add value in edit_user.html to remove this
    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def show_new_post_form(user_id):
    """Show form for adding a new post."""

    user = User.query.get_or_404(user_id)

    return render_template('new_post_form.html', user=user)


# in further study can add auto-date create
@app.route('/users/<int:user_id>/posts/', methods=["POST"])
def add_new_post(user_id):
    """Handle add form and add post to user detail page."""

    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(
        title=title, content=content, created_at='11-11-2011', user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post_details(post_id, user_id):

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post_details.html', post=post, user=user)


@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def show_edit_post_form(user_id, post_id):

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('edit_post.html', post=post, user=user)


@app.route('/users/<int:user_id>/posts/<int:post_id>', methods=['POST'])
def process_post_edit(user_id, post_id):

    title = request.form.get('title')
    content = request.form.get('content')

    post = Post.query.get_or_404(post_id)

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}/posts/{post_id}')


@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
