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

Create `~/.urlink` and run `. ~/.urlink`, its contents should look like:

```
#!/bin/sh
export MAIL_USERNAME="example@gmail.com"
export MAIL_PASSWORD="lololol"
export SECRET_KEY="wwowowowowowowoeijfeoaijf"
```

Install either `requirements_no_postgres.txt` or `requirements.txt`,
depending on if you want `psycopg2` (I use sqlite locally, but
PostgreSQL on Heroku).

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
