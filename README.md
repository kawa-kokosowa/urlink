# urlink

Simple-as-possible non-social bookmark service, including live search
and elegant frontend.

[See urlink in action!](http://urlink.link)

## The tools

  * `flask`, `flask_user`, `flask_login`, `flask_sqlalchemy`
  * Bootstrap
  * jQuery

Optionally: Heroku.

## Work in progress

Please forgive me; this is super sloppy and undocumented, but I just
finished the live bookmark filtering, so I wanna at least start the repo.

## Quickstart

Create `~/.urlink` or the like, it should look like:

```
#!/bin/sh
export MAIL_USERNAME="example@gmail.com"
export MAIL_PASSWORD="lololol"
export SECRET_KEY="wwowowowowowowoeijfeoaijf"
```

Finally, setup and run local development server:

```
$ . ~/.urlink
$ pip install -r requirements.txt
$ gunicorn app:app
```

## Heroku

### Environmental Variables

  * `SECRET_KEY` (you must override)
  * `SQLALCHEMY_DATABASE_URI` (optional; defaults to sqlite)
  * `MAIL_USERNAME` (you always need to set this!)
  * `MAIL_PASSWORD` (you always need to set this!)
  * `MAIL_DEFAULT_SENDER` (don't set if you're using gmail)
  * `MAIL_SERVER` (don't set if you're using gmail)
  * `MAIL_PORT` (don't set if you're using gmail)
  * `MAIL_USE_SSL` (don't set if you're using gmail)
  * `MAIL_USE_TLS` (don't set if you're using gmail)
