#!-*- encoding:utf-8 -*-

def hide_record(table, record):
    db[table](record).update_record(is_active=False)
    db.commit()