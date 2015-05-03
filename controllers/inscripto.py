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



def actions():
    js  = "$('.modal').modal('hide');"
    js += "$('*[data-object=%(target)s]').find('.%(action)s').html('%(result)s');"
    js += "$('*[data-object=%(target)s]').find('*[data-action=%(action)s]')"
    js += ".attr('class', 'btn btn-default btn-xs disabled');"

    action, target = request.args
    model, id = target.split('-')

    if action == 'abonar':
        expresion = {'pago': True}
        js = js % {'target': target,
                   'action': action,
                   'result': CENTER(
                                SPAN(_class='glyphicon glyphicon-ok'),
                                _class='alert-success')}

    elif action == 'acreditar':
        expresion = {'acreditado': True}
        js = js % {'target': target,
                   'action': action,
                   'result': CENTER(
                                SPAN(_class='glyphicon glyphicon-ok'),
                                _class='alert-success')}

    if Inscripto(id).update_record(**expresion):
        return js
    else:
        return 'alert("Problemas al procesar la acción: %s");' % action