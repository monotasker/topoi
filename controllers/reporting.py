

def list_by_tags():
    """
    Controller function to allow listing notes based on the tags they contain.
    """

    response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.css'))
    response.files.append(URL('static', 'plugin_ajaxselect/plugin_ajaxselect.js'))

    author_select = AjaxSelect(db.notes.author, 0,
                               refresher=True,
                               adder=False,
                               orderby='author',
                               lister='simple').widget()
    work_select = AjaxSelect(db.notes.work, 0,
                               refresher=True,
                               adder=False,
                               orderby='author',
                               lister='simple').widget()
    tags_select = AjaxSelect(db.notes.tags, 0,
                               refresher=True,
                               adder=False,
                               orderby='author',
                               lister='simple').widget()
    tags_x_select = AjaxSelect(db.notes.tags, 0,
                               refresher=True,
                               adder=False,
                               orderby='author',
                               lister='simple').widget()
    print tags_x_select[0][0]
    tags_x_select[0][0]['_name'] = 'tags_excluded'

    return {'author_select': author_select,
            'work_select': work_select,
            'tags_select': tags_select,
            'tags_x_select': tags_x_select}

def get_notes():
    """
    Fetch and return the note records requested.
    """
    author = request.vars['author'] if 'author' in request.vars.keys() else None
    work = request.vars['work'] if 'work' in request.vars.keys() else None
    tags = request.vars['tags'] if 'tags' in request.vars.keys() else None
    tags_excluded = request.vars['tags_excluded'] if 'tags_excluded' in request.vars.keys() else None
    with_excerpt = request.vars['with_excerpt'] if 'with_excerpt' in request.vars.keys() else None
    with_comments = request.vars['with_comments'] if 'with_comments' in request.vars.keys() else None

    notes = db(db.notes.id > 0).select();
    print len(notes)

    if author and author not in ['none', None]:
        author = [author] if isinstance(author, (int, str)) else author
        notes = notes.find(lambda row: row.author and str(row.author) in author)
    if work and work not in ['none', None]:
        work = [work] if isinstance(work, (int, str)) else work
        notes = notes.find(lambda row: row.work and str(row.work) in work)
    if tags and tags not in ['none', None]:
        tags = [tags] if isinstance(tags, (int, str)) else tags
        notes = notes.find(lambda row: row.tags and [t for t in row.tags
                                                     if str(t) in tags])
    if tags_excluded and tags_excluded not in ['none', None]:
        tags_excluded = [tags_excluded] \
            if isinstance(tags_excluded, (int, str)) else tags_excluded
        notes.exclude(lambda row: row.tags and [t for t in row.tags
                                                if str(t) in tags_excluded])
    if with_excerpt and with_excerpt not in ['false', None]:
        notes.exclude(lambda row: row.excerpt in [None, ''])
    if with_comments and with_comments not in ['false', None]:
        notes.exclude(lambda row: row.body in [None, ''])

    note_table = TABLE()
    note_table['_class'] = 'table'
    for n in notes:
        myrow = TR()
        myrow.append(TD(db.authors(n.author).short_name))
        myrow.append(TD(db.works(n.work).short_title))
        myrow.append(TD(n.excerpt))
        myrow.append(TD(n.body))
        note_table.append(myrow)

    note_display = CAT(SPAN(H4('{} notes selected'.format(len(notes)))), note_table)

    return note_display
