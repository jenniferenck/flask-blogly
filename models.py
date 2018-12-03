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

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    image_url = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """Show info about user in a nice packaged way, rather than just <User><User>"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    # def delete(self):
    #     """delete user"""
    #     User.query.filter(user.id==self).delete()

