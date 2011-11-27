@auth.requires_login()
def add():
    tablename = request.args[1]
    if not tablename in db.tables():
        response.flash = T('no table with that name in database')
    else:
        form = SQLFORM(db[tablename])
    #FIXME: Requires that first field of table (after id) be used as formatting label.
    fieldname = db[tablename].fields[1]

    if form.accepts(request.vars):
        response.flash = T("new %s added") %(tablename)
        target= request.args[0]
        #close the widget's dialog box
        response.js = '$( "#%s_dialog-form" ).dialog( "close" ); ' %(target)
        #update the options they can select their new category in the main form                
        response.js += """$("#%s").append("<option value='%s'>%s</option>");""" % (target, form.vars.id, form.vars[fieldname])
        #and select the one they just added
        response.js += """$("#%s").val("%s");""" % (target, form.vars.id)
        #finally, return a blank form incase for some reason they wanted to add another option
        return form
    elif form.errors:
        #silly user, just send back the form and it'll still be in our dialog box complete with error messages
        return form
    else:
        #hasn't been submitted yet, just give them the fresh blank form        
        return form
    return dict(form = form)
