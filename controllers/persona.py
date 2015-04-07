#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
from gluon.tools import prettydate


@auth.requires_login()
def index():
    response.title = 'Administración'
    response.subtitle = 'grilla'
    createargs = viewargs = None

    ### Config Grid
    fields = (Persona.nombre, Persona.apellido, Persona.dni, Persona.matricula, Persona.created_on)
    # Represent Columns
    Persona.created_on.represent = lambda v, r: SPAN(prettydate(v),
                                                   _title=v)
    # Readable&Writable
    Persona.created_on.readable = True

    grid = SQLFORM.grid(Persona,
                        csv=False,
                        fields=fields,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Persona.created_on,
                        )

    return dict(grid=grid)
