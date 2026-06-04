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

# All tables the library 0001_initial migration creates
LIBRARY_TABLES = [
    'library_libraryfine',
    'library_borrowedbook',
    'library_libraryuser',
    'library_librarysettings',
    'library_librarynews',
    'library_book',
]

def run_sql(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)

def table_exists(table_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def migration_recorded(app, name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM django_migrations WHERE app = %s AND name = %s
            );
        """, [app, name])
        return cursor.fetchone()[0]

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
    for table in LIBRARY_TABLES:
        if table_exists(table):
            run_sql(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
            print(f"  Dropped: {table}")
    # Also clear any stale migration record
    run_sql("DELETE FROM django_migrations WHERE app = 'library';")
    print("  Cleared library migration records\n")

elif not existing and not recorded:
    print("No tables and no migration record — fresh install, running migrate normally.\n")

elif existing and not missing and not recorded:
    print("All tables exist but not recorded — faking migration.\n")
    run_sql("""
        INSERT INTO django_migrations (app, name, applied)
        VALUES ('library', '0001_initial', NOW())
        ON CONFLICT DO NOTHING;
    """)

elif recorded and not missing:
    print("All tables exist and migration is recorded — nothing to fix.\n")

# Step 3: Run migrate
print("Running migrate...\n")
call_command('migrate', '--noinput')

# Step 4: Final check
print("\n=== Final State ===")
for table in LIBRARY_TABLES:
    exists = table_exists(table)
    print(f"  {'✓' if exists else '✗'} {table}")

print("\nDone!")
