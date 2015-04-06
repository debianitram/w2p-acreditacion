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

## by default give a view/generic.extension hhto all actions from localhost
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
                Field('abreviatura', length=5),
                auth.signature,
                common_filter=lambda q: db.profesion.is_active == True,
                format='%(nombre)s'
                )


Persona = db.define_table('persona',
                Field('nombre', length=50),
                Field('apellido', length=50),
                Field('profesion', Profesion),
                Field('docente', 'boolean'),
                Field('dni', length=30),
                Field('email', length=100),
                Field('matricula', length=15),
                Field('telefono', length=30),
                Field('domicilio', length=150),
                auth.signature,
                common_filter=lambda q: db.persona.is_active == True,
                format='%(apellido)s, %(nombre)s',
                )

ProfesionPersona = db.define_table('profesion_persona',
                Field('profesion', Profesion),
                Field('persona', Persona),
                auth.signature,
                common_filter=lambda q: db.profesion_persona.is_active == True,
                format=lambda r: '%s: %s' % (r.profesion.abreviatura, r.persona.apellido),
                )

Curso = db.define_table('curso',
                Field('titulo', length=200),
                Field('lugar', length=200),
                Field('docente', Persona),
                Field('valor', 'decimal(8,2)', default=0.0),
                auth.signature,
                common_filter=lambda q: db.curso.is_active == True,
                format='%(titulo)s'
                )

Inscripto = db.define_table('inscripto',
                Field('curso', Curso),
                Field('persona', Persona),
                Field('fecha_inscripcion', 'datetime'),
                Field('consultas_docente', 'text'),
                Field('sugerencia', 'text'),
                Field('curso_persona'),
                Field('pago', 'boolean'),
                auth.signature,
                format=lambda r: '%s: %s' % (r.curso.titulo, r.persona.apellido),
                )

Pagos = db.define_table('pagos',
                Field('inscripto', Inscripto),
                Field('monto', 'decimal(8,2)', default=0.0),
                Field('fecha', 'datetime', default=request.now),
                auth.signature,
                )

Documentos = db.define_table('documentos',
                Field('curso', Curso),
                Field('nombre', length=150),
                Field('documento', 'upload'),
                auth.signature,
                format='%(nombre)s'
                )

CFecha = db.define_table('cfecha',
                Field('curso', Curso),
                Field('fecha', 'date'),
                Field('hora_inicio', 'time'),
                Field('hora_fin', 'time'),
                auth.signature,
                )

Asistencia = db.define_table('asistencia',
                Field('cfecha', CFecha),
                Field('inscripto', Inscripto),
                auth.signature,
                )






