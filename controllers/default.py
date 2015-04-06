# -*- coding: utf-8 -*-

def index():
    return dict()


def user():
    return dict(form=auth())


@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()


