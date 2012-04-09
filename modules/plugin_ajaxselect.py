from gluon import current, SPAN, A, DIV, SQLFORM, INPUT, UL, LI, OPTION, SELECT
from gluon.html import URL
from gluon.sqlhtml import OptionsWidget, MultipleOptionsWidget 
import pprint
#TODO: add ListWidget as another option?

class AjaxSelect(object):
    """
    This plugin creates a select widget wrapped that can be refreshed via ajax 
    without resetting the entire form. It also provides an "add new" button 
    that allows users to add a new item to the table that populates the select 
    widget via ajax. The widget is then automatically refreshed via ajax so that 
    the new item is visible as a select option and can be chosen. All of this
    happens without a page or form refresh so that data entered in other fields 
    is not lost or submitted.

    Installation:
    1. download the plugin file;
    2. In the web2py online ide (design view for your app) scroll to the bottom 
    section labeled "Plugins";
    3. At the bottom of that section is a widget to "upload plugin file". Click 
    "Browse".
    4. In the file selection window that opens, navigate to the downloaded 
    plugin file, select it, and click "open". The file selection window should 
    close.
    5. Click the "upload" button.
    6. Add the following three lines to the top of a module file to make db 
    available in the 'current' object and to include the js and css files for 
    the plugin:
        from gluon import current
        current.db = db
        response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.css'))
        response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.js'))

    The plugin should now be installed and ready to use.

    Usage:
    In a web2py model file, import this class and then apply it as
    the widget-factory for one or more db fields. To do this for a field named
    'author' from a table named 'notes' you would add this line somewhere in
    the model file:

    db.notes.author.widget = lambda field, value: AjaxSelect(field, value, 
    {optional arguments}).widget()

    Optional arguments:
    :param refresher (True/False; defaults to True):a button to manually refresh the 
    select widget via ajax.

    :param adder (True/False; defaults to True): a button to add a new record to the 
    linked table that populates the select widget.

    :param restrictor ({form field name}): adds a dynamic constraint on the records 
    displayed in the named field's widget. When the specified form field 
    (within the same form) has its value changed, this select will be refreshed 
    and its displayed records filtered accordingly. Note that this is only 
    useful if {fieldname} references values shared with the linked table.

    e.g., to make the select constrain the widget for the 'works' table:
    db.notes.author.widget = lambda field, value: AjaxSelect(field, value, 
    'authors', restrictor='work').widget()

    :param multi (basic/False; defaults to False): Instead of displaying a single 
    select widget, the 'basic' value displays a standard multiselect widget (an 
    html select widget with a size greater than 1). This will only work 
    properly if the database field type is defined as "list:reference" in the 
    model. 

    :lister (False/'simple'/'editlinks'; defaults to False): 'normal' adds a 
    list of the widget's currently selected values below a multiselect widget. If 
    set to 'editlinks' these passive list items become links opening edit forms
    for the linked items in a modal window.

    """
    """TODO: allow for restrictor argument to take list and filter multiple other 
    fields"""

    def __init__(self):
        print '\n starting modules/plugin_ajaxselect __init__'
        
    def widget(self, field, value, restricted=None, refresher=False, 
                adder=True, restrictor=None, multi=False, lister=False):
        """
        Main method to create the ajaxselect widget. Calls helper methods 
        and returns the wrapper element containing all associated elements. 
        """
        session, request = current.session, current.request

        print '\nstarting AjaxSelect.widget()'
        #assemble information first
        fieldset = str(field).split('.')
        wrappername = self.wrappername(fieldset)
        linktable = self.linktable(field) #find table referenced by widget
        form_name = '%s_adder_form' % linktable #for referenced table form
        value = self.choose_val(value, wrappername) #choose db or session
        clean_val = self.clean(value, multi)
        uargs = fieldset #args for add and refresh urls
        restricted = self.restricted(restricted) #isolate setting of this param
        uvars = dict(value=clean_val, linktable=linktable, 
                    wrappername=wrappername, refresher=refresher,
                    adder=adder, restrictor=restrictor,
                    multi=multi, lister=lister, 
                    restricted=restricted) #vars for add and refresh urls

        #create and assemble elements of widget
        wrapper = SPAN('', _id = wrappername, _class = self.classes())
        wrapper[0] = self.create_widget()
        wrapper.append(self.hidden_ajax_field(wrappername))
        wrapper.append(self.refresher(wrappername, uargs, uvars))
        wrapper.append(self.adder(wrappername, linktable, uargs, uvars, form_name))
        wrapper.append(self.dialog(form_name))
        if multi and lister == 'simple':
            wrapper.append(self.taglist(value, linktable))
        elif multi and lister == 'editlinks':
            wrapper.append(self.linklist(value, linktable, uargs, uvars))
        else:
            print 'did not request list of tags'

        return wrapper

    def wrappername(self, fieldset):
        """Assemble id for the widget wrapper element"""
        wrappername = '%s_%s_loader' % (fieldset[0], fieldset[1])
        return wrappername

    def linktable(self, field):
        """Get name of table referenced by this widget from the widget's 
        requires attribute."""

        if not isinstance(field.requires, list):
            requires = [field.requires]
        else:
            requires = field.requires
        linktable = requires[0].ktable

        return linktable

    def choose_val(self, val, wrappername):
        """
        Use value stored in session if changes to widget haven't been sent to
        db session val must be reset to None each time it is checked.
        """
        session = current.session

        if (wrappername in session) and (session[wrappername]):
            val = session[wrappername]
            print 'session value being used in module: %s' % val
            session[wrappername] = None
        else:
            print 'db value being used in module: %s' % val
            session[wrappername] = None
        return val

    def clean(self, value, multi):
        clean = value
        #remove problematic pipe characters or commas from the field value 
        #in case of list:reference fields
        if multi and isinstance(value, list):
            clean = '-'.join(map(str, value))
        return clean

    def restricted(self, restricted):
        """Isolate creation of this value so that it can be overridden in 
        child classes."""
        return None

    def create_widget(self):       
        
        """create either a single select widget or multiselect widget"""
        print '\nstarting create_widget()'
        if self.multi == 'basic':
            self.wrapper = [MultipleOptionsWidget.widget(self.field, self.value)]
        else:
            self.wrapper = [OptionsWidget.widget(self.field, self.clean_val)]
            print 'in create_widget, value ', self.clean_val

    def hidden_ajax_field(self, wrappername):
        """hidden input to help send unsaved changes via ajax so that they're 
        preserved through a widget refresh"""

        inputid = wrappername + '_input'
        i = INPUT(_id = inputid, _name = inputid, _type = 'hidden', _value = '')
        return i

    def refresher(self, wrappername, linktable, uargs, uvars):
        '''create link to refresh this widget via ajax. The widget is always 
        created, since its href attribute is used to pass several values 
        to the client-side javascripts. If the widget is instantiated with 
        the 'refresher' parameter set to False, then the link is hidden 
        via CSS.'''

        return '%s_refresh_trigger' % linktable
        #prepare to hide 'refresh' button via CSS if necessary
        rstyle = ''
        if self.refresher is False:
            rstyle = 'display:none'
        #URL to refresh widget via ajax
        comp_url = URL('plugin_ajaxselect', 'set_widget.load', 
                            args=uargs, vars=uvars)
        #create 'refresh' button
        refresh_a = A('r', _href=comp_url, _id=self.refresher_id(), 
                        _class='refresh_trigger', cid=wrappername, 
                        _style=rstyle)
        return refresh_a

    def adder(self, wrappername, linktable, uargs, uvars, form_name):
        '''Build link for adding a new entry to the linked table'''

        #create id for adder link
        add_id '%s_add_trigger' % linktable
        #URL to load form for linking table via ajax
        add_url = URL('plugin_ajaxselect', 'set_form_wrapper.load',
                           args=uargs, vars=uvars)
        #create 'add new' button to open form
        add_a = A('+', _href=add_url, _id=add_id, 
                    _class='add_trigger', cid=form_name)
        return add_a

    def dialog(self, form_name):      
        '''create hidden div to hold form (to be displayed via modal dialog, 
        dialog triggered in static/plugin_ajaxselect.js'''

        dialog = DIV('', _id = form_name)
        return dialog

    def taglist(self, value, linktable):
        """Build a list of selected widget options to be displayed as a 
        list of 'tags' below the widget."""
        print '\n starting models/plugin_ajaxselect add_tags'

        db = current.db

        tl = UL(_class='taglist')
        for v in self.value:
            the_row = db(db[linktable].id == v).select().first()
            f = db[linktable]._format % the_row
            tl.append(LI(f, _class='tag'))

        return tl

    def linklist(self, value, linktable, uargs, uvars):
        """Build a list of selected widget options to be displayed as a 
        list of 'tags' below the widget."""
        print '\n starting models/plugin_ajaxselect add_tags'

        db = current.db

        #create list to hold linked tags
        ll = UL(_class='taglist editlist')       
        #append the currently selected items to the list
        for v in value:       
            myrow = db(db[linktable].id == v).select().first()

            formatted = db[linktable]._format % the_row
            edit_trigger_id = '%s_editlist_trigger_%i' % (linktable, v)            
            linkargs = uargs[:] #slice for new obj so vals don't pile up
            linkargs.append(v)
           
            ll.append(LI(A(formatted, 
                            _href=URL('plugin_ajaxselect', 
                                        'set_form_wrapper.load', 
                                        args=linkargs, 
                                        vars=uvars),   
                            _id = edit_trigger_id,
                            _class = 'edit_trigger editlink tag', 
                            cid = form_name), 
                        _class = 'editlink tag'))
        #append an empty div to hold the modal form
        form_name = '%s_editlist_form' % linktable
        ll.append(DIV('', _id = form_name))

        return ll

    def classes(self):
        #classes for wrapper span to indicate filtering relationships
        c = 'plugin_ajaxselect '
        if self.restrictor and self.restrictor != None:
            c += '%s restrictor for_%s ' % (self.linktable, self.restrictor)
        if self.lister == 'simple':
            c += 'lister_simple '
        elif self.lister == 'editlinks':
            c += 'lister_editlinks '
        return c


