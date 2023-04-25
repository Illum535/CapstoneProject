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
        '': f'/add_{type}?confirm',
        'confirm': f'/add_{type}?success',
        'success': f'/add_{type}',
        'fail': f'/add_{type}'
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