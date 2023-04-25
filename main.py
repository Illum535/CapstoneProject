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

@app.route('/about')
def about():
    '''
    Returns the about page at path "/about"
    '''
    return render_template("about.html")


@app.route("/new_cca", methods = ['POST', 'GET'])
def add_cca():
    '''
    Returns the page at path '/new_cca' to add new cca to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/new_cca")
            
        return render_template('add.html', data = add_data(list(request.args)[0], type = 'cca', form_data = dict(request.form)))
    
    return render_template('add.html', data = add_data('', type = 'cca'))
    
@app.route("/new_act", methods = ['POST', 'GET'])
def add_act():
    '''
    Returns the page at path '/new_act' to add new activity to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/new_act")
            
        return render_template('add.html', data = add_data(list(request.args)[0], type = 'act', form_data = dict(request.form)))
    
    return render_template('add.html', data = add_data('', type = 'act'))

if __name__ == "__main__":
    app.run('0.0.0.0')