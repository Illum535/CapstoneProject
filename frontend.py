from storage import *
from flask import Flask, render_template, request, redirect

coll = { # Backend implementation, creating collections for the different tables bravo Dylan
    'activity': ActivityCollection(),
    'cca': CCACollection(),
    'class': ClassCollection(),
    'student': StudentCollection(),
    'subject': SubjectCollection(),
    'student_class': StudentClassCollection(),
    'student_cca': StudentCCACollection(),
    'student_activity': StudentActivityCollection(),
    'student_subject': StudentSubjectCollection(),
    'cca_activity': CCAActivityCollection()
}

cca_act_class_ext = ['students'] # Extra headers used for /view webpages for cca, activity, class and subject

default_values = {
    'student_ccarole': 'member',
    'student_activityrole': 'participant'
}

ext_headers = { # Full dictionary for extra headers used for /view webpages
    'activity': cca_act_class_ext,
    'cca': cca_act_class_ext + ['activities'],
    'class': cca_act_class_ext,
    'student': [
        'ccas',
        'activities',
        'subjects'
    ],
    'subject': cca_act_class_ext
}

radio_options = { # Dictionary for the different options when using the radio input type for different inputs
    'student_activitycategory': [
        'achievement',
        'enrichment',
        'leadership',
        'service'
    ],
    'classlevel': [
        'J1',
        'J2'
    ],
    'subjectlevel': [
        'H1',
        'H2',
        'H3'
    ],
    'student_subjectlevel': [
        'H1',
        'H2',
        'H3'
    ]
}

add_form_type = { # Dictionary for all the different input types for the add forms
    'student': {
        'name': 'text',
        'age': 'number',
        'year_enrolled': 'number',
        'graduating_year': 'number'
    },
    
    'class': {
        'name': 'text',
        'level': 'radio'
    },
    
    'cca': {
        'name': 'text',
        'type': 'text'
    },
    
    'activity': {
        'name': 'text',
        'description': 'text',
        'start_date': 'date',
        'end_date': 'date'
    },

    'subject': {
        'name': 'text',
        'level': 'radio'
    },
    'student_class': {
        'student_name': 'text',
        'class_name': 'text',
    },
    
    'student_subject': {
        'student_name': 'text',
        'subject_name': 'text',
        'level': 'radio'
    },
    
    'student_cca': {
        'student_name': 'text',
        'cca_name': 'text',
        'role': 'text'
    },
    
    'student_activity': {
        'student_name': 'text',
        'activity_name': 'text',
        'role': 'text',
        'category': 'radio',
        'award': 'text',
        'hours': 'number',
    },
    
    'cca_activity': {
        'cca_name': 'text',
        'activity_name': 'text',
    }
}

update_form_type = {}

for type, headers in add_form_type.items(): # To create a dictionary with all the input types for the update forms
    if '_' in type: # Check for collection using multiple tables
        types = type.split('_')
        update_form_type[type] = {
            f'{types[0]}_name': 'text', # For name fields belonging to each corresponding table
            f'{types[1]}_name': 'text'
        }
        
        count = 2 
        
    else:
        update_form_type[type] = {'name': 'text'}
        if type == 'subject':
            update_form_type[type]['level'] = 'radio'
        count = 0
    
    for header, value in headers.items():
        if count <= 0:
            update_form_type[type][f'new_{header}'] = value
            
        else:
            count -= 1

def add_data(update_or_add, path, type, form_data = None): # Function for adding and updating data
    data = {}
    paths = { # Form actions for different stages in adding/updating data
        '': f'/{update_or_add}_{type}?confirm',
        'confirm': f'/{update_or_add}_{type}?success',
        'success': f'/{update_or_add}_{type}',
        'fail': f'/{update_or_add}_{type}?confirm'
    }
    
    fail_msg = { # Corresponding message when failed to add/update data
        'add': 'failed to add to database.',
        'update': 'failed to update to database.'
    }
    
    if path == 'fail':
        data['msg'] = fail_msg[update_or_add] # Adding fail msg to the returned dictionary
        
    for key, act in paths.items(): # Finding the correct form action to be returned
        if key == path:
            action = act

    data['form_meta'] = { # Adding the form meta
        'action': action,
        'method': 'post'
    }
    
    if update_or_add == 'add': # Using the dictionaries to add the input types for the forms
        data['form_type'] = add_form_type[type]

    else:
        data['form_type'] = update_form_type[type]
    
    if form_data: # If form is filled in
        data['checked'] = {}
        data['form_data'] = form_data
        
        for key in form_data.keys():
            new_key = f"{type}{key.replace('new_', '')}"
            
            if new_key in list(radio_options.keys()): # checking if any data entered is a radio input
                data['checked'][key] = form_data[key]
                data['form_data'][key] = radio_options[new_key] # making sure the default checked radio option is the given input
                    

    else: # If form is not filled in
        if update_or_add == 'add': # Making the dictionary for the empty form data
            data['form_data'] = add_form_type[type].copy()
            
        else:
            data['form_data'] = update_form_type[type].copy()

        for key, value in data['form_data'].items(): # Converting the form type values into empty values
            
                if value == 'radio': # Checking if value is a radio input
                    new_key = f"{type}{key.replace('new_', '')}"
                    data['form_data'][key] = radio_options[new_key] # making the form data value be a list of the radio options
                    
                elif f"{type}{key.replace('new_', '')}" in default_values.keys(): # if value is supposed to have a default value
                    data['form_data'][key] = default_values[f"{type}{key.replace('new_', '')}"] # assigning the value to be the corresponding default value

                else:
                    data['form_data'][key] = '' # Empty value if does not fit any criteria

    data['check'] = type # adding form type as a check in the html later on
    data['path'] = path # adding the stage in which the adding/updating is in
    data['page_type'] = update_or_add # adding information on if the page is for adding or updating
    
    return data

