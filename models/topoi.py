# coding: utf8
from plugin_selectoradd import SELECT_OR_ADD_OPTION
from plugin_multiselect_widget import hmultiselect_widget, vmultiselect_widget
import datetime

add_option = SELECT_OR_ADD_OPTION(form_title="Add new", controller="plugin_selectoradd", function="add", button_text = "Add New", dialog_width=500)

db.define_table('locations',
    Field('location', 'string'),
    format='%(location)s')

db.define_table('authors', 
    Field('name', 'string', default='anonymous'),
    Field('location', db.locations),
    Field('lived', 'string'), 
    format='%(name)s')
db.authors.location.widget = add_option.widget 
        
db.define_table('works',
    Field('title', 'string'),
    Field('author', db.authors),
    Field('date_earliest'),
    Field('date_latest'),
    Field('date_likely'),
    Field('genre'),
    Field('source'),
    Field('comments'),
    format='%(title)s')

db.define_table('projects',
    Field('projectname', 'string'),
    Field('owner', db.auth_user, default=auth.user_id),
    Field('description', 'text'),
    format='%(projectname)s')

db.define_table('tags',
    Field('tagname', 'string'),
    Field('creator', db.auth_user, default=auth.user_id),
    Field('project', db.projects),
    format='%(tagname)s')
    
db.define_table('notes',
    Field('label', 'string'),
    Field('user', db.auth_user, default=auth.user_id),
    Field('author', db.authors),
    Field('work', db.works),
    Field('reference'),
    Field('excerpt'),
    Field('body', 'text'),
    Field('tags', 'list:reference db.tags'),
    Field('last_edited', 'datetime', default=datetime.datetime.utcnow()),
    Field('project', db.projects),
    format='%(label)s')
#Initialize the add-or-select widget
db.notes.author.widget = add_option.widget
db.notes.work.widget = add_option.widget
db.notes.tags.requires = IS_IN_DB(db, 'tags.id', db.tags._format, multiple = True)
db.notes.tags.widget = hmultiselect_widget
db.notes.project.widget = add_option.widget
