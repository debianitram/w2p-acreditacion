#!-*- encoding:utf-8 -*-

def hide_record(table, record):
    db[table](record).update_record(is_active=False)
    db.commit()


def readable_signature(table, show=True):
    for field in ('created_by', 'created_on', 'modified_by', 'modified_on'):
        table[field].readable = True if show else False