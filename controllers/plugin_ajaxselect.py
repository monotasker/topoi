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
    wrappername = request.args[4]

    the_table = db[table]
    the_field = the_table[field]
    the_linktable = db[linktable]

    formname = '%s/create' % (linktable)

    form2 = SQLFORM(the_linktable)
    if form2.process(formname = formname).accepted:
        print formname
        response.flash = 'form accepted'
        #response.js = "web2py_component('%', '%');" % (comp_url, wrappername)
    else:
        response.error = 'form was not processed'

    w = OptionsWidget.widget(the_field, value)

    return dict(widget = w, wrappername = wrappername, form2 = form2, linktable = linktable)