class FilteredAjaxSelect(AjaxSelect):

    def restricted(self, restricted):
        """Override parent restricted() method to allow a defined parameter 
        with this name to take effect."""
        return restricted

    def create_widget(self, restricted):       
        
        """create either a single select widget or multiselect widget"""
        if self.multi == 'basic':
            self.wrapper = [MultipleOptionsWidget.widget(self.field, self.value)]
        else:
            self.wrapper = [FilteredOptionsWidget.widget(self.field, self.value, restricted)]
        #hidden input to help send unsaved changes via ajax so that they're 
        #preserved through a widget refresh
        inputid = self.wrappername + '_input'
        self.wrapper.append(INPUT(_id = inputid, _name = inputid, _type = 'hidden', _value = ''))    


class FilteredOptionsWidget(OptionsWidget):
    """
    Overrides the gluon.sqlhtml.OptionsWidget class to filter the list of options.

    The initial list of options comes via field.requires.options(). This furnishes 
    a list of tuples, each of which contains the id and format string for one option 
    from the referenced field.
    """

    @classmethod
    def widget(cls, field, value, restricted, **attributes):
        """
        generates a SELECT tag, including OPTIONs (only 1 option allowed)

        This method takes one argument more than OptionsWidget.widget. The restricted
        argument identifies the form field whose value constrains the values to be 
        included as available options for this widget. 

        see also: 
            :meth:`FormWidget.widget`
            :meth:`OptionsWidget.widget`
        """
        db = current.db

        default = dict(value=value)
        attr = cls._attributes(field, default, **attributes)

        # get raw list of options for this widget
        requires = field.requires
        if not isinstance(requires, (list, tuple)):
            requires = [requires]
        if requires:
            if hasattr(requires[0], 'options'):
                options = requires[0].options()
            else:
                raise SyntaxError, 'widget cannot determine options of %s' % field
        
        # get the table referenced by this field
        linktable = requires[0].ktable

        # get the value of the restricting field
        table = field.table
        filter_field = table[restricted]
        filter_val = db(field == value).select(filter_field).first()[filter_field] 
        print 'filter_field', filter_field
        print 'filter_val', filter_val

        # get the table referenced by the restricting field
        filter_req = filter_field.requires
        if not isinstance(filter_req, (list, tuple)):
            filter_req = [filter_req]        
        filter_linktable = filter_req[0].ktable        
        print 'filter_linktable', filter_linktable

        #find the linktable field that references filter_linktable
        ref = 'reference %s' % filter_linktable
        cf = [f for f in db[linktable].fields if db[linktable][f].type == ref][0]

        # filter raw list of options
        f_options = [o for o in options if db((db[linktable].id == o[0]) 
                                            & (db[linktable][cf] == filter_val)).select()]

        # build widget with filtered options
        opts = [OPTION(v, _value=k) for (k, v) in f_options]

        return SELECT(*opts, **attr)