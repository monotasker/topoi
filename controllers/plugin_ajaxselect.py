from gluon.sqlhtml import OptionsWidget


def set_widget():
    """
    creates an instance of the OptionsWidget class defined in gluon.sqlhtml and returns the result to populate the ajax LOAD field
    """

    #get variables to build widget for the proper field, with proper current value
    table = request.args[0]
    field = request.args[1]
    value = request.args[2]
    linktable = request.args[3]
    loadname = request.args[4]

    the_table = db[table]
    the_field = the_table[field]
    the_linktable = db[linktable]

    #create HTML select widget using OptionsWidget class from gluon.sqlhtml
    w = OptionsWidget.widget(the_field, value)
    print w

    #URL to reload component
    comp_url = URL('plugin_ajaxselect', 'set_widget.load', args=[table, field, value, linktable, loadname])

    """
    formname = '%s/create' % (linktable)

    form = SQLFORM(the_linktable)
    if form.accepts(request, session, formname = formname):
        response.flash = 'form accepted'
        #response.js = "web2py_component('%', '%');" % (comp_url, loadname)
    else:
        response.error = 'form was not processed'
    """

    #create button to trigger table refresh
    bid = table + '_' + field + '_option_refresh_trigger'
    button = A('refresh', _href=comp_url, cid=request.cid)

    #create button to trigger adding dialog
    #button = A('Add New', _href='#', _id=bid, _class='button_secondary option_add_trigger')

    return dict(widget = w, button = button, loadname = loadname) # form = form,
