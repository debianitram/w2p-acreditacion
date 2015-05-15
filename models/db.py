# -*- coding: utf-8 -*-

import locale
from gluon.contrib.appconfig import AppConfig

# Config Locale
locale.setlocale(locale.LC_ALL, ('es_AR', 'UTF-8'))

## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)
install = True

db = DAL(myconf.take('db.uri'),
         pool_size=myconf.take('db.pool_size', cast=int),
         check_reserved=['all'],
         migrate=True
         )

response.generic_patterns = ['*'] if request.is_local else []

## Style Forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## Create all Tables for Auth
auth.define_tables(username=False, signature=False)

# Custom attributes of table.auth_user
db.auth_user._format = '%(last_name)s, %(first_name)s'
db.auth_membership.user_id.represent = lambda v, r: db.auth_user._format % r.user_id
db.auth_membership.group_id.represent = lambda v, r: r.group_id.role

## Configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.sender')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## Configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.create_user_groups = None


# Config String to Search for Field
PersonaSearch = '{nombre_apellido} {dni} {matricula} {domicilio}'

## Define Tables
Profesion = db.define_table('profesion',
                Field('nombre', length=100),
                Field('abreviatura', length=5),
                auth.signature,
                common_filter=lambda q: db.profesion.is_active == True,
                format='%(nombre)s',
                )


Persona = db.define_table('persona',
                Field('profesion', Profesion),
                Field('nombre_apellido', length=250),
                Field('dni', length=25, unique=True),
                Field('email', length=150),
                Field('matricula', length=100),
                Field('telefono', length=30),
                Field('domicilio', length=150),
                Field('fsearch',
                      compute=lambda r: PersonaSearch.format(**r.as_dict())),
                auth.signature,
                common_filter=lambda q: db.persona.is_active == True,
                format='%(nombre_apellido)s',
                )

Curso = db.define_table('curso',
                Field('titulo', length=200),
                Field('lugar', length=200),
                Field('precio', 'decimal(10,2)', default=0.0),
                auth.signature,
                common_filter=lambda q: db.curso.is_active == True,
                format='%(titulo)s'
                )


Inscripto = db.define_table('inscripto',
                Field('curso', Curso),
                Field('persona', Persona),
                Field('docente', 'boolean', default=False),
                Field('fecha_inscripcion', 'datetime'),
                Field('consultas_docente', 'text'),
                Field('sugerencia', 'text'),
                Field('acreditado', 'boolean', default=False),
                Field('pago', 'boolean', default=False),
                Field('total_abonado', 'decimal(8, 2)', default=0.0),
                auth.signature,
                format=lambda r: '%s> %s' % (r.curso.titulo, r.persona.nombre_apellido),
                )

Pagos = db.define_table('pagos',
                Field('inscripto', Inscripto),
                Field('monto', 'decimal(8,2)'),
                Field('nro_recibo', length=100, default="0" * 10),
                auth.signature
                )

Documentos = db.define_table('documentos',
                Field('curso', Curso),
                Field('nombre', length=150),
                Field('documento', 'upload'),
                auth.signature,
                format=lambda r: '%s> Archivo: %s' % (r.curso.titulo, r.nombre)
                )

CFecha = db.define_table('cfecha',
                Field('curso', Curso),
                Field('fecha', 'date', required=True),
                Field('hora_inicio', 'time', required=True),
                Field('hora_fin', 'time', required=True),
                auth.signature,
                format=lambda r: '%s> Fecha: %s' % (r.curso.titulo, r.fecha),
                )

Asistencia = db.define_table('asistencia',
                Field('cfecha', CFecha),
                Field('inscripto', Inscripto),
                auth.signature
                )






