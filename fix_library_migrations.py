"""
Fix library migration state on production.
Strategy: Drop any partial library tables, clear migration record, re-run fresh.
Safe because there's no real data in these tables yet.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swms.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
from django.db.migrations.recorder import MigrationRecorder

# All tables the library 0001_initial migration creates
LIBRARY_TABLES = [
    'library_libraryfine',
    'library_borrowedbook',
    'library_libraryuser',
    'library_librarysettings',
    'library_librarynews',
    'library_book',
]

def table_exists(table_name):
    return table_name in connection.introspection.table_names()

def migration_recorded(app, name):
    recorder = MigrationRecorder(connection)
    return (app, name) in recorder.applied_migrations()

print("=== Library DB Fix Script ===\n")

# Step 1: Check current state
existing = [t for t in LIBRARY_TABLES if table_exists(t)]
missing  = [t for t in LIBRARY_TABLES if not table_exists(t)]
recorded = migration_recorded('library', '0001_initial')

print(f"Tables that EXIST:   {existing or 'none'}")
print(f"Tables that MISSING: {missing or 'none'}")
print(f"Migration recorded:  {recorded}\n")

# Step 2: If DB is in a partial state (some exist, some don't), drop all and start fresh
if existing and missing:
    print("Partial state detected — dropping existing library tables for a clean migrate...\n")
    # Drop in reverse order of foreign key dependencies
    recorder = MigrationRecorder(connection)
    with connection.cursor() as cursor:
        for table in LIBRARY_TABLES:
            if table in connection.introspection.table_names():
                if connection.vendor == 'postgresql':
                    cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                else:
                    cursor.execute(f'DROP TABLE IF EXISTS "{table}";')
                print(f"  Dropped: {table}")
    # Also clear any stale migration record
    recorder.migration_class.objects.filter(app='library').delete()
    print("  Cleared library migration records\n")

elif not existing and not recorded:
    print("No tables and no migration record — fresh install, running migrate normally.\n")

elif existing and not missing and not recorded:
    print("All tables exist but not recorded — faking migration.\n")
    recorder = MigrationRecorder(connection)
    recorder.record_applied('library', '0001_initial')

elif recorded and not missing:
    print("All tables exist and migration is recorded — nothing to fix.\n")

# Step 3: Run migrate
print("Running migrate...\n")
call_command('migrate', '--noinput')

# Step 4: Final check
print("\n=== Final State ===")
for table in LIBRARY_TABLES:
    exists = table_exists(table)
    print(f"  {'[OK]' if exists else '[MISSING]'} {table}")

print("\nDone!")
