# coding: utf8
from plugin_ajaxselect import AjaxSelect, FilteredAjaxSelect
import datetime
import string
from gluon import current
current.db = db
response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.css'))
response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.js'))

spacer = ', '

db.define_table('locations',
    Field('location', 'string'),
    format='%(location)s')

db.define_table('authors',
    Field('name', 'string', default='anonymous'),
    Field('location', db.locations),
    Field('lived', 'string'),
    format='%(name)s')
db.authors.location.widget = lambda field, value: AjaxSelect().widget(
                                                        field, value)

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
    Field('user', db.auth_user, default=auth.user_id),
    Field('author', db.authors),
    Field('work', db.works),
    Field('reference'),
    Field('excerpt', 'text'),
    Field('body', 'text'),
    Field('tags', 'list:reference db.tags'),
    Field('last_edited', 'datetime', default=datetime.datetime.utcnow(),
            writable=False),
    Field('created', 'datetime', default=datetime.datetime.utcnow(),
            writable=False),
    Field('project', db.projects),
    format=lambda row: '%s, %s, %s' % (row.author.name, row.work.title, row.reference))
db.notes.author.widget = lambda field, value: AjaxSelect().widget(
                                                field, value,
                                                refresher=True,
                                                restrictor='work')
db.notes.work.widget = lambda field, value: FilteredAjaxSelect().widget(
                                                field, value,
                                                refresher=True,
                                                restricted='author')
db.notes.tags.requires = IS_IN_DB(db, 'tags.id', db.tags._format,
                                    multiple = True)
db.notes.tags.widget = lambda field, value: AjaxSelect().widget(
                                                field, value,
                                                multi='basic',
                                                refresher=True,
                                                lister='editlinks')
db.notes.project.requires = IS_IN_DB(db, 'projects.id', db.projects._format,
                                        multiple=False)
