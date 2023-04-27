# Index page (showing available actions)
# Other pages (as needed)
# Login page (not implemented for now)
# Profile page (not implemented for now)
# Admin page (not implemented for now)
# Form pages (see below)

#Functions
# ADD, VIEW and EDIT Cca
# NOTE REMEMBER TO UPDATE ADD AND UPDATE FORMS WITH DATABASE FUNCTIONS #


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
            
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'cca', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'cca'))
    
@app.route("/add_activity", methods = ['POST', 'GET'])
def add_act():
    '''
    Returns the page at path '/new_act' to add new activity to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/new_activity")
            
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'activity', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'activity'))



@app.route('/view_class', methods = ['GET'])
def view_class():
    '''
    Returns the page at path '/view_class' to show all classes
    '''
    if request.args:
        return render_template('view.html', data = view_data('class', list(request.args)[0]))
        
    return render_template('view.html', data = view_data('class'))

@app.route('/view_cca')
def view_cca():
    '''
    Returns the page at path '/view_cca' to show all ccas
    '''
    if request.args:
        return render_template('view.html', data = view_data('cca', list(request.args)[0]))
        
    return render_template('view.html', data = view_data('cca'))

@app.route('/view_activity')
def view_act():
    '''
    Returns the page at path '/view_activity' to show all activities
    '''
    if request.args:
        return render_template('view.html', data = view_data('activity', list(request.args)[0]))
        
    return render_template('view.html', data = view_data('activity'))



@app.route('/update_cca', methods = ['POST', 'GET'])
def update_cca():
    '''
    Returns the page at path '/update_cca' to update cca records
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_cca")
            
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'cca', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('update', '', type = 'cca'))

@app.route('/update_activity', methods = ['POST', 'GET'])
def update_act():
    '''
    Returns the page at path '/update_activity' to update activity records
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_activity")
            
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'activity', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('update', '', type = 'activity'))


if __name__ == "__main__":
   app.run('0.0.0.0')


