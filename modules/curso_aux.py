#!-*- encoding: utf-8 -*-

# Colmena Labs - Catamarca - Argentina
# debianitram (at) gmail.com
from datetime import datetime, timedelta

from gluon import current
from gluon.html import A, URL
from gluon.http import redirect


Curso = current.globalenv.get('Curso')
Inscripto = current.globalenv.get('Inscripto')
Pagos = current.globalenv.get('Pagos')
db = current.globalenv.get('db')


def oncreate(form):
    redirect(URL(args=('view', Curso._tablename, form.vars.id),
                 user_signature=True))


def js_append_inscripto(form):
    """ Append new inscripto """
    item = """<li class="list-group-item" data-target="inscripto-%(id)s" data-db="false">
                <a class="btn btn-xs remove-item">
                    <span class="glyphicon glyphicon-minus-sign"></span>
                </a>
                <input type="hidden" name="curso_inscripto", value="%(id)s">
                %(nombre_apellido)s
            </li>
        """ % form.vars

    return "$('.list-group').append('%s');" % item


def sanitize_dni(number):
    if number:
        return number.replace('.', '').strip()


def date_reportcert(rows_dates):
    result = ''
    n_dates = len(rows_dates)
    for c, item in enumerate(rows_dates):
        if c != 0 and c == n_dates - 1:
            result += ' y '
        elif c > 0 and c < n_dates:
            result += ', '
        
        result += item.fecha.strftime('%x')
    return result

def time_reportcert(rows_date):
    hours = []
    for d in rows_date:
        f1 = datetime(year=d.fecha.year,
                      month=d.fecha.month,
                      day=d.fecha.day,
                      hour=d.hora_inicio.hour,
                      minute=d.hora_inicio.minute)
        f2 = datetime(year=d.fecha.year,
                      month=d.fecha.month,
                      day=d.fecha.day,
                      hour=d.hora_fin.hour,
                      minute=d.hora_fin.minute)
        
        r = (f2 - f1).seconds / 60. ** 2
        hours.append(r)
        
    return sum(hours)


def str2date(date):
    if date:
        date = date.split('/')
        try:
            year = int(date[-1])
            month = int(date[-2]) if date[-2][0] != 0 else int(date[-2][-1])
            day = int(date[0])
            return datetime(year, month, day)
        except:
            return datetime.now()
    return datetime.now()