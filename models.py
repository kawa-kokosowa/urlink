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
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))  # should never be null :o
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    url = db.Column(db.String())  # should neve rbe null :o
    description = db.Column(db.String(140))
    title = db.Column(db.String())
    content_type = db.Column(db.String())  # isn't this a certain number of bytes max? should b required
    user = db.relationship('User', foreign_keys='Url.user_id', lazy='subquery')

    def __init__(self, user_id, url, description, content_type=None, title=None):
        self.user_id = user_id
        self.url = url
        self.description = description
        # these are derived from util.fetch_searchable_data()
        self.title = title
        self.content_type = content_type

    def __repr__(self):
        return '<URL #%s %s (%s)>' % (self.id, self.title, self.url)

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
            'title': self.title,
            'content_type': self.content_type,
        }
        return data_to_return
