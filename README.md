# urlink

Simple-as-possible non-social bookmark service, including live search
and elegant frontend.

## The tools

  * `flask`, `flask_user`, `flask_login`, `flask_sqlalchemy`
  * Bootstrap
  * jQuery

Optionally: Heroku.

## Work in progress

Please forgive me; this is super sloppy and undocumented, but I just
finished the live bookmark filtering, so I wanna at least start the repo.

## Quickstart

```
$ pip install -r requirements.txt
$ export URLINK_SETTINGS=/path/to/config-overrides.cfg
$ gunicorn app:app
```

## Heroku

### Environmental Variables

Be sure to override the `SECRET_KEY`, you also may want to change the
`SQLALCHEMY_DATABASE_URI`. The rest of the environmental variables you
should be concerned with are the variables for mailer/sender, which is
setup, by default, for Gmail:

  * `MAIL_USERNAME`
  * `MAIL_PASSWORD`
  * `MAIL_DEFAULT_SENDER`
  * `MAIL_SERVER`
  * `MAIL_PORT`
  * `MAIL_USE_SSL` = True
  * `MAIL_USE_TLS` = False
