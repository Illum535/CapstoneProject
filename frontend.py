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
        'start_date': '',
        'end_date': '',
        'description': ''
    }
}

update_forms = {
    'cca': {
        'student_name': '',
        'cca_name': '',
        'role': 'Member'
    },
    
    'activity': {
        'student_name': '',
        'activity_description': '',
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
        'activity_description': 'text',
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

def view_data(type):
    data = {}

    data['check'] = type
    data['data'] = [
        {
            'name': 'placeholder1',
            'class': 'pc4'
        },
        {
            'name': 'placeholder2',
            'class': 'pc3'
        },
        {
            'name': 'placeholder3',
            'class': 'pc2'
        },
        {
            'name': 'placeholder4',
            'class': 'pc1'
        },
    ] #Replace with database function
    header = {}
    
    for index, key in enumerate(data['data'][0].keys()):
        header[index] = key
        
    data['header'] = header
    
    return data

