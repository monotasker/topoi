
@auth.requires_membership(role='administrators')
def listing():
    response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.css'))
    response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.js'))
    response.files.append(URL('static', 'plugin_listandedit/plugin_listandedit.css'))
    
    return dict()
