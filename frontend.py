from storage import *
from flask import Flask, render_template, request, redirect

coll = {
    'activity': ActivityCollection(),
    'cca': CCACollection(),
    'class': ClassCollection(),
    'student': StudentCollection(),
    'subject': SubjectCollection()
    # 'studentclass': StudentClassCollection(),
    # 'studentcca': StudentCCACollection(),
    # 'studentactivity': StudentActivityCollection(),
    # 'studentsubject': StudentSubjectCollection(),
    # 'activitycca': CCAActivityCollection()
}

cca_act_class_ext = ['students']

default_values = {
    'student_ccarole': 'member',
    'student_activityrole': 'participant'
}

ext_headers = {
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

radio_options = {
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
    ]
}

add_form_type = {
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
    
    'student_cca': {
        'student_name': 'text',
        'cca_name': 'text',
        'role': 'text'
    },
    
    'student_activity': {
        'student_name': 'text',
        'activity_name': 'text',
        'category': 'radio',
        'role': 'text',
        'award': 'text',
        'hours': 'number',
    }
}

update_form_type = {}

for type, headers in add_form_type.items():
    if '_' in type:
        types = type.split('_')
        update_form_type[type] = {
            f'{types[0]}_name': 'text',
            f'{types[1]}_name': 'text'
        }
        count = 2
        
    else:
        update_form_type[type] = {'name': 'text'}
        count = 0
    
    for header, value in headers.items():
        if count <= 0:
            update_form_type[type][f'new_{header}'] = value
        else:
            count -= 1

def add_data(update_or_add, path, type, form_data = None):
    data = {}
    paths = {
        '': f'/{update_or_add}_{type}?confirm',
        'confirm': f'/{update_or_add}_{type}?success',
        'success': f'/{update_or_add}_{type}',
        'fail': f'/{update_or_add}_{type}?confirm'
    }
    fail_msg = {
        'add': 'already in database.',
        'update': 'not in database.'
    }
    
    if path == 'fail':
        data['msg'] = fail_msg[update_or_add]
        
    for key, act in paths.items():
        if key == path:
            action = act

    data['form_meta'] = {
        'action': action,
        'method': 'post'
    }
    if update_or_add == 'add':
        data['form_type'] = add_form_type[type]

    else:
        data['form_type'] = update_form_type[type]
    
    if form_data:
        data['form_data'] = form_data
        for key in form_data.keys():
            new_key = f"{type}{key.replace('new_', '')}"
            if new_key in list(radio_options.keys()):
                data['checked'] = form_data[key]
                data['form_data'][key] = radio_options[new_key]
                    

    else:
        if update_or_add == 'add':
            data['form_data'] = add_form_type[type].copy()
        else:
            data['form_data'] = update_form_type[type].copy()

        for key, value in data['form_data'].items():
                if value == 'radio':
                    new_key = f"{type}{key.replace('new_', '')}"
                    data['form_data'][key] = radio_options[new_key]
                    
                elif f'{type}{key}' in default_values.keys():
                    data['form_data'][key] = default_values[f'{type}{key}']

                else:
                    data['form_data'][key] = ''

    data['check'] = type
    data['path'] = path
    data['page_type'] = update_or_add
    return data

def view_data(type, main_table = '', foreign_table = ''):
    data = {}
    foreign_table_names = {
        'students': 'student',
        'activities': 'activity',
        'ccas': 'cca',
        'subjects': 'subject',
    }
    
    
    data['check'] = type
    data['main'] = main_table
    data['foreign'] = foreign_table
    data['data'] = []
    
    header = list(add_form_type[type].keys())
    records = coll[type].view_all()

    for record in records:
        record = dict(zip(header, record))
        
        main = list(record.values())[0]
        for key, value in ext_headers.items():
            if key == type:
                for extra in value:
                    record[extra] = [f'View {extra}', f'/view_{type}?{main}&{extra}']

                break
            
        data['data'].append(record)

    data['data'] = dict(enumerate(data['data']))
    data['extra'] = value
    data['form_type'] = add_form_type[type]
    for key, value in data['form_type'].items():
        if value == "radio":
            data['options'] = radio_options[f'{type}{key}']
            
    header = dict(enumerate(header + ext_headers[type]))
    
    data['header'] = header
    data['main_header'] = list(header.values())[0]

    return data

def get_update_data(view_or_update, record):
    if view_or_update == 'view':
        name = record['old_name']
        new_record = {}
        for key in record.keys():
            if 'old' not in key:
                new_record[key] = record[key]

    else:
        name = record['name']
        new_record = {}
        for key in record.keys():
            if 'new' in key:
                new_record[key.replace('new_', '')] = record[key]

    return (name, new_record)

def add_update(update_or_add, type, rqst):
    if rqst.args:
        if not dict(rqst.form).values():
            return redirect(f"/{update_or_add}_{type}")
        if 'success' in rqst.args:
            if update_or_add == 'add':
                result = coll[type].add_record(dict(rqst.form))
            else:
                data = get_update_data('update', dict(rqst.form))
                result = coll[type].edit_record(data[0], data[1])
                
            if result:
                return render_template('add_update.html', data = add_data(update_or_add, 'fail', type = type, form_data = dict(rqst.form)))
        
        return render_template('add_update.html', data = add_data(update_or_add, list(request.args)[0], type = type, form_data = dict(rqst.form)))
    
    return render_template('add_update.html', data = add_data(update_or_add, '', type = type))

def view(type, rqst):
    if rqst.args:
        if 'edit' in rqst.args:
            data = get_update_data('view', dict(rqst.form))
            coll[type].edit_record(data[0], data[1])
            return redirect(f'/view_{type}')
            
        return render_template('view.html', data = view_data(type, list(rqst.args)[0], list(rqst.args)[1]))
        
    return render_template('view.html', data = view_data(type))