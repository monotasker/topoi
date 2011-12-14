# coding: utf8
from gluon.custom_import import track_changes
from gluon.sqlhtml import *
from gluon.compileapp import LoadFactory
from gluon import current
from plugin_multiselect_widget import hmultiselect_widget, vmultiselect_widget
from plugin_ajaxselect import AjaxSelect

#FIXME: set track changes to false when dev is finished
track_changes(True)

class SelectOrAddOption(object):

    def __init__(self, controller = None, function = None, form_title = None, button_text = None, dialog_width = 450):
        self.T = current.T
        if form_title == None:
            self.form_title = self.T('Add New')
        else:
            self.form_title = form_title
        if button_text == None:
            self.button_text = self.T('Add')
        else:
            self.button_text = button_text
        self.dialog_width = dialog_width
        self.controller = controller
        self.function = function

    def widget(self, field, value, tablename):
        # initialize LOAD helper
        environment = {'request': current.request, 'response': current.response}
        LOAD = LoadFactory(environment)

        #generate the standard widget for this field
        select_widget = AjaxSelect(field, value).widget()

        #get the widget's id (need to know later on so can tell receiving controller what to update)
        my_select_id = select_widget.attributes.get('_id', None)
        #send widget's id and name of db table referenced by widget
        add_args = [my_select_id, tablename]

        #create a div that will load the specified controller via ajax
        form_loader_div = DIV(LOAD(c = self.controller, f = self.function, args = add_args, ajax = True), _id = my_select_id + "_dialog-form", _title = self.form_title)
        #generate the "add" button that will appear next the options widget and open our dialog
        activator_button = A(self.button_text, _id = my_select_id + "_option_add_trigger")
        #create javascript for creating and opening the dialog
        js = '$( "#%s_dialog-form" ).dialog({autoOpen: false, show: "blind", hide: "explode", width: %s});' % (my_select_id, self.dialog_width)
        js += '$( "#%s_option_add_trigger" ).click(function() { $( "#%s_dialog-form" ).dialog( "open" );return false;}); ' % (my_select_id, my_select_id)
        #decorate our activator button for good measure
        #TODO: decide whether to keep this jquery UI decoration on button
        #js += '$(function() { $( "#%s_option_add_trigger" ).button({text: true, icons: { primary: "ui-icon-circle-plus"} }); });' % (my_select_id)
        jq_script = SCRIPT(js, _type = "text/javascript")

        wrapper = DIV(_id = my_select_id + "_adder_wrapper")
        wrapper.components.extend([select_widget, form_loader_div, activator_button, jq_script])
        return wrapper


class MULTISELECT_OR_ADD_OPTION(SelectOrAddOption):

    #FIXME: FIND a way to reduce repeated code in this subclass
    def widget(self, field, value, tablename):
        # initialize LOAD helper
        environment = {'request': current.request, 'response': current.response}
        LOAD = LoadFactory(environment)

        #generate the standard widget for this field
        select_widget = hmultiselect_widget(field, value)

        #get the widget's id (need to know later on so can tell receiving controller what to update)
        my_select_id = select_widget.attributes.get('_id', None)
        add_args = [my_select_id, tablename]

        #create a div that will load the specified controller via ajax
        form_loader_div = DIV(LOAD(c = self.controller, f = self.function, args = add_args, ajax = True), _id = my_select_id + "_dialog-form", _title = self.form_title)
        #generate the "add" button that will appear next the options widget and open our dialog
        activator_button = A(self.button_text, _id = my_select_id + "_option_add_trigger")
        #create javascript for creating and opening the dialog
        js = '$( "#%s_dialog-form" ).dialog({autoOpen: false, show: "blind", hide: "explode", width: %s});' % (my_select_id, self.dialog_width)
        js += '$( "#%s_option_add_trigger" ).click(function() { $( "#%s_dialog-form" ).dialog( "open" );return false;}); ' % (my_select_id, my_select_id)
        #decorate our activator button for good measure
        #js += '$(function() { $( "#%s_option_add_trigger" ).button({text: true, icons: { primary: "ui-icon-circle-plus"} }); });' % (my_select_id)
        jq_script = SCRIPT(js, _type = "text/javascript")

        wrapper = DIV(_id = my_select_id + "_adder_wrapper")
        wrapper.components.extend([select_widget, form_loader_div, activator_button, jq_script])
        return wrapper


