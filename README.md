# urlink

Simple-as-possible non-social bookmark service, including live search
and elegant frontend.

[Use urlink LIVE on urlink.link!](http://urlink.link)

I've also included a Chrome Extension for urlink (`/chrome_extension`).

![urlink screen recording](https://github.com/lily-seabreeze/urlink/blob/master/demo.gif)

This is an early work in progress (call it "alpha").

## The tools

  * `flask`, `flask_user`, `flask_login`, `flask_sqlalchemy`,
    `flask_migrate`
  * Bootstrap
  * jQuery

## Quickstart

[Set the required environmental variables](http://askubuntu.com/questions/58814/how-do-i-add-environment-variables):

```
MAIL_USERNAME="example@gmail.com"
MAIL_PASSWORD="lololol"
SECRET_KEY="wwowowowowowowoeijfeoaijf"
```

`pip install -r` either `requirements_no_postgres.txt` (or
`requirements_dev.txt` (if you wanna run tests). `requirements.txt`
is for Heroku (it includes `psycopg2). I personally use SQLite for
developing locally and tests.

Create the database with `python app.py db init` (`db migrate`,
`db upgrade`, and `db --help` are also available).

Finally run the server with `gunicorn app:app:`.

## Environmental Variables

  * `SECRET_KEY` (you must override)
  * `SQLALCHEMY_DATABASE_URI` (optional; defaults to sqlite)
  * `MAIL_USERNAME` (you always need to set this!)
  * `MAIL_PASSWORD` (you always need to set this!)
  * `MAIL_DEFAULT_SENDER` (don't set if you're using gmail)
  * `MAIL_SERVER` (don't set if you're using gmail)
  * `MAIL_PORT` (don't set if you're using gmail)
  * `MAIL_USE_SSL` (don't set if you're using gmail)
  * `MAIL_USE_TLS` (don't set if you're using gmail)
