"""urlink Flask App

"""

# builtin
import os

# local
import models

# 3rd party/pip
import flask
import flask_mail
import flask_user
import flask_login  # depend of flask_user
import wtforms


# flask app setup
app = flask.Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
models.db.init_app(app)
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


@app.route('/')
def home_page():
    """Rendered Jinja/HTML page for searching/filtering bookmarks.

    Form on this page can use regular form submission, but
    this page also includes jQuery used to live-search
    with JSON, i.e., `/autocomplete` endpoint.

    See Also:
        autocomplete()

    """


    # only logged-in users have URLs to see and search!
    if flask_login.current_user.is_authenticated:
        # this form doesn't need validating
        search_form = SearchForm(flask.request.form)
        urls = models.Url.query.filter_by(
            user=flask_login.current_user
        ).all()
    else:
        urls = None
        search_form = None

    return flask.render_template(
        "home.html",
        search_form=search_form,
        urls=urls
    )


@app.route('/urls/<int:url_id>')
@flask_user.login_required
def view_url(url_id):
    """A unique address to view a URL post the
    current user owns.

    If the current user's ID matches the user ID (the owner)
    of the URL being requested by `url_id`, said link is
    presented/rendered, otherwise, a 403 Forbidden is returned.

    """

    url = models.Url.query.get(url_id)

    if url.user_id == flask_login.current_user.id:
        return flask.render_template(
            "view_url.html",
            url=url
        )
    else:
        flask.abort(403)


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

    search = flask.request.args.get('term')
    search_results = models.Url.query.filter(
        models.Url.user_id == flask_login.current_user.id,
        models.Url.description.ilike("%" + search + "%"),
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
        new_url = models.Url(
            user_id=flask_login.current_user.id,
            url=flask.request.form['url'],
            description=flask.request.form['description'],
        )
        models.db.session.add(new_url)
        models.db.session.commit()
        return flask.redirect(flask.url_for('view_url', url_id=new_url.id))
    else:
        return flask.render_template("add_url.html", form=form)


# Create the database
if __name__=='__main__':

    with app.app_context():
        models.db.create_all()
