########### Readable/Writable ###########
# Inscripto
Inscripto.curso.writable = False

# Pagos
Pagos.inscripto.writable = False

# Documentos
Documentos.curso.writable = False

# CFecha
CFecha.curso.writable = False


########### Requires - Validators ###########
# Profesion
Profesion.nombre.requires = IS_NOT_EMPTY()

# Persona
Persona.nombre.requires = IS_NOT_EMPTY()
Persona.apellido.requires = IS_NOT_EMPTY()
Persona.email.requires = IS_EMAIL()

# Curso
Curso.titulo.requires = [IS_NOT_IN_DB(db, Curso.titulo)]

# CFecha
CFecha.curso.requires = IS_NOT_EMPTY()
CFecha.fecha.requires = IS_NOT_EMPTY()
CFecha.hora_inicio.requires = IS_NOT_EMPTY()
CFecha.hora_fin.requires = IS_NOT_EMPTY()



