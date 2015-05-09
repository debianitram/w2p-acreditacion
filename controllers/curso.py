#!-*- encoding:utf-8 -*-
# Colmenalabs 2015
import csv

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
    Curso.created_on.represent = lambda v, r: SPAN(prettydate(v),
                                                   _title=v)
    # Readable&Writable
    Curso.created_on.readable = True

    # Pre Construct SQLFORM.grid
    if 'new' in request.args or 'edit' in request.args:
        response.subtitle = 'Nuevo' if 'new' in request.args else 'Edición'
        Curso.created_on.readable = False

    
    if 'view' in request.args:
        readable_signature(Curso)
        row = Curso(request.args(-1, cast=int))
        response.subtitle = 'Detalle > %s' % row.titulo
        
        f_cfecha = (CFecha.id, CFecha.fecha, CFecha.hora_inicio, CFecha.hora_fin)
        f_docente = (Inscripto.id, Inscripto.persona, Inscripto.docente)

        viewargs = dict(
            fecha = lambda: row.cfecha.select(*f_cfecha, orderby=CFecha.fecha),
            docente = lambda: row.inscripto.select(*f_docente).find(lambda r: r['docente'])
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

    # Post Construct SQLFORM.grid
    if 'view' in request.args:
        for i in grid.elements('.btn'):
            i.add_class('btn-xs btn-warning',)

    return dict(grid=grid)


def tab_inscriptos():
    curso = request.args(0, cast=int)

    query = ((Inscripto.curso == curso) & 
             (Inscripto.docente != True) & 
             (Persona.id == Inscripto.persona))

    fields = (Inscripto.id,
              Inscripto.persona,
              Inscripto.pago,
              Inscripto.acreditado,
              Inscripto.total_abonado
              )

    inscriptos = db(query).select(*fields, orderby=Inscripto.persona)

    return dict(inscriptos=inscriptos, curso=curso)


def tab_asistencias():
    curso = request.args(0, cast=int)
    query = ((Asistencia.inscripto == Inscripto.id) & (Inscripto.curso == curso))
    asistencias = db(query).select()
    return dict(asistencias=asistencias)


@auth.requires_membership('administrador')
def add_docente():
    """ Add Docente from Ajax """
    curso = request.args(0, cast=int)
    persona = request.vars.get('inscripto_docente')
    query = ((Inscripto.curso == curso) & (Inscripto.persona == persona))

    if db(query).isempty():
        inscripto = Storage()
        inscripto.pago = True
        inscripto.acreditado = True
        inscripto.docente = True
        inscripto.fecha_inscripcion = request.now
        inscripto.curso = curso
        inscripto.persona = persona
        inscripto.consultas_docente = '-'
        inscripto.sugerencia = '-'

        result = Inscripto.validate_and_insert(**inscripto)

    else:
        result = db(query).validate_and_update(docente=True)

    if result.errors:
        return "alert('Error al intentar cargar un docente: %s');" % result

    return ''


@auth.requires_membership('administrador')
def import_inscriptos():
    # Listo para las jornadas ...
    # Modificar para el sistema del Consejo
    response.view = 'curso/import_inscriptos.html'
    curso = Curso(request.args(0, cast=int))
    rows = []

    form = SQLFORM.factory(
            Field('csv_inscriptos',
                  'upload',
                  label='Archivo CSV',
                  uploadfolder='uploads/csv/'),
            formstyle='bootstrap3_stacked')


    if form.process().accepted:
        csvfile = request.vars.csv_inscriptos.file
        csvfile.seek(0)

        # jump_first_iteration = False

        for line in csv.DictReader(csvfile):
            persona = db(Persona.dni == line['inscripcion.dni']).select()

            if not persona:
                # Agregamos una nueva persona
                persona = Persona.validate_and_insert(
                    profesion=line['inscripcion.profesion'],
                    nombre_apellido='%(inscripcion.apellido)s, %(inscripcion.nombre)s' % line,
                    dni=line['inscripcion.dni'],
                    email=line['inscripcion.email'],
                    matricula=line['inscripcion.matricula'],
                    telefono=line['inscripcion.telefono'],
                    domicilio=line['consejo.nombre']
                )
                persona = [persona]
            
            if db((Inscripto.curso == curso) & (Inscripto.persona == persona[0].id)).isempty():
                inscripto = Inscripto.insert(curso=curso,
                                             persona=persona[0].id,
                                             fecha_inscripcion=request.now)

        session.flash = 'Se importó con éxitos!'
        csvfile.close()
        redirect(URL(c='curso',
                     f='index',
                     args=('view', 'curso', curso.id),
                     user_signature=True))

    return dict(form=form, curso=curso, rows=rows)


@auth.requires_membership('administrador')
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
                            modal_key=key,
                            lambda_js=curso_aux.js_append_inscripto)


    if request.ajax and not request.vars._ajax_add:
        inscriptos = request.vars.get('curso_inscripto', None)

        if inscriptos:
            if not isinstance(inscriptos, (list, tuple)):
                inscriptos = [inscriptos, ]
                
            for item in inscriptos:
                # Rechazamos una persona inscripta dos veces en el mismo curso.
                query  = Inscripto.curso == curso.id 
                query &= Inscripto.persona == int(item)
                if db(query).isempty():
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


@auth.requires_membership('administrador')
def add_fecha():
    """ Add Fecha from Ajax """
    curso = request.args(0, cast=int)
    dates = request.vars
    dates.update(curso=curso)

    result = CFecha.validate_and_insert(**dates)

    if result.errors:
        return "alert('%s');" % 'Errores al cargar la fecha'
    
    return ''


@auth.requires_membership('administrador')
def delete_item():
    target = request.vars.get('target')
    table, object_id = target.split('-')
    db[table](object_id).delete_record()

    return target
