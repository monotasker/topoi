# coding: utf8
# try something like
def list(): 
    response.files.append(URL('static', 'plugin_listandedit/plugin_listandedit.css'))
    response.files.append(URL('static', 'plugin_listandedit/plugin_listandedit.js'))
    #settings    
    displayfield = ''
    
    tablename = request.args[0]
    #FIXME: Hack here to solve problem of field name not being identical to table name
    tablename = tablename + 's'
    
    fieldname = db[tablename].fields[1]    
    print tablename
        
    rowlist = ''    
    if not tablename in db.tables():
        response.flash = 'error'
    else:
        tb = db[tablename]
        rowlist = db(tb).select()
    
    listset = []
    for r in rowlist:
        i = A(r[fieldname], _href=URL('plugin_listandedit', 'edit.load', args=[tablename, r.id]), _class='plugin_listandedit_list', cid='viewpane')    
        listset.append(i)
                
    return dict(listset = listset)

def edit():
    tablename = request.args[0]
    rowid = request.args[1]
    form = crud.update(db[tablename], rowid)
    
    return dict(form = form)
