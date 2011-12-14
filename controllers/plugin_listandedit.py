# coding: utf8
# try something like
def list():
    """
    API: Takes two required arguments. The first is the name of the table being listed, and the second is the id of the project.
    Takes one required variable in the URL request: a dictionary with at least one item with the index 'fields'. The value of request.vars[fields] provides the fields to be used to represent each record in the list.
    """
    response.files.append(URL('static', 'plugin_listandedit/plugin_listandedit.css'))
    response.files.append(URL('static', 'plugin_listandedit/plugin_listandedit.js'))

    tablename = request.args[0]
    fieldnames = request.vars['fields']

    rowlist = ''
    if not tablename in db.tables():
        response.flash = 'Sorry, you are trying to list entries from a table that does not exist in the database.'
    else:
        tb = db[tablename]
        rowlist = db().select(tb.id, tb.reference, db.works.title, db.authors.name)

    listset = []
    for r in rowlist:
        #FIXME: I need to get these values programmatically from vars['fields']
        listformat = r['authors'].name, ', ', r['works'].title, ', ', r[tablename].reference

        i = A(listformat, _href=URL('plugin_listandedit', 'edit.load', args=[tablename, r[tablename].id]), _class='plugin_listandedit_list', cid='viewpane')
        listset.append(i)

    return dict(listset = listset)

def edit():
    tablename = request.args[0]
    rowid = request.args[1]
    form = crud.update(db[tablename], rowid)

    return dict(form = form)
