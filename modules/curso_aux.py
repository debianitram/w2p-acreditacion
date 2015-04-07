from gluon import current
from gluon.html import A, URL
from gluon.http import redirect


Curso = current.globalenv.get('Curso')

def oncreate(form):
    redirect(URL(args=('view', Curso._tablename, form.vars.id),
                 user_signature=True))