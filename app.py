"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
    # import pdb; pdb.set_trace()
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

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route("/<int:user_id>")
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

    user = User.query.get_or_404(user_id)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name 
    if image_url:
        user.image_url = image_url 
   
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect('/users')



