from storage import *
from flask import Flask, render_template, request, redirect

coll = {
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
    ],
    'student_subjectlevel': [
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
        'category': 'radio',
        'role': 'text',
        'award': 'text',
        'hours': 'number',
    },
    
    'cca_activity': {
        'cca_name': 'text',
        'activity_name': 'text',
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

foreign_table_names = {
        'students': 'student',
        'activities': 'activity',
        'ccas': 'cca',
        'subjects': 'subject',
    }

def view_data(type, main = '', foreign_table = ''):
    data = {}
    
    data['check'] = type
    data['main'] = main
    data['data'] = []
    data['foreign'] = foreign_table
    data['form_type'] = add_form_type[type]
    
    if foreign_table:
        foreign_table = foreign_table_names[foreign_table]
        if foreign_table == 'student':
            form_index = f'{foreign_table}_{type}'
            index = 1
        else:
            form_index = f'{type}_{foreign_table}'
            index = 0

        header = list(add_form_type[form_index].keys())
        data['form_type'] = add_form_type[form_index]
        records = coll[form_index].view_all()
        data['records'] = []
        data['data'] = dict(zip(add_form_type[type].keys(), coll[type].view_record(main)))
        header.pop(index)
        for record in records:
            if main in record:
                record = list(record)
                record.pop(index)
                data['records'].append(dict(zip(header, record)))

        data['records'] = dict(enumerate(data['records']))
        data['no_of_headers'] = len(header)
        if 'level' in header:
            data['no_of_headers'] -= 1
            
        header = dict(enumerate(header))
        for key, value in data['form_type'].items():
            if value == "radio":
                data['options'] = radio_options[f'{form_index}{key}']
    
    else:
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

        
        data['extra'] = value
        for key, value in data['form_type'].items():
            if value == "radio":
                data['options'] = radio_options[f'{type}{key}']
                
        header = dict(enumerate(header + ext_headers[type]))
        data['data'] = dict(enumerate(data['data']))

    
    data['header'] = header
    return data

def get_update_data(view_or_update, record, is_multi = False, args = None, type = None):
    if view_or_update == 'view':
        if is_multi:
            values = list(record.values())
            keys = list(record.keys())

            if 'students' in args:
                name = values[1]
                record = [values[0]] + values[2:]
                coll_index = f'{foreign_table_names[args[1]]}_{type}'
            else:
                name = values[0]
                record = values[1:]
                coll_index = f'{type}_{foreign_table_names[args[1]]}'
                
                
            new_record = {}
            for index, value in enumerate(record):
                if index % 2 == 0:
                    new_record[keys[1:][index]] = value

            return (name, new_record, coll_index)
            
        name = record['old_name']
        new_record = {}
        for key in record.keys():
            if 'old' not in key:
                new_record[key] = record[key]

    else:
        new_record = {}
        if is_multi:
            name = record['student_name']
            new_record[list(record.keys())[1]] = list(record.values())[1]
        else:
            name = record['name']
            
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
                if '_' in type:
                    data = get_update_data('update', dict(rqst.form), True)
                else:
                    data = get_update_data('update', dict(rqst.form))
                print(data)
                result = coll[type].edit_record(data[0], data[1])
                
            if result:
                return render_template('add_update.html', data = add_data(update_or_add, 'fail', type = type, form_data = dict(rqst.form)))
        
        return render_template('add_update.html', data = add_data(update_or_add, list(request.args)[0], type = type, form_data = dict(rqst.form)))
    
    return render_template('add_update.html', data = add_data(update_or_add, '', type = type))

def view(type, rqst):
    if rqst.args:
        args = list(rqst.args)
        if 'edit' in rqst.args:
            if len(rqst.args) > 1:
                data = get_update_data('view', dict(rqst.form), True, args, type)
                coll[data[2]].edit_record(data[0], data[1])
                return redirect(f'/view_{type}?{args[0]}&{args[1]}')
                
            data = get_update_data('view', dict(rqst.form))
            coll[type].edit_record(data[0], data[1])
            return redirect(f'/view_{type}')
            
        elif 'delete' in rqst.args:
            if len(rqst.args) > 1:
                data = get_update_data('view', dict(rqst.form), True, args, type)
                coll[data[2]].delete_record(data[0])
                return redirect(f'/view_{type}?{args[0]}&{args[1]}')
                
            data = get_update_data('view', dict(rqst.form))
            coll[type].delete_record(data[0])
            return redirect(f'/view_{type}')
            
        return render_template('view.html', data = view_data(type, args[0], args[1]))
        
    return render_template('view.html', data = view_data(type))