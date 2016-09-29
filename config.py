"""Really sloppy configuration that will be overhauled
to include environment-specific configs (develop, test, production).

Mostly due to a Heroku headache.

"""

DEBUG = False
TESTING = False

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:////tmp/debug.db'
)

# flask-mail settings for flask-user
# (email confirmation, password reset)
# setup for gmail by default
MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # example@gmail.com
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = '"urlink" <noreply@urlink.link>'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
# this is used by email:
USER_APP_NAME = 'urlink'
