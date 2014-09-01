import os
import sys
from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form, widgets


from conselect import get_contests, create_table

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_pyfile('config.py')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/select', methods=['GET', 'POST'])
def select_contests():
    if request.method == 'GET':
        act = get_contests('actual-olympiads')
        psd = get_contests('ended-olympiads')
        return render_template('select.html', actual=act, passed=psd)
    else:
        form_data = request.form.getlist("contest")
        session['selected'] = form_data
        return redirect(url_for('monitor'))
    

@app.route('/monitor')
def monitor():
    sel = '<p>No contests selected<p>'
    if 'selected' in session:
        sel = create_table(session['selected'])
    else:
        return redirect(url_for('select_contests'))
    return render_template('monitor.html', selected=sel)
