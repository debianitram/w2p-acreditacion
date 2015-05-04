# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################
response.logo = A(B('CPCEC Acreditación'),
                  _class="navbar-brand",_href="#",
                  _id="web2py-logo")
response.title = 'Acreditación'
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Martín Miranda - Adrian Marello'
response.meta.description = 'Sistema de Acreditación'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [(T('Inicio'), False, URL('default', 'index')),
	(T('Personas'), False, '#', [
        (T('Gestión Personas'), False, URL('persona', 'index', user_signature=True)),
        (T('Gestión Profesiones'), False, URL('persona', 'profesion', user_signature=True)),
    ]),
    (T('Cursos'), False, '#',[
        (T('Gestión Cursos'), False, URL('curso', 'index', user_signature=True)),
    	(T('Reportes'), False, URL('default', 'index', user_signature=True)),
    ])]

if auth.has_membership('administrador'):
    response.menu.append((T('Administración'),
                          False,
                          URL('default', 'admin', user_signature=True)
                        ))

if "auth" in locals(): auth.wikimenu() 
