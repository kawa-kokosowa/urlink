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
$ cp config.py-SAMPLE config.py
$ vim config.py
$ gunicorn app:app
```
