"""Really sloppy configuration that will be overhauled
to include environment-specific configs (develop, test, production).

Mostly due to a Heroku headache.

"""

import os


DEBUG = False
TESTING = False

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv(
    'SQLALCHEMY_DATABASE_URI',  # if not this... then below
    os.getenv('DATABASE_URL', 'sqlite:////tmp/debug.db'),  # heroku
)

# flask-user
USER_ENABLE_USERNAME = False
USER_ENABLE_CHANGE_USERNAME = False
# flask-mail settings for flask-user
# (email confirmation, password reset)
# setup for gmail by default
# NOTE, FIXME, TODO: the only reason this is false
# is because gmail isn't allowing me use their smtp
# anymore!
USER_ENABLE_CONFIRM_EMAIL = False
# this email stuff is all moot because of above note
# will renable once have smtp service
"""
MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # example@gmail.com
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = '"urlink" <noreply@urlink.link>'
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USE_SSL = True
MAIL_USE_TLS = True
"""
# this is used by email:
USER_APP_NAME = 'urlink'
