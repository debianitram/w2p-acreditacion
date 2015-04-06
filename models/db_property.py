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
Curso.titulo.requires = IS_NOT_EMPTY()
Curso.docente.requires = IS_IN_DB(db(Persona.docente==True),
                                  Persona,
                                  Persona._format)



