# -*- coding: utf-8 -*-

def index():
    return dict()


def user():
    return dict(form=auth())


@auth.requires_membership('administrador')
def admin():
    target = request.vars.get('target', 'actions')

    grid = None

    if target == 'users':
        title = 'Usuarios del Sistema'
        grid = SQLFORM.grid(db.auth_user.id > 1,
                            csv=False,
                            deletable=False)

    elif target == 'permission':
        title = 'Asignar Permisos a Usuarios'
        grid = SQLFORM.grid(db.auth_membership.user_id != 1,
                            csv=False)

    elif target == 'actions':
        title = 'Administración'
    else:
        session.flash = 'Intento ingresar a un área restringida'
        redirect(URL('index'))

    return dict(title=title, target=target, grid=grid)


@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()


