"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """Show info about user in a nice packaged way, rather than just <User><User>"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, unique=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False, unique=False)

    user = db.relationship('User', backref='posts')


class PostTag(db.Model):
    """Join table for tag on a post"""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    posts = db.relationship('Post', secondary="post_tags", backref="tags")

    def __repr__(self):
        """Show info about user in a nice packaged way, rather than just <User><User>"""

        t = self
        return f"<Tser {t.id} {t.name}>"
