#!-*- encoding: utf-8 -*-

from decimal import Decimal

from gluon.serializers import json

from curso_aux import date_reportcert, time_reportcert


@auth.requires_login()
def index():
    response.title = 'Administración'
    response.subtitle = 'Listado'
    createargs = viewargs = None

    ### Config Grid
    fields = (Inscripto.persona,
               Inscripto.curso,
               Inscripto.fecha_inscripcion,
               Inscripto.finalizo,
               Inscripto.pago)

    if 'new' in request.args or 'edit' in request.args:
        response.subtitle = 'Nuevo' if 'new' in request.args else 'Edición'


    if 'view' in request.args:
        response.subtitle = 'Detalle'
        readable_signature(Persona)

    Inscripto.persona.represent = lambda value, row: Persona._format % value

    grid = SQLFORM.grid(Inscripto,
                        csv=False,
                        fields=fields,
                        maxtextlength=200,
                        ondelete=hide_record,
                        user_signature=True,
                        showbuttontext=False,
                        orderby=~Inscripto.created_on,
                        )

    return dict(grid=grid)


@auth.requires_login()
def tabla_abonado(inscripto):
    inscripto = inscripto
    table = TABLE(THEAD(TR(TH('fecha'), TH('monto'))),
                  _class='table table-condensed')
    fields = (Pagos.created_on, Pagos.monto)
    pagos = inscripto.pagos.select(*fields, orderby=fields[0])

    body = [TR(TD(i.created_on), TD('$ ', i.monto)) for i in pagos]
    table.append(TBODY(*body))

    return table


def actions_view():
    action, target = request.args
    model, id = target.split('-')

    inscripto = Inscripto(id)
    nombre_persona = Persona._format % inscripto.persona
    tag = TAG['']()
    btnok = ''

    if action == 'abonar':
        if auth.has_membership('cajero') or auth.has_membership('administrador'):
            message = DIV('Realizar pago de: %s' % nombre_persona, _class='col-md-12')
            form = DIV(
                DIV(
                    DIV(LABEL("Monto $", _class='form-label'),
                        INPUT(_class='form-control',
                              _type='number',
                              _name='monto'),
                    _class='form-group'),
                    DIV(LABEL("Nro Recibo", _class='form-label'),
                        INPUT(_class='form-control',
                              _type='text',
                              _name='nro_recibo'),
                    _class='form-group'),
                    DIV(LABEL('Permitir sin finalizar pago',
                             _class='form-label'),
                        INPUT(_type='checkbox', _name='pago'),
                    _class='form-group'),
                _class='form-horizontal'),
            _class='col-md-4')
            
            table = DIV(tabla_abonado(inscripto), _class='col-md-8')
            tag.append(message)
            tag.append(table)
            tag.append(form)

            ajax = "ajax('%s', ['monto', 'nro_recibo', 'pago'], ':eval');"
            ajax = ajax % URL(c='inscripto',
                              f='actions_process',
                              args=('abonar', target),
                              user_signature=True)
            btnok = A('abonar', _class='btn btn-primary', _onclick=ajax)
        else:
            tag = DIV('No tiene permisos suficientes', _class='alert alert-danger')
            

    elif action == 'acreditar':
        if auth.has_membership('colaborador') or auth.has_membership('administrador'):
            message = DIV('Desea acreditar a: %s' % nombre_persona,
                          _class='col-md-12')
            ajax = "ajax('%s', [], ':eval');"
            ajax = ajax % URL(c='inscripto',
                              f='actions_process',
                              args=('acreditar', target),
                              user_signature=True)
            btnok = A('acreditar', _class='btn btn-primary', _onclick=ajax)

            tag.append(message)

        else:
            tag = DIV('No tiene permisos suficientes', _class='alert alert-danger')

    return json(dict(content=tag, btn=btnok))



@auth.requires_login()
def actions_process():
    hide_modal  = "$('.modal').modal('hide');"
    js = "$('*[data-target=%(target)s]').find('.%(action)s').html('%(result)s');"
    

    action, target = request.args
    model, id = target.split('-')
    inscripto = Inscripto(id)

    if action == 'abonar':
        if auth.has_membership('cajero') or auth.has_membership('administrador'):

            if request.vars.pago:
                inscripto.update_record(pago=True)

            expresion = {'inscripto': inscripto.id,
                         'monto': request.vars.monto,
                         'nro_recibo': request.vars.nro_recibo}

            # Agregamos Pago para inscripto
            result = Pagos.validate_and_insert(**expresion)

            if result.errors:
                return hide_modal + 'alert("Errors al abonar %s");' % result.errors

            total = sum([i.monto for i in inscripto.pagos.select(Pagos.monto)])
            
            if inscripto.pago:
                js += "$('*[data-target=%(target)s]').find('*[data-action=%(action)s]')"
                js += ".attr('class', 'btn btn-default btn-xs disabled');"
                span = CENTER(SPAN('$ ', total), _class='alert-success')
            else:
                span = CENTER(SPAN('$ ', total), _class='alert-danger')

            js = hide_modal + js
            js = js % {'target': target,
                       'action': action,
                       'result': span}

            response.flash = 'Ingreso un nuevo pago'
            return js

        else:
            return hide_modal + 'alert("No tiene permisos suficientes");'

    elif action == 'acreditar':
        if auth.has_membership('colaborador') or auth.has_membership('administrador'):
            if not inscripto.pago:
                return hide_modal + 'alert("Debe abonar para ser acreditado");'
            
            inscripto.update_record(acreditado=True)
            js = hide_modal + js
            js = js % {'target': target,
                       'action': action,
                       'result': CENTER(
                                    SPAN(_class='glyphicon glyphicon-ok'),
                                    _class='alert-success')}

            response.flash = 'Inscripto acreditado'
            return js

        else:
            return hide_modal + 'alert("No tiene permisos suficientes");'




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
        import os
        import StringIO
        from xhtml2pdf.pisa import CreatePDF

        path_css = os.path.join(request.env.web2py_path,
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
    return context
