from gluon import sqlhtml, current, SPAN, A
from gluon.compileapp import LoadFactory
from gluon.custom_import import track_changes

session = current.session

#FIXME: set track changes to false when dev is finished
track_changes(True)

class AjaxSelect:
    def __init__(self, field, value):
        self.field = field
        self.value = value

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

        #create component wrapper with ajax loading helper
        wrapper = LOAD('plugin_ajaxselect', 'set_widget.load',
            args=[tablename, fieldname, self.value], ajax=True)

        return wrapper
