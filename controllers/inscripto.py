#!-*- encoding: utf-8 -*-

from gluon.serializers import json


@auth.requires_login()
def tabla_abonado(inscripto):
    inscripto = inscripto
    precio_curso = inscripto.curso.precio
    
    fields = (Pagos.created_on, Pagos.monto)
    pagos = inscripto.pagos.select(*fields, orderby=fields[0])

    table = TABLE(THEAD(TR(TH('fecha'), TH('monto'))), 
                  _class='table table-condensed')

    body = [TR(TD(i.created_on), TD('$ ', i.monto)) for i in pagos]

    abonado = sum([i.monto for i in pagos])
    saldo = abonado - precio_curso

    if saldo < 0:
        rsaldo = TD('- $ %.2f' % saldo, _class='alert-danger')
    else:
        rsaldo = TD('+ $ %.2f' % saldo, _class='alert-success')
    
    body.append(TR(TD(B('Total abonado'), _style='text-align:right'), 
                   TD('$ ', abonado)))
    body.append(TR(TD(B('Precio Curso'), _style='text-align:right'),
                   TD('$ ', precio_curso, _class='alert-warning')))
    body.append(TR(TD(B('Saldo'), _style='text-align:right'), rsaldo))
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
        if memberships('cajero', 'administrador'):
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
        if memberships('colaborador', 'administrador'):
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

    elif action == 'detalle-pagos':
        message = DIV('Detalle de pagos: %s' % nombre_persona)
        table = DIV(tabla_abonado(inscripto), _class='col-md-12')
        tag.append(message)
        tag.append(table)

    return json(dict(content=tag, btn=btnok))



@auth.requires_login()
def actions_process():
    hide_modal  = "$('.modal').modal('hide');"
    js = "$('*[data-target=%(target)s]').find('.%(action)s').html('%(result)s');"
    

    action, target = request.args
    model, id = target.split('-')
    inscripto = Inscripto(id)

    if action == 'abonar':
        if memberships('cajero', 'administrador'):

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
                # Deshabilitamos el botón de abonar
                js += "$('*[data-target=%(target)s]').find('*[data-action=%(action)s]')"
                js += ".attr('class', 'btn btn-default btn-xs disabled');"
                # Habilitamos el botón de acreditar
                js += "$('*[data-target=%(target)s]').find('*[data-action=acreditar]')"
                js += ".attr('class', 'btn btn-default btn-xs actions');"
                rt = CENTER('$ %s' % total, _class='alert-success')
            else:
                rt = CENTER('$ %s' % total, _class='alert-danger')

            span = SPAN(_class='actions',
                        _title='Ver detalle',
                        **{'_data-title': 'Detalle Pagos',
                           '_data-action': 'detalle-pagos'})
            span.append(rt)
            js = hide_modal + js
            js = js % {'target': target,
                       'action': action,
                       'result': span}

            response.flash = 'Ingreso un nuevo pago'
            return js

        else:
            return hide_modal + 'alert("No tiene permisos suficientes");'

    elif action == 'acreditar':
        if memberships('colaborador', 'administrador'):
            if not inscripto.pago:
                return hide_modal + 'alert("Debe abonar para ser acreditado");'
            
            inscripto.update_record(acreditado=True)
            js = hide_modal + js
            # Deshabilitamos el botón de acreditación
            js += "$('*[data-target=%(target)s]').find('*[data-action=%(action)s]')"
            js += ".attr('class', 'btn btn-default btn-xs disabled');"
            # Habilitamos el botón de imprimir
            js += "$('*[data-target=%(target)s]').find('*[data-action=imprimir]')"
            js += ".attr('class', 'btn btn-default btn-xs');"
            js = js % {'target': target,
                       'action': action,
                       'result': CENTER(
                                    SPAN(_class='glyphicon glyphicon-ok'),
                                    _class='alert-success')}

            response.flash = 'Inscripto acreditado'
            return js

        else:
            return hide_modal + 'alert("No tiene permisos suficientes");'
