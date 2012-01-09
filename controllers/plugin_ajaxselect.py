from gluon.sqlhtml import OptionsWidget

def set_widget():
    """
    creates a replacement instance of the OptionsWidget class defined in gluon.sqlhtml and returns the result to re-populate the ajax LOAD field
    """

    #get variables to build widget for the proper field, with proper current value
    table = request.args[0]
    field = request.args[1]
    value = request.args[2]
    linktable = request.args[3]
    wrappername = request.args[4]

    the_table = db[table]
    the_field = the_table[field]
    the_linktable = db[linktable]

    w = OptionsWidget.widget(the_field, value) 

    return dict(widget = w, linktable = linktable)

def set_form_wrapper():
    """
    Creates the LOAD helper to hold the modal form for creating a new item in the linked table
    """
    tablename = request.args[0]
    fieldname = request.args[1]
    value = request.args[2]
    linktable = request.args[3]
    wrappername = request.args[4]


    formwrapper = LOAD('plugin_ajaxselect', 'linked_create_form.load', args=[tablename, fieldname, value, linktable, wrappername], ajax=True)

    return dict(formwrapper = formwrapper)


def linked_create_form():
    """
    creates a form to insert a new entry into the linked table which populates the ajaxSelect widget
    """

    tablename = request.args[0]
    fieldname = request.args[1]
    value = request.args[2]
    linktable = request.args[3]
    wrappername = request.args[4]

    form = SQLFORM(db[linktable])

    comp_url = URL('plugin_ajaxselect', 'set_widget.load', args=[tablename, fieldname, value, linktable, wrappername])

    if form.process().accepted:
        response.flash = 'form accepted'
        response.js = "web2py_component('%s', '%s');" % (comp_url, wrappername)
    else:
        response.error = 'form was not processed'

    return dict(form = form)
