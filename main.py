# Index page (showing available actions)
# Other pages (as needed)
# Login page (not implemented for now)
# Profile page (not implemented for now)
# Admin page (not implemented for now)
# Form pages (see below)

#Functions
# ADD, VIEW and EDIT Cca
# NOTE REMEMBER TO UPDATE ADD AND UPDATE FORMS WITH DATABASE FUNCTIONS #


from flask import Flask, render_template, request
from frontend import *
from storage import *

app = Flask(__name__)

@app.errorhandler(404)
def error404(e):
    '''
    Returns the error page
    '''
    return render_template('error.html', error = '404', msg = 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.')

@app.errorhandler(500)
def error500(e):
    '''
    Returns the error page
    '''
    return render_template('error.html', error = '500', msg = 'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.')


@app.route('/')
def index():
    '''
    Returns the index page at path '/'
    '''
    return render_template("index.html")


@app.route("/add_student", methods = ['POST', 'GET'])
def add_student():
    '''
    Returns the page at path '/add_student' to add new student to the database
    '''
    return add_update('add', 'student', request)

@app.route("/add_class", methods = ['POST', 'GET'])
def add_class():
    '''
    Returns the page at path '/add_class' to add new class to the database
    '''
    return add_update('add', 'class', request)

@app.route("/add_subject", methods = ['POST', 'GET'])
def add_subject():
    '''
    Returns the page at path '/add_subject' to add new subject to the database
    '''
    return add_update('add', 'subject', request)

@app.route("/add_cca", methods = ['POST', 'GET'])
def add_cca():
    '''
    Returns the page at path '/add_cca' to add new cca to the database
    '''
    return add_update('add', 'cca', request)
    
@app.route("/add_activity", methods = ['POST', 'GET'])
def add_act():
    '''
    Returns the page at path '/add_activity' to add new activity to the database
    '''
    return add_update('add', 'activity', request)

@app.route("/add_student_class", methods = ['POST', 'GET'])
def add_student_class():
    '''
    Returns the page at path '/add_student_class to an existing student to an existing class
    '''
    return add_update('add', 'student_class', request)

@app.route("/add_student_cca", methods = ['POST', 'GET'])
def add_student_cca():
    '''
    Returns the page at path '/add_student_cca' to an existing student to an existing cca
    '''
    return add_update('add', 'student_cca', request)
    
@app.route("/add_student_activity", methods = ['POST', 'GET'])
def add_student_activity():
    '''
    Returns the page at path '/add_student_activity' to add an existing student to an existing activity
    '''
    return add_update('add', 'student_activity', request)


@app.route('/view_student', methods = ['GET', 'POST'])
def view_student():
    '''
    Returns the page at path '/view_student' to show all students
    '''
    return view('student', request)

@app.route('/view_class', methods = ['GET', 'POST'])
def view_class():
    '''
    Returns the page at path '/view_class' to show all classes
    '''
    return view('class', request)

@app.route('/view_cca', methods = ['GET', 'POST'])
def view_cca():
    '''
    Returns the page at path '/view_cca' to show all ccas
    '''
    return view('cca', request)

@app.route('/view_activity', methods = ['GET', 'POST'])
def view_act():
    '''
    Returns the page at path '/view_activity' to show all activities
    '''
    return view('activity', request)

@app.route('/view_subject', methods = ['GET', 'POST'])
def view_subject():
    '''
    Returns the page at path '/view_subject' to show all subjects
    '''
    return view('subject', request)



@app.route('/update_student', methods = ['POST', 'GET'])
def update_student():
    '''
    Returns the page at path '/update_student' to update student data
    '''
    return add_update('update', 'student', request)
        
@app.route('/update_class', methods = ['POST', 'GET'])
def update_class():
    '''
    Returns the page at path '/update_class' to update class data
    '''
    return add_update('update', 'class', request)
        
@app.route('/update_cca', methods = ['POST', 'GET'])
def update_cca():
    '''
    Returns the page at path '/update_cca' to update cca data
    '''
    return add_update('update', 'cca', request)
        
@app.route('/update_activity', methods = ['POST', 'GET'])
def update_activity():
    '''
    Returns the page at path '/update_activity' to update activity data
    '''
    return add_update('update', 'activity', request)

@app.route('/update_subject', methods = ['POST', 'GET'])
def update_subject():
    '''
    Returns the page at path '/update_subject' to update subject data
    '''
    return add_update('update', 'subject', request)
        
@app.route('/update_student_cca', methods = ['POST', 'GET'])
def update_studentcca():
    '''
    Returns the page at path '/update_student_cca' to update student cca membership
    '''
    return add_update('update', 'student_cca', request)

@app.route('/update_student_activity', methods = ['POST', 'GET'])
def update_act():
    '''
    Returns the page at path '/update_student_activity' to update student activity participation
    '''
    return add_update('update', 'student_activity', request)


if __name__ == "__main__":
   app.run('0.0.0.0')

