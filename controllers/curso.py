#!-*- encoding:utf-8 -*-
# Colmenalabs 2015

@auth.requires_login()
def index():
    response.title = 'Administración Curso'
    createargs = viewargs = None

    ### Config Grid
    fields = (Curso.titulo, Curso.docente, Curso.valor, Curso.created_on)
    # Represent Columns
    Curso.docente.represent = lambda v, r: SPAN(Persona._format % r['docente'])
    Curso.valor.represent = lambda v, r: SPAN('$ {:,.2f}'.format(v),
                                              _class='label label-success')
    # Readable&Writable
    Curso.created_on.readable = True

    grid = SQLFORM.grid(Curso,
                        csv=False,
                        fields=fields,
                        maxtextlength=200,
                        showbuttontext=False,
                        orderby=~Curso.created_on)

    return dict(grid=grid)