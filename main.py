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
    if request.args:
        if not dict(request.form).values():
            return redirect("/add_student")
        if 'success' in request.args:
            result = coll['student'].add_record(dict(request.form))
            if result:
                return render_template('add_update.html', data = add_data('add', 'fail', type = 'student', form_data = dict(request.form)))
        
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'student', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'student'))

@app.route("/add_class", methods = ['POST', 'GET'])
def add_class():
    '''
    Returns the page at path '/add_class' to add new class to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/add_class")
        if 'success' in request.args:
            result = coll['class'].add_record(dict(request.form))
            if result:
                return render_template('add_update.html', data = add_data('add', 'fail', type = 'class', form_data = dict(request.form)))
        
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'class', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'class'))

@app.route("/add_subject", methods = ['POST', 'GET'])
def add_subject():
    '''
    Returns the page at path '/add_subject' to add new subject to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/add_subject")
        if 'success' in request.args:
            result = coll['subject'].add_record(dict(request.form))
            if result:
                return render_template('add_update.html', data = add_data('add', 'fail', type = 'subject', form_data = dict(request.form)))
        
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'subject', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'subject'))

@app.route("/add_cca", methods = ['POST', 'GET'])
def add_cca():
    '''
    Returns the page at path '/new_cca' to add new cca to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/add_cca")
        if 'success' in request.args:
            result = coll['cca'].add_record(dict(request.form))
            if result:
                return render_template('add_update.html', data = add_data('add', 'fail', type = 'cca', form_data = dict(request.form)))
        
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'cca', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'cca'))
    
@app.route("/add_activity", methods = ['POST', 'GET'])
def add_act():
    '''
    Returns the page at path '/new_act' to add new activity to the database
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/add_activity")
        if 'success' in request.args:
            result = coll['activity'].add_record(dict(request.form))
            if result:
                return render_template('add_update.html', data = add_data('add', 'fail', type = 'activity', form_data = dict(request.form)))
            
        return render_template('add_update.html', data = add_data('add', list(request.args)[0], type = 'activity', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('add', '', type = 'activity'))



@app.route('/view_student', methods = ['GET', 'POST'])
def view_student():
    '''
    Returns the page at path '/view_student' to show all students
    '''
    if request.args:
        if 'edit' in request.args:
            data = get_update_data('view', dict(request.form))
            coll['student'].edit_record(data[0], data[1])
            return redirect('/view_student')
            
        return render_template('view.html', data = view_data('student', list(request.args)[0], list(request.args)[1]))
        
    return render_template('view.html', data = view_data('student'))

@app.route('/view_class', methods = ['GET', 'POST'])
def view_class():
    '''
    Returns the page at path '/view_class' to show all classes
    '''
    if request.args:
        if 'edit' in request.args:
            data = get_update_data('view', dict(request.form))
            coll['class'].edit_record(data[0], data[1])
            return redirect('/view_class')
        
        return render_template('view.html', data = view_data('class', list(request.args)[0], list(request.args)[1]))
        
    return render_template('view.html', data = view_data('class'))

@app.route('/view_cca', methods = ['GET', 'POST'])
def view_cca():
    '''
    Returns the page at path '/view_cca' to show all ccas
    '''
    if request.args:
        if 'edit' in request.args:
            data = get_update_data('view', dict(request.form))
            print(data)
            coll['cca'].edit_record(data[0], data[1])
            return redirect('/view_cca')
            
        return render_template('view.html', data = view_data('cca', list(request.args)[0], list(request.args)[1]))
        
    return render_template('view.html', data = view_data('cca'))

@app.route('/view_activity', methods = ['GET', 'POST'])
def view_act():
    '''
    Returns the page at path '/view_activity' to show all activities
    '''
    if request.args:
        if 'edit' in request.args:
            data = get_update_data('view', dict(request.form))
            coll['activity'].edit_record(data[0], data[1])
            return redirect('/view_activity')
            
        return render_template('view.html', data = view_data('activity', list(request.args)[0], list(request.args)[1]))
        
    return render_template('view.html', data = view_data('activity'))

@app.route('/view_subject', methods = ['GET', 'POST'])
def view_subject():
    '''
    Returns the page at path '/view_subject' to show all subjects
    '''
    if request.args:
        if 'edit' in request.args:
            data = get_update_data('view', dict(request.form))
            coll['subject'].edit_record(data[0], data[1])
            return redirect('/view_subject')
            
        return render_template('view.html', data = view_data('subject', list(request.args)[0], list(request.args)[1]))
        
    return render_template('view.html', data = view_data('subject'))



@app.route('/update_student', methods = ['POST', 'GET'])
def update_student():
    '''
    Returns the page at path '/update_student' to update student data
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_student")
        if 'success' in request.args:
            data = get_update_data('update', dict(request.form))
            result = coll['student'].edit_record(data[0], data[1])
            if result:
                return render_template('add_update.html', data = add_data('update', 'fail', type = 'student', form_data = dict(request.form)))
        
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'student', form_data = dict(request.form)))

    return render_template('add_update.html', data = add_data('update', '', type = 'student'))
        
@app.route('/update_class', methods = ['POST', 'GET'])
def update_class():
    '''
    Returns the page at path '/update_class' to update class data
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_class")
        if 'success' in request.args:
            data = get_update_data('update', dict(request.form))
            result = coll['class'].edit_record(data[0], data[1])
            if result:
                return render_template('add_update.html', data = add_data('update', 'fail', type = 'class', form_data = dict(request.form)))

        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'class', form_data = dict(request.form)))

    return render_template('add_update.html', data = add_data('update', '', type = 'class'))
        
