import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swms.settings')
django.setup()

from django.db import connection

def fix_migrations():
    with connection.cursor() as cursor:
        tables = connection.introspection.table_names()
        if 'library_book' not in tables:
            print("library_book table is missing in the database.")
            print("Removing 'library' app migration records from django_migrations to force re-creation...")
            cursor.execute("DELETE FROM django_migrations WHERE app = 'library';")
            print("Records deleted. The next 'migrate' command will create the tables.")
        else:
            print("library_book table exists. Database is healthy.")

if __name__ == '__main__':
    fix_migrations()
