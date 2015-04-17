#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
from gluon.tools import prettydate
from gluon.storage import Storage
import curso_aux

@auth.requires_login()
def index():
    response.title = 'Administración'
    response.subtitle = 'Listado'
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
        readable_signature(Curso)
        f_cfecha = (CFecha.id, CFecha.fecha, CFecha.hora_inicio, CFecha.hora_fin)
        f_docente = (Inscripto.id, Inscripto.persona, Inscripto.docente)
        viewargs = dict(
            fecha = lambda c: Curso(c).cfecha.select(*f_cfecha, orderby=CFecha.fecha),
            docente = lambda c: Curso(c).inscripto.select(*f_docente).find(lambda r: r['docente'])
        )
        

    grid = SQLFORM.grid(Curso,
                        csv=False,
                        fields=fields,
                        viewargs=viewargs,
                        maxtextlength=200,
                        ondelete=hide_record,
                        oncreate=curso_aux.oncreate,
                        onupdate=curso_aux.oncreate,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Curso.created_on,
                        )

    return dict(grid=grid)



def tab_inscriptos():
    curso = request.args(0, cast=int)
    query = ((Inscripto.curso == curso) & (Inscripto.docente != True))
    inscriptos = db(query).select()
    return dict(inscriptos=inscriptos)


def tab_asistencias():
    curso = request.args(0, cast=int)
    query = ((Asistencia.inscripto == Inscripto.id) & (Inscripto.curso == curso))
    asistencias = db(query).select()
    return dict(asistencias=asistencias)


def add_docente():
    """ Add Docente from Ajax """
    print request.vars
    return ''


def add_fecha():
    """ Add Fecha from Ajax """
    curso = request.args(0, cast=int)
    dates = request.vars
    dates.update(curso=curso)

    result = CFecha.validate_and_insert(**dates)

    if not result.errors:
        return ''
    else:
        return "alert('%s');" % 'Errores al cargar la fecha'
    
    return ''


def delete_item():
    print(request.vars)
    return 'Ok'