@app.route('/update_cca', methods = ['POST', 'GET'])
def update_cca():
    '''
    Returns the page at path '/update_cca' to update cca data
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_cca")
        if 'success' in request.args:
            data = get_update_data('update', dict(request.form))
            result = coll['cca'].edit_record(data[0], data[1])
            if result:
                return render_template('add_update.html', data = add_data('update', 'fail', type = 'cca', form_data = dict(request.form)))
        
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'cca', form_data = dict(request.form)))

    return render_template('add_update.html', data = add_data('update', '', type = 'cca'))
        
@app.route('/update_activity', methods = ['POST', 'GET'])
def update_activity():
    '''
    Returns the page at path '/update_activity' to update activity data
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_activity")
        if 'success' in request.args:
            data = get_update_data('update', dict(request.form))
            result = coll['activity'].edit_record(data[0], data[1])
            if result:
                return render_template('add_update.html', data = add_data('update', 'fail', type = 'activity', form_data = dict(request.form)))
            
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'activity', form_data = dict(request.form)))

    return render_template('add_update.html', data = add_data('update', '', type = 'activity'))

@app.route('/update_subject', methods = ['POST', 'GET'])
def update_subject():
    '''
    Returns the page at path '/update_subject' to update subject data
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_activity")
        if 'success' in request.args:
            data = get_update_data('update', dict(request.form))
            result = coll['subject'].edit_record(data[0], data[1])
            if result:
                return render_template('add_update.html', data = add_data('update', 'fail', type = 'subject', form_data = dict(request.form)))
            
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'subject', form_data = dict(request.form)))

    return render_template('add_update.html', data = add_data('update', '', type = 'subject'))
        
@app.route('/update_student_cca', methods = ['POST', 'GET'])
def update_studentcca():
    '''
    Returns the page at path '/update_student_cca' to update student cca membership
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_student_cca")
            
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'student_cca', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('update', '', type = 'student_cca'))

@app.route('/update_student_activity', methods = ['POST', 'GET'])
def update_act():
    '''
    Returns the page at path '/update_student_activity' to update student activity participation
    '''
    if request.args:
        if not dict(request.form).values():
            return redirect("/update_student_activity")
            
        return render_template('add_update.html', data = add_data('update', list(request.args)[0], type = 'student_activity', form_data = dict(request.form)))
    
    return render_template('add_update.html', data = add_data('update', '', type = 'student_activity'))


if __name__ == "__main__":
   app.run('0.0.0.0')

