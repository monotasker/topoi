if 0:
    #from gluon import current, SQLFORM, redirect, A, URL
    from gluon.tools import Auth, Crud
    from gluon.dal import DAL
    db = DAL()
    auth = Auth()
    crud = Crud()

@auth.requires_login()
def post():
    comment = db.plugin_comments_comment
    return dict(form=crud.create(comment),
        comments=db(comment).select())
