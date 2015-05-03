#!-*- encoding: utf-8 -*-

from decimal import Decimal


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
def actions():
    hide_modal  = "$('.modal').modal('hide');"
    js = "$('*[data-object=%(target)s]').find('.%(action)s').html('%(result)s');"
    js += "$('*[data-object=%(target)s]').find('*[data-action=%(action)s]')"
    js += ".attr('class', 'btn btn-default btn-xs disabled');"

    action, target = request.args
    model, id = target.split('-')
    row_inscripto = Inscripto(id)

    print request.vars

    if action == 'abonar':
        if auth.has_membership('cajero') or auth.has_membership('administrador'):
            expresion = {'pago': True}
            expresion_pago = {'inscripto': row_inscripto.id,
                              'monto': request.vars.monto,
                              'nro_recibo': request.vars.nro_recibo}

            # Agregamos Pago para inscripto.
            result = Pagos.validate_and_insert(**expresion_pago)
            
            if result.errors:
                return hide_modal + 'alert("Errors al acreditar %s");' % result.errors

            js = hide_modal + js
            js = js % {'target': target,
                       'action': action,
                       'result': CENTER(
                                    SPAN(_class='glyphicon glyphicon-ok'),
                                    _class='alert-success')}
        else:
            return hide_modal + 'alert("No tiene permisos suficientes");'

    elif action == 'acreditar':
        if auth.has_membership('colaborador') or auth.has_membership('administrador'):
            
            if not row_inscripto.pago:
                return hide_modal + 'alert("Debe abonar para ser acreditado");'
            
            expresion = {'acreditado': True}
            js = hide_modal + js
            js = js % {'target': target,
                       'action': action,
                       'result': CENTER(
                                    SPAN(_class='glyphicon glyphicon-ok'),
                                    _class='alert-success')}
        else:
            return hide_modal + 'alert("No tiene permisos suficientes");'

    if row_inscripto.update_record(**expresion):
        response.flash = 'Se aplicaron los cambios'
        return js

    else:
        return 'alert("Problemas al procesar la acción: %s");' % action