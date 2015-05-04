#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
from gluon.tools import prettydate
from gluon.serializers import json

@auth.requires_login()
def index():
    response.title = 'Administración'
    response.subtitle = 'Listado'
    createargs = viewargs = None

    ### Config Grid
    fields = (Persona.nombre_apellido, Persona.dni, Persona.matricula)

    if 'new' in request.args or 'edit' in request.args:
        response.subtitle = 'Nuevo' if 'new' in request.args else 'Edición'


    if 'view' in request.args:
        readable_signature(Persona)
        row = Persona(request.args(-1, cast=int))
        response.subtitle = 'Detalle > %s' % row.nombre_apellido


    grid = SQLFORM.grid(Persona,
                        csv=False,
                        fields=fields,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=Persona.nombre_apellido,
                        )

    if 'view' in request.args:
        for i in grid.elements('.btn'):
            i.add_class('btn-xs btn-warning',)

    return dict(grid=grid)



@auth.requires_login()
def profesion():
    response.title = 'Administración'
    response.subtitle = 'grilla'
    createargs = viewargs = None

    ### Config Grid
    fields = (Profesion.nombre, Profesion.created_on)
    # Represent Columns
    Profesion.created_on.represent = lambda v, r: SPAN(prettydate(v),
                                                   _title=v)
    # Readable&Writable
    Profesion.created_on.readable = True

    grid = SQLFORM.grid(Profesion,
                        csv=False,
                        fields=fields,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Profesion.created_on,
                        )

    return dict(grid=grid)


def persona_ajax():
    query = str(request.vars.query)
    result = db(Persona.fsearch.lower().contains(query.lower()))
    if not result.isempty():
        return json([{'id': r.id, 'value': Persona._format % r.as_dict()} \
                    for r in result.select()])
    else:
        return json([{'id': '',
                      'value': '<span style="color:red">Sin resultados</span>'}])


@auth.requires_login()
def tab_inscripciones():
    persona = request.args(0, cast=int)
    inscripciones = db(Inscripto.persona == persona).select()
    return dict(inscripciones=inscripciones)


@auth.requires_login()
def tab_pagos():
    persona = request.args(0, cast=int)
    query = ((Pagos.inscripto == Inscripto.id) & (Inscripto.persona == persona))
    pagos = db(query).select()
    return dict(pagos=pagos)


@auth.requires_login()
def tab_asistencias():
    persona = request.args(0, cast=int)
    query = ((Asistencia.inscripto == Inscripto.id) & (Inscripto.persona == persona))
    asistencias = db(query).select()
    return dict(asistencias=asistencias)