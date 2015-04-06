# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B(request.controller.title()),
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

response.menu = []

if "auth" in locals(): auth.wikimenu() 
