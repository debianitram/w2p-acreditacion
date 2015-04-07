#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
from gluon.tools import prettydate
import curso_aux

@auth.requires_login()
def index():
    response.title = 'Administración'
    response.subtitle = 'Grilla'
    createargs = viewargs = None

    ### Config Grid
    fields = (Curso.titulo, Curso.precio, Curso.created_on)
    # Represent Columns
    Curso.precio.represent = lambda v, r: SPAN('$ {:,.2f}'.format(v),
                                              _class='label label-success')
    Curso.created_on.represent = lambda v, r: SPAN(prettydate(v),
                                                   _title=v)
    # Readable&Writable
    Curso.created_on.readable = True

    if 'new' in request.args or 'edit' in request.args:
        response.subtitle = 'Nuevo' if 'new' in request.args else 'Edición'
        Curso.created_on.readable = False


    if 'view' in request.args:
        response.subtitle = 'Detalle'
        



    grid = SQLFORM.grid(Curso,
                        csv=False,
                        fields=fields,
                        maxtextlength=200,
                        ondelete=hide_record,
                        oncreate=curso_aux.oncreate,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Curso.created_on,
                        )

    return dict(grid=grid)