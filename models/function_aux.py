#!-*- encoding:utf-8 -*-

def hide_record(table, record):
    db[table](record).update_record(is_active=False)
    db.commit()


def readable_signature(table, show=True):
    for field in ('created_by', 'created_on', 'modified_by', 'modified_on'):
        table[field].readable = True if show else False


def label_inscripto(row):
    persona = Persona._format % row.persona
    return SPAN('%s %s' % (row.persona.profesion.abreviatura, persona))


def memberships(*groups):
    for g in groups:
        if g in auth.user_groups.values():
            return True
    return False

### First Execution After of Install.
if not install:
    # add User Root
    if db(db.auth_user).isempty():
        root = db.auth_user.insert(first_name='root',
                                   last_name='colmenalabs',
                                   email='root@colmenalabs.com',
                                   password='1234qwer//'  # change after
                                )

    # add groups
    if db(db.auth_group).isempty():
        items = [{'role': 'administrador', 'description': 'Administación'},
                 {'role': 'cajero', 'description': 'Cajero'},
                 {'role': 'colaborador', 'description': 'Colaborador'}]
        db.auth_group.bulk_insert(items)
        db.auth_membership(user_id=root, group_id=1)

    # add profesion
    if db(Profesion).isempty():
        items = [{'nombre': 'Contador Público Nacional',
                  'abreviatura': 'CPN',
                  'created_on': request.now,
                  'modified_on': request.now,
                  'created_by': root,
                  'modified_by': root},
                 {'nombre': 'Licenciado en Administración',
                  'abreviatura': 'LIC',
                  'created_on': request.now,
                  'modified_on': request.now,
                  'created_by': root,
                  'modified_by': root},
                 {'nombre': 'Licenciado en Economía',
                  'abreviatura': 'LIC',
                  'created_on': request.now,
                  'modified_on': request.now,
                  'created_by': root,
                  'modified_by': root},
                 {'nombre': 'Otro',
                  'abreviatura': 'Sr/a',
                  'created_on': request.now,
                  'modified_on': request.now,
                  'created_by': root,
                  'modified_by': root}
                ]
        Profesion.bulk_insert(items)
