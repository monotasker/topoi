from gluon import sqlhtml, current, SPAN, A
from gluon.compileapp import LoadFactory
from gluon.custom_import import track_changes
from gluon.html import URL
from gluon.sqlhtml import OptionsWidget

session = current.session
request = current.request

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
        """
        Returns a select widget that can be refreshed (via Ajax) by clicking the accompanying button. This allows updating of the select's contents without refreshing the whole form.
        """

        #get field and tablenames for element id's
        fieldset = str(self.field).split('.')
        tablename = fieldset[0]
        fieldname = fieldset[1]


        wrappername = '%s_%s_loader' %(tablename, fieldname)

        #URL to reload widget via ajax
        comp_url = URL('plugin_ajaxselect', 'set_widget.load', args=[tablename, fieldname, self.value, self.linktable, wrappername])

        #create component wrapper with ajax loading helper
        adder_id = '%s_add_trigger' % (self.linktable)
        w = OptionsWidget.widget(self.field, self.value)
        wrapper = SPAN(w, _id=wrappername), A('refresh', _href=comp_url, cid=wrappername), A('add new', _href='#', _id=adder_id)

        return wrapper
