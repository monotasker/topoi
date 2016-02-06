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
    Field('name', 'string'),
    Field('short_name', 'string'),
    Field('location', 'list:reference db.locations'),
    Field('lived', 'string'),
    Field('genres', 'list:reference db.genres'),
    Field('notes', 'text'),
    format='%(name)s')

db.authors.location.requires = IS_EMPTY_OR(IS_IN_DB(db, 'locations.id', db.locations._format,
                                                        multiple=True))
db.authors.location.widget = lambda field, value: AjaxSelect(field, value,
                                                        multi='basic',
                                                        refresher=True,
                                                        lister='simple').widget()
db.authors.genres.requires = IS_EMPTY_OR(IS_IN_DB(db, 'genres.id', db.genres._format,
                                                        multiple=True))
db.authors.genres.widget = lambda field, value: AjaxSelect(field, value,
                                                        multi='basic',
                                                        refresher=True,
                                                        lister='simple').widget()

db.define_table('works',
    Field('title', 'string'),
    Field('short_title', 'string'),
    Field('author', 'reference authors'),
    Field('date_earliest'),
    Field('date_latest'),
    Field('date_likely'),
    Field('genre', 'list:reference db.genres'),
    Field('source'),
    Field('comments'),
    format=lambda row: '{}, {}'.format(db.authors[row.author].short_name,
                                           row.title))
db.works.genre.requires = IS_EMPTY_OR(IS_IN_DB(db, 'genres.id', db.genres._format))
db.works.genre.widget = lambda field, value: AjaxSelect(field, value,
                                                        refresher=True,
                                                        multi='basic',
                                                        lister='simple').widget()
db.works.author.widget = lambda field, value: AjaxSelect(field, value,
                                                        multi=False,
                                                        refresher=True,
                                                        lister=None).widget()

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
    Field('user', 'reference auth_user', default=auth.user_id),
    Field('author', 'reference authors'),
    Field('work', 'reference works'),
    Field('reference'),
    Field('excerpt', 'text'),
    Field('body', 'text'),
    Field('tags', 'list:reference db.tags'),
    Field('last_edited', 'datetime', default=datetime.datetime.utcnow(),
            writable=False),
    Field('created', 'datetime', default=datetime.datetime.utcnow(),
            writable=False),
    Field('project', 'reference projects'),
    format=lambda row: '{}, {}, {}'.format(db.authors[row.author].short_name,
                                           db.works[row.work].short_title,
                                           row.reference))

db.notes.author.widget = lambda field, value: AjaxSelect(
                                               field, value,
                                               refresher=True,
                                               multi=False,
                                               restrictor='work',
                                               lister=None,
                                               orderby='name').widget()

db.notes.work.widget = lambda field, value: FilteredAjaxSelect(
                                                field, value,
                                                refresher=True,
                                                lister=None,
                                                multi=False,
                                                restricted='author',
                                                orderby='title').widget()
db.notes.tags.requires = IS_EMPTY_OR(IS_IN_DB(db, 'tags.id', db.tags._format,
                                    multiple=True))
db.notes.tags.widget = lambda field, value: AjaxSelect(
                                                field, value,
                                                multi='basic',
                                                refresher=True,
                                                lister='simple',
                                                orderby='tagname').widget()
