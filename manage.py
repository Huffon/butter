#!/usr/bin/env python
import os
import sys
import sqlite3

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'butter.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    con = sqlite3.connect("./DB/userquiz.db")
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE user_quiz(Name TEXT, Quiz TEXT, Hint TEXT);")
    except:
        pass

    execute_from_command_line(sys.argv)