foreign_table_names = { # To convert the html request arguments into the proper collection names
        'students': 'student',
        'activities': 'activity',
        'ccas': 'cca',
        'subjects': 'subject',
    }

def view_data(type, main = '', foreign_table = ''): # Function for the /view webpages
    data = {}
    
    data['check'] = type # adding form type as a check in the html
    data['main'] = main # adding what is the main record to focus on in the collection, is empty string if none
    data['data'] = []
    data['foreign'] = foreign_table # adding what is the foreign table to be focused on, is empty string if none
    data['form_type'] = add_form_type[type] # adding form input type for when editing/deleting data using /view pages
    
    if foreign_table: # if foreign table is focused
        foreign_table = foreign_table_names[foreign_table] # finding the correct name of the collection for the foreign table
        
        if foreign_table == 'student': # special case for when foreign is student changing the convention for the key used in the coll dict
            form_index = f'{foreign_table}_{type}'
            index = 1 
            
        else:
            form_index = f'{type}_{foreign_table}'
            index = 0 

        header = list(add_form_type[form_index].keys()) # getting headers for the multi table data
        data['form_type'] = add_form_type[form_index] # adding form input types
        records = coll[form_index].view_all() # getting all the data from the multi coll
        data['records'] = []
        data['data'] = dict(zip(add_form_type[type].keys(), coll[type].view_record(main))) # getting the data on the main record focused on
        header.pop(index)
        
        for record in records:
            if main in record:
                record = list(record)
                record.pop(index)
                data['records'].append(dict(zip(header, record))) # adding each record from the multi table coll corresponding to the main record

        data['records'] = dict(enumerate(data['records'])) # numbering the records
        data['no_of_headers'] = len(header)
        
        if 'level' in header: # special case for student_subject such that 'level' header is not considered editable
            data['no_of_headers'] -= 1
            
        header = dict(enumerate(header)) # numbering the headers
        
        for key, value in data['form_type'].items(): # check if any radio inputs
            if value == "radio":
                data['options'] = radio_options[f'{form_index}{key}'] # adding the radio options if there is radio input, becomes a dropdown for /view
    
    else: # if nothing is focused
        header = list(add_form_type[type].keys()) # headers for the coll
        
        if type == 'student': # add class header if viewing students
            header += ['class']
            
        records = coll[type].view_all() # getting data from coll
    
        for record in records:
            record = dict(zip(header, record)) # convert record into a dict
            
            if type == 'student': # if viewing students
                class_data = coll['student_class'].view_record(record['name'])
                
                if class_data:
                    record['class'] = class_data[1] # add class to record
                    
                else:
                    record['class'] = None
            
            main = list(record.values())[0]
            
            for key, value in ext_headers.items():
                if key == type:
                    for extra in value:
                        record[extra] = [f'View {extra}', f'/view_{type}?{main}&{extra}'] # adding extra headers for the main and foreign table functionality
    
                    break
            
            data['data'].append(record) # adding each record into the data

        
        data['extra'] = value # adding the list of extra headers
        
        for key, value in data['form_type'].items(): # check for any radio inputs and adding them
            if value == "radio":
                data['options'] = radio_options[f'{type}{key}']
                
        header = dict(enumerate(header + ext_headers[type])) # numbering the headers
        data['data'] = dict(enumerate(data['data'])) # numbering the records

    
    data['header'] = header # adding the headers
    
    return data

def get_update_data(view_or_update, record, is_multi = False, args = None, type = None): # for getting data when updating records
    if view_or_update == 'view': # if updated through /view
        
        if is_multi: # check for multi table coll
            values = list(record.values())
            keys = list(record.keys())

            if 'students' in args: # special case for if student table is the foreign table
                name = values[1]
                keys = [keys[0]] + keys[2:]
                coll_index = f'{foreign_table_names[args[1]]}_{type}' # changing coll key for the correct coll to be used
                
            else:
                name = values[0]
                keys = keys[1:]
                coll_index = f'{type}_{foreign_table_names[args[1]]}' # changing coll key for the correct coll to be used
                
            new_record = {}
            
            old_record = {
                'student_name': name
            }
            
            for key in keys:
                if 'old' not in key:
                    new_record[key] = record[key] # retrieving new inputted data and excluding the old data
                else:
                    if 'name' in key:
                        new_record[key] = record[key]
                        
                    old_record[key] = record[key]

            return (old_record, new_record, coll_index)
            
        # if not multi table coll
        new_record = {}
        old_record = {}
        
        for key in record.keys():
            if 'old' not in key:
                new_record[key] = record[key] # retrieving new data and removing old data
            else:
                old_record[key.replace('old_', '')] = record[key]

        return (old_record, new_record)

    else: # else if updated through /update
        new_record = {}
        
        if is_multi: # if multi table coll
            name = record['student_name'] # retrieve student name
            new_record[list(record.keys())[1]] = list(record.values())[1] # adding other tables name value

        else:
            name = record['name']
            
        for key in record.keys(): # for updating record keys to not have "new_"
            if 'new' in key:
                new_record[key.replace('new_', '')] = record[key]
                
    
    return (name, new_record)

