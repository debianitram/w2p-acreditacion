
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
Persona.nombre_apellido.requires = [IS_NOT_EMPTY(), IS_UPPER()]
Persona.dni.requires = IS_NOT_IN_DB(db, Persona.dni)
Persona.email.requires = IS_EMAIL()

# Curso
Curso.titulo.requires = [IS_NOT_IN_DB(db, Curso.titulo), IS_UPPER()]

# CFecha
CFecha.curso.requires = IS_NOT_EMPTY()
CFecha.fecha.requires = IS_NOT_EMPTY()
CFecha.hora_inicio.requires = IS_NOT_EMPTY()
CFecha.hora_fin.requires = IS_NOT_EMPTY()

# Pagos
Pagos.monto.requires = IS_NOT_EMPTY()


########### Requires - Validators ###########
# Persona
Persona.dni.label = 'DNI'

########### Represent ###########
# Curso
Curso.precio.represent = lambda v, r: SPAN('$ {:,.2f}'.format(v),
                                              _class='label label-success')

# Inscripto
Inscripto.curso.represent = lambda v, r: Curso._format % v
Inscripto.persona.represent = lambda v, r: Persona._format % v



########### Callback before/after where insert/update/delete #############
def pago_after_in(row, id):
    inscripto = Inscripto(row.inscripto)
    precio_curso = inscripto.curso.precio
    total_abonado = [i.monto for i in inscripto.pagos.select(Pagos.monto)]

    monto = sum(total_abonado) if total_abonado else row.monto
    expresion = {'total_abonado': monto}


    if precio_curso <= monto:
        expresion.update(pago=True)

    inscripto.update_record(**expresion)
    db.commit()

Pagos._after_insert.append(lambda row, id: pago_after_in(row, id))