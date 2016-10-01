# builtin
import datetime

# 3rd party
import flask_sqlalchemy
import flask_user


db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model, flask_user.UserMixin):
    """Generic User data model for flask_user as seen
    in their documentation.

    http://pythonhosted.org/Flask-User/basic_app.html

    """

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')


class Url(db.Model):
    """A URL belonging to a user, accompanied by a description
    of 140 characters or less.

    Belongs to /urls/x

    """

    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    url = db.Column(db.String())
    description = db.Column(db.String(140))
    user = db.relationship('User', foreign_keys='Url.user_id', lazy='subquery')

    def __init__(self, user_id, url, description):
        self.user_id = user_id
        self.url = url
        self.description = description

    def __repr__(self):
        return '<URL #%s (%s)>' % (self.id, self.url)

    def to_dict(self):
        """Create a dictionary representing this URL.

        Returns:
            dict: contains the id, url, and description of
                this URL.

        """

        data_to_return = {
            'id': self.id,
            # TODO:
            # 'created': self.created,
            'url': self.url,
            'description': self.description,
        }
        return data_to_return
