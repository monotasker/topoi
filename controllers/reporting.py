

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

    return {'author_select': author_select,
            'work_select': work_select,
            'tags_select': tags_select}

def get_notes():
    """
    Fetch and return the note records requested.
    """
    print 'gotcha!'
