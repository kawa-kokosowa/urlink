# urlink

Simple-as-possible non-social bookmark service, including live search
and elegant frontend.

[Use urlink LIVE on urlink.link!](http://urlink.link)

I've also included a Chrome Extension for urlink (`/chrome_extension`).

![urlink screen recording](https://github.com/lily-seabreeze/urlink/blob/master/demo.gif)

This is an early work in progress (call it "alpha").

## The tools

  * Python 3
  * `flask`, `flask_user`, `flask_login`, `flask_sqlalchemy`,
    `flask_migrate`
  * Bootstrap
  * jQuery

## Quickstart

```
mkvirtualenv urlink -p python3
pip install -r requirements_no_postgres.txt
export SECRET_KEY="asfdsfasdfasdffsdsdfa"
python app.py db init
python app.py db upgrade
gunicorn app:app
```
## Environmental Variables

This application is configured through environmental variables.

Required (everything else is optional):

  * `SECRET_KEY` (you must override)
  * `SQLALCHEMY_DATABASE_URI` (optional; defaults to sqlite)

You will want to look at `flask-mail`  if you want to provide registration
email verification, as seen below:

  * `MAIL_USERNAME` (you always need to set this!)
  * `MAIL_PASSWORD` (you always need to set this!)
  * `MAIL_DEFAULT_SENDER` (don't set if you're using gmail)
  * `MAIL_SERVER` (don't set if you're using gmail)
  * `MAIL_PORT` (don't set if you're using gmail)
  * `MAIL_USE_SSL` (don't set if you're using gmail)
  * `MAIL_USE_TLS` (don't set if you're using gmail)

