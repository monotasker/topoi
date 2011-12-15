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

    w = OptionsWidget.widget(the_field, value)

    f = SQLFORM(the_linktable)

    comp_url = URL('plugin_ajaxselect', 'set_widget.load', args=[table, field, value, linktable, loadname])

    #create button to trigger adding dialog
    bid = table + '_' + field + '_option_add_trigger'
    button = A('Add New', _href='#', _id=bid, _class='option_add_trigger')

    return dict(widget = w, button = button, form = f, comp_url = comp_url, loadname = loadname)
