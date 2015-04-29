#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
from gluon.tools import prettydate
from gluon.storage import Storage

from web2py_modal import modal_reference
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

    if 'view' in request.args:
        for i in grid.elements('.btn'):
            i.add_class('btn-xs btn-warning',)

    return dict(grid=grid)


def tab_inscriptos():
    # Represent
    Inscripto.persona.represent = lambda r, v: SPAN('Saludos')
    
    curso = request.args(0, cast=int)
    query = ((Inscripto.curso == curso) & (Inscripto.docente != True) & (Persona.id == Inscripto.persona))
    # Fields
    fields = (Inscripto.id,
              Inscripto.persona,
              Inscripto.pago,
              Inscripto.acreditado
              )

    inscriptos = db(query).select(*fields)

    return dict(inscriptos=inscriptos, curso=curso)


def tab_asistencias():
    curso = request.args(0, cast=int)
    query = ((Asistencia.inscripto == Inscripto.id) & (Inscripto.curso == curso))
    asistencias = db(query).select()
    return dict(asistencias=asistencias)


def add_docente():
    """ Add Docente from Ajax """
    inscripto = Storage()
    inscripto.pago = True
    inscripto.acreditado = True
    inscripto.docente = True
    inscripto.fecha_inscripcion = request.now
    inscripto.curso = request.args(0, cast=int)
    inscripto.persona = request.vars.get('inscripto_docente')
    inscripto.consultas_docente = '-'
    inscripto.sugerencia = '-'
    result = Inscripto.validate_and_insert(**inscripto)

    # Próxima versión: Comprobar la persona no está inscripta en el curso.

    if result.errors:
        return "alert('%s');" % 'Error al intentar cargar un docente'

    return ''


def import_inscriptos():
    response.view = 'curso/import_inscriptos.html'
    curso = Curso(request.args(0, cast=int))

    form = SQLFORM.factory(
            Field('csv_inscriptos',
                  'upload',
                  label='Archivo CSV',
                  uploadfolder='uploads/csv/'),
            formstyle='bootstrap3_stacked')


    if form.process().accepted:
        csvfile = request.vars.csv_inscriptos.file
        print type(csvfile)
        csvfile.seek(0)
        print csvfile.read()


    return dict(form=form, curso=curso)


def add_inscriptos():
    response.view = 'curso/add_inscriptos.html'
    curso = Curso(request.args(0, cast=int))

    key = str(Inscripto.persona).replace('.', '_')
    modal = modal_reference(Inscripto.persona,
                            btn_title='Añadir Persona',
                            btn_icon='glyphicon glyphicon-plus-sign',
                            btn_name='Nueva Persona',
                            btn_class='btn btn-default btn-xs',
                            modal_title='Nueva Persona',
                            modal_key=key)


    if request.ajax and not request.vars._ajax_add:
        inscriptos = request.vars.get('curso_inscripto', None)

        if inscriptos:
            if not isinstance(inscriptos, (list, tuple)):
                inscriptos = [inscriptos, ]
                
            for count, item in enumerate(inscriptos):
                # Evitamos dos inscriptos iguales.
                if item not in inscriptos[count + 1:]:
                    Inscripto.validate_and_insert(curso=curso.id,
                                                  persona=int(item),
                                                  fecha_inscripcion=request.now)

            redirect(URL(c='curso',
                         f='index',
                         args=('view', Curso._tablename, curso.id),
                         user_signature=True),
                    client_side=True)
        else:
            return 'alert("Inscriba una persona al curso");'

    return dict(curso=curso, modal=modal)


def add_fecha():
    """ Add Fecha from Ajax """
    curso = request.args(0, cast=int)
    dates = request.vars
    dates.update(curso=curso)

    result = CFecha.validate_and_insert(**dates)

    if result.errors:
        return "alert('%s');" % 'Errores al cargar la fecha'
    
    return ''


def delete_item():
    target = request.vars.get('target')
    table, object_id = target.split('-')
    db[table](object_id).delete_record()

    return target
