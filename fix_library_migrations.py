"""
Script to fix the library migration state on production.
Run with: python fix_library_migrations.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swms.settings')
django.setup()

from django.db import connection

def table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def migration_recorded(app, name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM django_migrations 
                WHERE app = %s AND name = %s
            );
        """, [app, name])
        return cursor.fetchone()[0]

def record_migration(app, name):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES (%s, %s, NOW())
            ON CONFLICT DO NOTHING;
        """, [app, name])
    print(f"  ✓ Recorded migration: {app}.{name}")

library_tables = [
    'library_book',
    'library_librarynews', 
    'library_librarysettings',
    'library_borrowedbook',
    'library_libraryuser',
    'library_libraryfine',
]

print("=== Library Migration State Check ===\n")

print("Tables in database:")
for table in library_tables:
    exists = table_exists(table)
    print(f"  {'✓' if exists else '✗'} {table}: {'EXISTS' if exists else 'MISSING'}")

print(f"\nMigration record for library.0001_initial: {'RECORDED' if migration_recorded('library', '0001_initial') else 'MISSING'}")

print("\n=== Attempting Fix ===\n")

any_table_exists = any(table_exists(t) for t in library_tables)

if any_table_exists and not migration_recorded('library', '0001_initial'):
    print("Tables exist but migration not recorded. Faking migration...")
    record_migration('library', '0001_initial')
    print("Done! Now running remaining migrations...")
    
    from django.core.management import call_command
    call_command('migrate', '--noinput')
elif not any_table_exists and not migration_recorded('library', '0001_initial'):
    print("No tables exist and migration not recorded. Running full migrate...")
    from django.core.management import call_command
    call_command('migrate', '--noinput')
elif migration_recorded('library', '0001_initial'):
    print("Migration already recorded. Checking for unapplied migrations...")
    from django.core.management import call_command
    call_command('migrate', '--noinput')

print("\n=== Final State ===")
for table in library_tables:
    exists = table_exists(table)
    print(f"  {'✓' if exists else '✗'} {table}: {'EXISTS' if exists else 'MISSING'}")

print("\nDone!")