def get_delete_data(record, type = None, args = None):
    new_record = {}
    
    for key, value in record.items(): # removing old_ from the headers
        if 'old' in key:
            new_record[key.replace('old_', '')] = value

    if args and type:
        
        if 'students' in args: # special case for if student table is the foreign table
            
            coll_index = f'{foreign_table_names[args[1]]}_{type}' # changing coll key for the correct coll to be used
            old_record = new_record.copy()
            
            new_record = { # new record to be returned
                'student_name': old_record['student_name'],
                list(old_record.keys())[0]: list(old_record.values())[0]
            }
            
            index = 2
            
            while index < len(list(old_record.values())): # add the rest of the data into new_record
                
                new_record[list(old_record.keys())[index]] = list(old_record.values())[index]
                index += 1

            
        else:
            coll_index = f'{type}_{foreign_table_names[args[1]]}' # changing coll key for the correct coll to be used
    else:
        coll_index = type

    return (new_record, coll_index)

    

def add_update(update_or_add, type, rqst): # add/update function for rendering add/update forms
    if rqst.args: # checks if form is in 'success' or 'confirm' stages
        
        if not dict(rqst.form).values(): # if no data entered redirect back to first stage
            return redirect(f"/{update_or_add}_{type}")
            
        if 'success' in rqst.args: # if 'success' stage
            if update_or_add == 'add': # if is /add
                result = coll[type].add_record(dict(rqst.form)) # add the record
                
            else:
                if '_' in type: # if multi table
                    data = get_update_data('update', dict(rqst.form), True) # get data for multi table coll
                    old_record = {
                        'name1': list(dict(rqst.form).values())[0],
                        'name2': list(dict(rqst.form).values())[1]
                    }
                    
                    
                else:
                    data = get_update_data('update', dict(rqst.form)) # get data for single table coll
                    old_record = {'name': data[0]}
                    if type == 'subject':
                        old_record['level'] = rqst.form['level']

                if old_record:
                    result = coll[type].edit_record(old_record, data[1]) # edit the data
                else:
                    result = False

            if not result: # if failed to add/update
                return render_template('add_update.html', data = add_data(update_or_add, 'fail', type = type, form_data = dict(rqst.form))) # fail page
        
        return render_template('add_update.html', data = add_data(update_or_add, list(request.args)[0], type = type, form_data = dict(rqst.form))) # 'confirm' or 'success' page
    
    return render_template('add_update.html', data = add_data(update_or_add, '', type = type)) # first stage page

def view(type, rqst): # view function for rendering /view pages
    if rqst.args: # checks if to focus on any records or to edit/delete
        args = list(rqst.args)
        
        if 'edit' in rqst.args: # if to edit data
            
            if len(rqst.args) > 1: # if multi table coll update
                data = get_update_data('view', dict(rqst.form), True, args, type) # gets data for updating multi table coll data
                print(data)
                coll[data[2]].edit_record(data[0], data[1]) # edits the data
                
                return redirect(f'/view_{type}?{args[0]}&{args[1]}') # redirects to the same page

            data = get_update_data('view', dict(rqst.form)) # gets data for updating single table coll data
            coll[type].edit_record(data[0], data[1]) # edit the data
            if type == 'student':
                old_record = {'student': data[0]['name'], 'class': data[0]['class']}
                new_record = {'student': data[1]['name'], 'class': data[1]['class']}
                coll['student_class'].edit_record(old_record, new_record)
            
            return redirect(f'/view_{type}') # redirects to the same page
            
        elif 'delete' in rqst.args: # if deleting data
            
            if len(rqst.args) > 1: # if multi table coll delete
                data = get_delete_data(dict(rqst.form), type, args) # gets data for deleting multi table coll data
                coll[data[1]].delete_record(data[0]) # deletes the data
                
                return redirect(f'/view_{type}?{args[0]}&{args[1]}') # redirects to the same page
                
            data = get_delete_data(dict(rqst.form), type) # gets data for deleting single table coll data
            coll[type].delete_record(data[0]) # deletes data
            
            return redirect(f'/view_{type}') # redirects to the same page
            
        return render_template('view.html', data = view_data(type, args[0], args[1])) # renders data when focused on multi table coll
        
    return render_template('view.html', data = view_data(type)) # renders main records