#!-*- encoding: utf-8 -*-

import StringIO
from os import path
from xhtml2pdf.pisa import CreatePDF

from curso_aux import date_reportcert, time_reportcert


@auth.requires(memberships('colaborador', 'administrador'))
def certificados():
    response.view = 'reports/certificado.html'

    curso = Curso(request.args(0, cast=int))
    fechas = curso.cfecha.select(CFecha.fecha,
                                 CFecha.hora_inicio,
                                 CFecha.hora_fin)

    text_date = date_reportcert(fechas)
    text_hours_count = time_reportcert(fechas)
    
    if 'all' in request.args:
        inscriptos = curso.inscripto.select(
            Inscripto.persona,
            Inscripto.docente,
            Inscripto.acreditado
        ).find(lambda r: r['acreditado'])
    else:
        inscriptos = curso.inscripto(Inscripto.id == request.args(-1)).select()
        if not inscriptos.first()['acreditado']:
            response.flash = 'Necesita acreditarlo para poder imprimir el certificado'
            redirect(URL(c='curso',
                         f='index',
                         extension='html',
                         args=('view', Curso._tablename, curso.id),
                         user_signature=True))


    context = dict(curso=curso,
                   inscriptos=inscriptos,
                   text_date=text_date,
                   count_hours=text_hours_count)

    if request.extension == 'pdf':
        path_css = path.join(request.env.web2py_path,
                                'applications/init/static/css/reporte_cert.css')
        
        with open(path_css, 'r') as rcss:
            css = rcss.read()

        html = response.render(response.view, context)
        doc = StringIO.StringIO()
        pdf = CreatePDF(html,
                        dest=doc,
                        default_css=css,
                        encoding='utf-8')
        return doc.getvalue()


@auth.requires_membership('administrador')
def asistencias():
    response.view = 'reports/asistencias.html'

    curso = Curso(request.args(0, cast=int))
    fechas = curso.cfecha.select(CFecha.fecha,
                                 CFecha.hora_inicio,
                                 CFecha.hora_fin)
    row_inscriptos = curso.inscripto.select(Inscripto.persona, Inscripto.docente)
    docentes = row_inscriptos.find(lambda r: r['docente'])
    inscriptos = row_inscriptos.find(lambda r: not r['docente'])

    context = dict(curso=curso,
                   fechas=fechas,
                   docentes=docentes,
                   inscriptos=inscriptos)

    if request.extension == 'pdf':
        path_static = path.join(request.env.web2py_path,
                                'applications/init/static')
        
        with open(path.join(path_static, 'css/reporte_asist.css'), 'r') as rcss:
            css = rcss.read()

        html = response.render(response.view, context)
        doc = StringIO.StringIO()
        pdf = CreatePDF(html,
                        dest=doc,
                        path=path.join(path_static, 'images'),
                        default_css=css,
                        encoding='utf-8')
        return doc.getvalue()


@auth.requires_membership('administrador')
def inscriptos_acreditados():
    response.view = 'reports/inscriptos_acreditados.html'
    curso = Curso(request.args(-1, cast=int))
    fields = (Inscripto.id,
              Inscripto.pago,
              Inscripto.acreditado,
              Inscripto.total_abonado,
              Persona.dni,
              Persona.domicilio,
              Persona.nombre_apellido)

    query = (Inscripto.curso == curso.id)

    rows = db(query).select(*fields,
                            left=Inscripto.on(Inscripto.persona == Persona.id))

    rows_groups = rows.group_by_value(Persona.domicilio)

    context =  dict(curso=curso, rows_groups=rows_groups)

    if request.extension == 'pdf':
        path_static = path.join(request.env.web2py_path,
                                'applications/init/static')
        
        with open(path.join(path_static, 'css/reporte_asist.css'), 'r') as rcss:
            css = rcss.read()

        html = response.render(response.view, context)
        doc = StringIO.StringIO()
        pdf = CreatePDF(html,
                        dest=doc,
                        path=path.join(path_static, 'images'),
                        default_css=css,
                        encoding='utf-8')
        return doc.getvalue()
    return context