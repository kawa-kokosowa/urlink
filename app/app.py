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
config_path = os.path.dirname(os.path.abspath(__file__))
app.config.from_pyfile(os.path.join(config_path, "config.py"))
models.db.init_app(app)
# flask user
mail = flask_mail.Mail(app)
db_adapter = flask_user.SQLAlchemyAdapter(models.db, models.User)
user_manager = flask_user.UserManager(db_adapter, app)


class AddUrlForm(wtforms.Form):
    url = wtforms.StringField(
        'url',
        [wtforms.validators.URL(require_tld=True),],
        render_kw={"placeholder": "URL/Link", "class": "form-control"},
    )
    description = wtforms.StringField(
        'description',
        [wtforms.validators.Length(max=140),],
        render_kw={"placeholder": "Description/about URL"},
    )


class SearchForm(wtforms.Form):
    autocomp = wtforms.TextField('autocomp', id='autocomplete')


# The Home page is accessible to anyone
@app.route('/')
def home_page():
    search_form = SearchForm(flask.request.form)

    if flask_login.current_user.is_authenticated:
        urls = models.Url.query.filter_by(
            user=flask_login.current_user
        ).all()
    else:
        urls = None

    return flask.render_template(
        "home.html",
        search_form=search_form,
        urls=urls
    )


@app.route('/urls/<int:url_id>')
@flask_user.login_required
def view_url(url_id):
    search_form = SearchForm(flask.request.form)
    url = models.Url.query.get(url_id)

    if url.user_id == flask_login.current_user.id:
        return flask.render_template(
            "view_url.html",
            search_form=search_form,
            url=url
        )
    else:
        pass
        # should be flask abort


@app.route('/autocomplete', methods=['GET'])
@flask_user.login_required
def autocomplete():
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
    search_form = SearchForm(flask.request.form)

    if flask.request.method == 'POST':

        if len(flask.request.form['description']) > 140:
            flask.abort(400)

        new_url = models.Url(
            user_id=flask_login.current_user.id,
            url=flask.request.form['url'],
            description=flask.request.form['description'],
        )
        models.db.session.add(new_url)
        models.db.session.commit()
        return flask.redirect(flask.url_for('view_url', url_id=new_url.id))
    else:
        form = AddUrlForm(flask.request.form)
        return flask.render_template("add_url.html", search_form=search_form, form=form)


# Start development web server
if __name__=='__main__':

    with app.app_context():
        models.db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)
