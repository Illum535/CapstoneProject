from storage import ActivityCollection, CCACollection

act_coll = ActivityCollection()
cca_coll = CCACollection()
coll = {
    'activity': act_coll,
    'cca': cca_coll
}

cca_act_class_ext = ['students']

ext_headers = {
    'activity': cca_act_class_ext,
    'cca': cca_act_class_ext,
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

cca_header = [
    'name',
    'type'
]

headers = {
    'activity': act_header,
    'cca': cca_header
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

def view_data(type, specific = ''):
    data = {}

    data['check'] = type
    data['specific'] = specific
    data['data'] = []
    records = coll[type].view_all()
    header = headers[type]
    for record in records:
        record = dict(zip(header, record))
        main = list(record.values())[0]
        for key, value in ext_headers.items():
            if key == type:
                for extra in value:
                    record[extra] = [f'View {extra}', f'/view_{type}?{main}']
                break
                
        data['data'].append(record)

    data['extra'] = value
    
    header = {}
    
    for index, key in enumerate(data['data'][0].keys()):
        header[index] = key
        
    data['header'] = header
    data['main_header'] = list(header.values())[0]

    return data

