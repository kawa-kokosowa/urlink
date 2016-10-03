"""urlink Flask App

"""

# builtin
import os

# local
import models
import config
import urlhelper

# 3rd party/pip
import flask
import flask_mail
import flask_user
import flask_login
import flask_script
import flask_migrate
import sqlalchemy
import wtforms


# flask app setup
app = flask.Flask(__name__)
app.config.from_object(config)
migrate = flask_migrate.Migrate(app, models.db)

manager = flask_migrate.Manager(app)
manager.add_command('db', flask_migrate.MigrateCommand)

models.db.init_app(app)  # ???
# flask user
mail = flask_mail.Mail(app)
db_adapter = flask_user.SQLAlchemyAdapter(models.db, models.User)
user_manager = flask_user.UserManager(db_adapter, app)


class AddUrlForm(wtforms.Form):
    """Validation and fields for the form/page which allows a user
    to save/add a URL/link.

    """

    url = wtforms.StringField(
        'url',
        [wtforms.validators.URL(require_tld=True),],
        render_kw={
            "placeholder": "URL/Link",
            "class": "form-control input-lg",
            "id": "url",
            "autofocus": True
        },
    )
    description = wtforms.TextAreaField(
        'description',
        [wtforms.validators.Length(max=140),],
        render_kw={
            "placeholder": "Description/about URL",
            "class": "form-control input-lg",
            "id": "description",
            "maxlength": 140,
        },
    )


class SearchForm(wtforms.Form):
    """For live searching/filtering the bookmarks.

    Uses the /autocomplete endpoint (see: autocomplete()).

    """

    autocomp = wtforms.TextField('autocomp', id='autocomplete')


# TODO: newest first.
@app.route('/')
def home_page():
    """Rendered Jinja/HTML page for live-searching bookmarks.

    Form on this page can use normal form submission, however,
    this page includes jQuery which implements the live-searching
    feature, it updates the page with values from `/autocomplete`,
    i.e., autocomplete().

    If the user isn't logged in, they are redirected to the about page.

    """

    if flask_login.current_user.is_authenticated:
        # this form doesn't need validating
        search_form = SearchForm(flask.request.form)
        urls = models.Url.query.filter_by(
            user=flask_login.current_user
        ).all()
        return flask.render_template(
            "ur_links.html",
            search_form=search_form,
            urls=urls
        )
    else:
        return flask.render_template("landing.html")


@app.route('/autocomplete', methods=['GET'])
@flask_user.login_required
def autocomplete():
    """Provides JSON response of URLs where
    the search term is in the description.

    Query for URLs owned by the current user, whose descriptions
    in the database contain `term`.

    Returns:
        json: A list of dictionaries describing each
            matching URL.

    """

    search_term = flask.request.args.get('term')
    search_type = flask.request.args.get('type')

    if search_type:
        search_results = models.Url.query.filter(
            models.Url.user_id == flask_login.current_user.id,
            sqlalchemy.or_(
                models.Url.url.ilike("%" + search_term + "%"),
                models.Url.description.ilike("%" + search_term + "%"),
            ),
            models.Url.content_type == search_type,
        )
    else:
        search_results = models.Url.query.filter(
            models.Url.user_id == flask_login.current_user.id,
            sqlalchemy.or_(
                models.Url.url.ilike("%" + search_term + "%"),
                models.Url.description.ilike("%" + search_term + "%"),
            ),
        )

    urls = [url.to_dict() for url in search_results]
    return flask.jsonify(urls)


@app.route('/urls/add', methods=['POST', 'GET'])
@flask_user.login_required
def add_url():
    """Process and provide the form for adding a new URL to the
    current user's urls.

    """

    form = AddUrlForm(flask.request.form)

    # Either process the form from POST or show the form.
    if flask.request.method == 'POST' and form.validate():
        # There's no reason to prevent the URL from being created
        # using the POST'd information. Create and show the URL.
        url = flask.request.form['url']
        searchable_data = urlhelper.fetch_searchable_data(url)
        new_url = models.Url(
            user_id=flask_login.current_user.id,
            url=url,
            description=flask.request.form['description'],
            **searchable_data,
        )
        models.db.session.add(new_url)
        models.db.session.commit()
        return flask.redirect(flask.url_for('home_page'))
    else:
        return flask.render_template("add_url.html", form=form)


# Create the database
if __name__=='__main__':
    manager.run()
