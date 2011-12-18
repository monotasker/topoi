from gluon import sqlhtml, current, SPAN, A
from gluon.compileapp import LoadFactory
from gluon.custom_import import track_changes

session = current.session

#FIXME: set track changes to false when dev is finished
track_changes(True)

class AjaxSelect:
    """
    Creates a select widget wrapped in a web2py LOAD helper so that it can be refreshed via ajax without resetting the entire form.

    Usage: In a web2py model file, import this class and then apply it as the widget-factory for one or more db fields. To do this for a field named 'author' from a table named 'notes' you would add this line somewhere in the model file:

    db.notes.author.widget = lambda field, value: AjaxSelect(field, value, 'authors').widget()

    Note that the third argument passed to AjaxSelect should be the name of the table *referenced by the current field*. In this example, the field 'author' references the table 'authors'. So the third argument in this case is 'authors'.

    """
    def __init__(self, field, value, linktable):
        self.field = field
        self.value = value
        self.linktable = linktable

    def widget(self):
        # initialize LOAD helper
        environment = {
            'request': current.request,
            'response': current.response}
        LOAD = LoadFactory(environment)

        #get field and tablenames for element id's
        fieldset = str(self.field).split('.')
        tablename = fieldset[0]
        fieldname = fieldset[1]

        loadname = '%s_%s_loader' %(tablename, fieldname)

        #create component wrapper with ajax loading helper
        wrapper = LOAD('plugin_ajaxselect', 'set_widget.load',
            args=[tablename, fieldname, self.value, self.linktable, loadname],
            ajax=True,
            target=loadname)

        return wrapper
