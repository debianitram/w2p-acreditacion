#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
from gluon.tools import prettydate


@auth.requires_login()
def index():
    response.title = 'Administración'
    response.subtitle = 'Listado'
    createargs = viewargs = None

    ### Config Grid
    fields = (Persona.nombre,
              Persona.apellido,
              Persona.dni,
              Persona.matricula)

    if 'new' in request.args or 'edit' in request.args:
        response.subtitle = 'Nuevo' if 'new' in request.args else 'Edición'


    if 'view' in request.args:
        response.subtitle = 'Detalle'
        readable_signature(Persona)


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


def inscripto():
	grid2 = SQLFORM.grid(Inscripto,
                        csv=False,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Inscripto.created_on,
                        )
	return dict(grid2=grid2)
