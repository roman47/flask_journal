from flask import (Flask, g, render_template, flash, redirect,
                   url_for, abort)
from flask.ext.bcrypt import check_password_hash

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/')
@app.route('/index')
@app.route('/entries')
def index():
    entries = models.Entry.select().limit(100)
    return render_template('index.html', entries=entries)


@app.route('/new', methods=('GET', 'POST'))
@app.route('/entry', methods=('GET', 'POST'))
def new():
    form = forms.NewForm()
    if form.validate_on_submit():
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_you_learned=form.what_you_learned.data,
            resources_to_remember=form.resources_to_remember.data
        )
        flash("New Entry Created", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/detail/<title>')
@app.route('/details/<title>')
@app.route('/entries/<title>')
def detail(title):
    entries = models.Entry.select().where(models.Entry.title == title)
    if entries.count() == 0:
        flash("no entries", "error")
        abort(404)
    return render_template('detail.html', entries=entries)


@app.route('/delete/<title>')
@app.route('/entries/delete/<title>')
def delete(title):
    try:
        entry_delete = models.Entry.get(models.Entry.title == title)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Entry.get(models.Entry.title == title).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("you've deleted {}".format(title), 'success')
    return redirect(url_for('index'))


@app.route('/edit/<title>', methods=('GET', 'POST'))
@app.route('/entries/edit/<title>', methods=('GET', 'POST'))
@app.route('/entry/<title>', methods=('GET', 'POST'))
def edit(title):
    form = forms.NewForm()
    if form.validate_on_submit():
        # Yes, this is a delete then an insert, but I could not get the
        # Peewee update to work properly
        models.Entry.get(models.Entry.title == title).delete_instance()
        models.Entry.create_entry(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            what_you_learned=form.what_you_learned.data,
            resources_to_remember=form.resources_to_remember.data
        )
        flash("Entry Updated", "success")
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, title=title)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    models.initialize()
    try:
        models.Entry.create_entry(
            title='Aurora3',
            date='11/11/2018',
            time_spent=2,
            what_you_learned='nothing',
            resources_to_remember='Sci Fi'
        )

    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
