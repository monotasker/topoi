from gluon.sqlhtml import OptionsWidget


def set_widget():
    """
    creates an instance of the OptionsWidget class defined in gluon.sqlhtml and returns the result to populate the ajax LOAD field
    """
    table = request.args[0]
    field = request.args[1]
    value = request.args[2]

    the_table = db[table]
    the_field = the_table[field]
    print the_field

    w = OptionsWidget.widget(the_field, value)

    #create button to trigger adding dialog
    bid = table + '_' + field + '_option_add_trigger'
    button = A('Add New', _href='#', _id=bid _class='option_add_trigger')

    return dict(widget = w, button = button)
