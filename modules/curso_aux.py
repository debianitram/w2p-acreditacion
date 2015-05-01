#!-*- encoding: utf-8 -*-

# Colmena Labs - Catamarca - Argentina
# debianitram (at) gmail.com

from gluon import current
from gluon.html import A, URL
from gluon.http import redirect


Curso = current.globalenv.get('Curso')

def oncreate(form):
    redirect(URL(args=('view', Curso._tablename, form.vars.id),
                 user_signature=True))


def js_append_inscripto(form):
    """ Append new inscripto """
    item = """<li class="list-group-item" id="inscripto-%(id)s">
                <a class="btn btn-xs remove-item-nodb">
                    <span class="glyphicon glyphicon-minus-sign"></span>
                </a>
                <input type="hidden" name="curso_inscripto", value="%(id)s">
                %(nombre_apellido)s
            </li>
        """ % form.vars

    return "$('.list-group').append('%s');" % item