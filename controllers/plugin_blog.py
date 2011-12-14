def front():
    arts = db(db.articles.id > 0).select(orderby = db.articles.created)
    return dict(articles = arts)

def articles():
    a_id = request.args[0]
    art = db(db.articles.id == a_id).select()
    title = art.title
    body = art.body
    tags = []
    for t in art.blog_tags:
        tname = db(db.blog_tags.id == t).select(db.blog_tags.tagname)
        tags.append(tname)
    return dict(title = title, body = body, tags = tags)

def new_post():
    form = crud.create(db.articles)
    return dict(form = form)

def edit_post():
    form = crud.update(db.articles)
    return dict(form = form)

def new_tag():
    form = crud.create(db.blog_tags)
    return dict(form = form)