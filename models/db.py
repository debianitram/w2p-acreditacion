# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.sender')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


## TABLES
Profesion = db.define_table('profesion',
                Field('nombre'),
                auth.signature,
                format='%(nombre)s'
                )

Persona = db.define_table('persona',
                Field('nombre'),
                Field('apellido'),
                Field('profesion', Profesion),
                Field('email'),
                Field('matricula'),
                Field('telefono'),
                Field('domicilio'),
                auth.signature,
                format='%(apellido)s, %(nombre)s',
                )

ProfesionPersona = db.define_table('profesion_persona',
                Field('profesion', Profesion),
                Field('persona', Persona),
                auth.signature
                )

Curso = db.define_table('curso',
                Field('titulo'),
                Field('fecha_inicio', 'datetime'),
                Field('fecha_fin', 'datetime'),
                Field('valor', 'decimal(8,2)', defaut=0.0),
                auth.signature,
                format='%(titulo)s'
                )

Inscripto = db.define_table('inscripto',
                Field('curso', Curso),
                Field('persona', Persona),
                Field('fecha_inscripcion', 'datetime'),
                Field('consultas_docente', 'text'),
                Field('sugerencia', 'text'),
                Field('index'),
                auth.signature,
                )

Pagos = db.define_table('pagos',
                Field('inscripto', Inscripto),
                Field('monto', 'decimal(8,2)'),
                Field('fecha', 'datetime'),
                auth.signature,
                )

Documentos = db.define_table('documentos',
                Field('curso', Curso),
                Field('nombre'),
                Field('documento', 'upload'),
                auth.signature,
                format='%(nombre)s'
                )


