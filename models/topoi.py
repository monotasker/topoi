# coding: utf8
from plugin_ajaxselect import AjaxSelect, FilteredAjaxSelect
import datetime
import string
from gluon import current
current.db = db
response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.css'))
response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.js'))
response.files.append(URL('static', 'plugin_listandedit/plugin_listandedit.css'))


spacer = ', '

db.define_table('locations',
    Field('location', 'string'),
    format='%(location)s')

db.define_table('genres',
    Field('name', 'string'),
    format='%(name)s')

db.define_table('authors',
    Field('name', 'string', default='anonymous'),
    Field('location', 'list:reference db.locations'),
    Field('lived', 'string'),
    Field('genres', 'list:reference db.genres'),
    Field('notes', 'text'),
    format='%(name)s')

db.authors.location.requires = IS_IN_DB(db, 'locations.id', db.locations._format,
                                                        multiple=True)
db.authors.location.widget = lambda field, value: AjaxSelect().widget(
                                                        field, value,
                                                        multi='basic',
                                                        refresher=True,
                                                        lister='editlinks')
db.authors.genres.requires = IS_IN_DB(db, 'genres.id', db.genres._format,
                                                        multiple=True)
db.authors.genres.widget = lambda field, value: AjaxSelect().widget(
                                                        field, value,
                                                        multi='basic',
                                                        refresher=True,
                                                        lister='editlinks')

db.define_table('works',
    Field('title', 'string'),
    Field('author', db.authors),
    Field('date_earliest'),
    Field('date_latest'),
    Field('date_likely'),
    Field('genre', 'list:reference db.genres'),
    Field('source'),
    Field('comments'),
    format='%(title)s')
db.works.genre.requires = IS_IN_DB(db, 'genres.id', db.genres._format)
db.works.genre.widget = lambda field, value: AjaxSelect().widget(
                                                field, value,
                                                refresher=True)

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
    format=lambda row: '{}, {}, {}'.format(row.author,
                                            row.work,
                                            row.reference))

db.notes.author.requires = IS_IN_DB(db, 'authors.id', db.works._format)
db.notes.author.widget = lambda field, value: AjaxSelect(
                                               field, value,
                                               refresher=True,
                                               multi='basic',
                                               lister='simple',
                                               orderby='name').widget()

db.notes.work.requires = IS_IN_DB(db, 'works.id', db.works._format)
db.notes.work.widget = lambda field, value: AjaxSelect(
                                                field, value,
                                                refresher=True,
                                                lister='simple',
                                                multi='basic',
                                                orderby='title').widget()
db.notes.tags.requires = IS_IN_DB(db, 'tags.id', db.tags._format,
                                    multiple=True)
db.notes.tags.widget = lambda field, value: AjaxSelect(
                                                field, value,
                                                multi='basic',
                                                refresher=True,
                                                lister='editlinks',
                                                orderby='tagname').widget()
db.notes.project.requires = IS_IN_DB(db, 'projects.id', db.projects._format,
                                        multiple=False)
