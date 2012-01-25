# coding: utf8
if 0:
    from gluon import current
    from gluon.tools import Crud
    db, auth = current.db, current.auth
    crud = Crud(db)

@auth.requires_login()
def post():
    comment = db.plugin_comments_comment
    return dict(form=crud.create(comment),
        comments=db(comment).select())
