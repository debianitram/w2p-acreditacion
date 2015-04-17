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
    fields = (Persona.nombre,
              Persona.apellido,
              Persona.dni,
              Persona.matricula
              )

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



def persona_ajax():
    query = str(request.vars.query)
    result = db(Persona.fsearch.lower().contains(query.lower()))
    if not result.isempty():
        return json([{'value': Persona._format % r.as_dict()} \
                    for r in result.select()])

def tab_inscripciones():
    persona = request.args(0, cast=int)
    query = ((Inscripto.persona == persona) & (Inscripto.docente != True))
    inscripciones = db(query).select()
    return dict(inscripciones=inscripciones)

def tab_pagos():
    persona = request.args(0, cast=int)
    query = ((Pagos.inscripto == Inscripto.id) & (Inscripto.persona == persona))
    pagos = db(query).select()
    return dict(pagos=pagos)