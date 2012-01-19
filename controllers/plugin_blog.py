def front():
    arts = db(db.articles.id > 0).select(orderby = db.articles.created)
    return dict(articles = arts)

def articles():
    the_id = request.args[0]
    art = db(db.articles.id == the_id).select()
    a = art[0]
    created = a.created.strftime('%B %e, %Y')
    return dict(a = a, created = created)

@auth
def new_post():
    form = crud.create(db.articles)
    return dict(form = form)

def edit_post():
    form = crud.update(db.articles)
    return dict(form = form)

def new_tag():
    form = crud.create(db.blog_tags)
    return dict(form = form)
