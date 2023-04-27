from storage import *

coll = {
    'activity': ActivityCollection(),
    'cca': CCACollection(),
    'class': ClassCollection(),
    'student': StudentCollection(),
    'studentclass': StudentClassCollection(),
    'studentcca': StudentCCACollection(),
    'studentactivity': StudentActivityCollection(),
    'studentsubject': StudentSubjectCollection(),
    'activitycca': CCAActivityCollection()
}

cca_act_class_ext = ['students']

ext_headers = {
    'activity': cca_act_class_ext,
    'cca': cca_act_class_ext + ['activities'],
    'class': cca_act_class_ext,
    'student': [
        'ccas',
        'activities',
        'subjects'
    ]
}


act_header = [
    'name',
    'description',
    'start_date',
    'end_date'
]

class_header = [
    'name',
    'level'
]

cca_header = [
    'name',
    'type'
]

student_header = [
    'name',
    'age',
    'year_enrolled',
    'graduating_year'
]

subject_header = [
    'name',
    'level'
]

studentcca_header = [
    'role'
]

studentactivity_header = [
    'category',
    'role',
    'award',
    'hours'
]

headers = {
    'activity': act_header,
    'cca': cca_header,
    'class': class_header,
    'student': student_header,
    'subject_header': subject_header,
    'studentclass': [],
    'studentcca': studentcca_header,
    'studentactivity': studentactivity_header,
    'studentsubject': [],
    'activitycca': []
}


act_cat = [
            'achievement',
            'enrichment',
            'leadership',
            'service'
        ]

add_forms = {
    'cca': {
        'name': '',
        'type': ''
    },
    
    'activity': {
        'name': '',
        'start_date': '',
        'end_date': '',
        'description': ''
    }
}

update_forms = {
    'cca': {
        'cca_name': '',
        'student_name': '',
        'role': 'Member'
    },
    
    'activity': {
        'name': '',
        'student_name': '',
        'category': act_cat,
        'role': 'Participant',
        'award': '',
        'hours': '',
    }
}

add_form_type = {
    'cca': {
        'name': 'text',
        'type': 'text'
    },
    
    'activity': {
        'name': 'text',
        'start_date': 'date',
        'end_date': 'date',
        'description': 'text'
    }
}

update_form_type = {
    'cca': {
        'student_name': 'text',
        'cca_name': 'text',
        'role': 'text'
    },
    
    'activity': {
        'student_name': 'text',
        'activity_name': 'text',
        'category': 'radio',
        'role': 'text',
        'award': 'text',
        'hours': 'number',
    }
}


def add_data(update_or_add, path, type, form_data = None):
    data = {}
    paths = {
        '': f'/{update_or_add}_{type}?confirm',
        'confirm': f'/{update_or_add}_{type}?success',
        'success': f'/{update_or_add}_{type}',
        'fail': f'/{update_or_add}_{type}'
    }

    for key, act in paths.items():
        if key == path:
            action = act

    data['form_meta'] = {
        'action': action,
        'method': 'post'
    }
    if form_data:
        data['form_data'] = form_data
        if 'category' in form_data.keys():
            data['checked'] = form_data['category']
            data['form_data']['category'] = act_cat

    else:
        if update_or_add == 'add':
            data['form_data'] = add_forms[type]
            
        else:
            data['form_data'] = update_forms[type]

    data['check'] = type
    data['path'] = path
    data['page_type'] = update_or_add
    
    if update_or_add == 'add':
        data['form_type'] = add_form_type[type]

    else:
        data['form_type'] = update_form_type[type]
    
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
    
    if foreign_table:
        main_record = coll[type].view_record(main_table)
        main_id = main_record[0]

        main_record = dict(zip(headers[type], main_record))
        
        foreign_table = foreign_table_names[foreign_table]
        if type == 'student':
            data['header'] = dict(enumerate(['name'] + headers[f"{type}{foreign_table}"]))
            records = coll[f"{type}{foreign_table}"].view_all(headers[f"{type}{foreign_table}"])
            index = 0 
        
        else:
            data['header'] = dict(enumerate(['name'] + headers[f"{foreign_table}{type}"]))
            records = coll[f"{foreign_table}{type}"].view_all(headers[f"{foreign_table}{type}"])
            index = 1
        
        for key, value in foreign_table_names.items():
            if value == type:
                type = key
            
        used_records = []
        for record in records:
            if record[index] == main_id:
                record = list(record)
                record.pop(index)
                used_records.append(record)

        
        data['data'] = main_record
        data['records'] = used_records
        data['extra'] = []
    
    else:
        if type != 'student':
            header = headers[type]
            records = coll[type].view_all()
        else:
            header = ['name', 'class']
            records = coll['studentclass'].view_all(headers['studentclass'])
        
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
            
            header = {}
            
            for index, key in enumerate(data['data'][0].keys()):
                header[index] = key
                
            data['header'] = header
            data['main_header'] = list(header.values())[0]

    return data

