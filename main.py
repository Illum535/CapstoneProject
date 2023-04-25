# Index page (showing available actions)
# Other pages (as needed)
# Login page (not implemented for now)
# Profile page (not implemented for now)
# Admin page (not implemented for now)
# Form pages (see below)

#Functions
# ADD, VIEW and EDIT Cca

from flask import Flask, render_template, request, redirect
from frontend import *

app = Flask(__name__)

@app.route('/')
def index():
    '''
    Returns the index page at path '/'
    '''
    return render_template("index.html")


@app.route("/add_cca", methods = ['POST', 'GET'])
def add_cca():
    '''
    Returns the page at path '/new_cca' to add new cca to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/new_cca")
            
        return render_template('add.html', data = add_data(list(request.args)[0], type = 'cca', form_data = dict(request.form)))
    
    return render_template('add.html', data = add_data('', type = 'cca'))
    
@app.route("/add_act", methods = ['POST', 'GET'])
def add_act():
    '''
    Returns the page at path '/new_act' to add new activity to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/new_act")
            
        return render_template('add.html', data = add_data(list(request.args)[0], type = 'act', form_data = dict(request.form)))
    
    return render_template('add.html', data = add_data('', type = 'act'))


@app.route('/view_class')
def view_class():
    '''
    Returns the page at path '/view_class' to show all classes
    '''
    return render_template('view.html', data = view_data('class'))

@app.route('/view_cca')
def view_cca():
    '''
    Returns the page at path '/view_cca' to show all ccas
    '''
    return render_template('view.html', data = view_data('cca'))

@app.route('/view_act')
def view_act():
    '''
    Returns the page at path '/view_act' to show all activities
    '''
    return render_template('view.html', data = view_data('act'))

if __name__ == "__main__":
    app.run('0.0.0.0')