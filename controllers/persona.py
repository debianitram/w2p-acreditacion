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

def pagos():
	grid3 = SQLFORM.grid(Pagos,
                        csv=False,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Pagos.created_on,
                        )
	return dict(grid3=grid3)

def asistencia():
	grid4 = SQLFORM.grid(Asistencia,
                        csv=False,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Asistencia.created_on,
                        )
	return dict(grid4=grid4)