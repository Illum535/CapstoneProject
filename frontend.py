forms = {
    'cca': {
        'name': '',
        'type': ''
    },
    
    'act': {
        'start_date': '',
        'end_date': '',
        'description': ''
    }
}

form_type = {
    'cca': {
        'name': 'text',
        'type': 'text'
    },
    
    'act': {
        'start_date': 'date',
        'end_date': 'date',
        'description': 'text'
    }
}


def add_data(path, type, form_data = None):
    data = {}
    paths = {
        '': f'/new_{type}?confirm',
        'confirm': f'/new_{type}?success',
        'success': f'/new_{type}',
        'fail': f'/new_{type}'
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

    else:
        data['form_data'] = forms[type]

    data['check'] = type
    data['path'] = path
    data['form_type'] = form_type[type]
        
    return data