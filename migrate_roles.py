import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swms.settings')
django.setup()

from hms.models import StaffProfile

ROLE_MAPPING = {
    'SUPER_ADMIN': 'super_admin',
    'HEALTH_MGR': 'health_manager',
    'MAINT_SUP': 'maintenance_sup',
    'WARDEN': 'warden',
    'FINANCE': 'finance_officer',
    'SECURITY': 'security_officer',
    'NEWS_EDITOR': 'news_editor',
    'AUDITOR': 'auditor',
    'EMERGENCY': 'emergency_coord',
    'SUPPORT': 'support_agent',
    'DIPLOMA': 'diploma_coordinator',
    'DEAN_HHS': 'dean_of_students',
    'DEFERMENT': 'deferment_officer',
    'DEPT_MCS': 'dept_mcs',
    'DVC_ASA': 'deputy_vice_chancellor', # Assuming DVC_ASA is a deputy
    'VC': 'vice_chancellor',
    'DVC': 'deputy_vice_chancellor',
    'REG_ADMIN': 'register_admin',
    'REG_USER': 'register_user',
    'DEAN_GRAD': 'dean_graduate_school',
    'DIR_RESOURCE': 'director_resource',
    'DIR_TVET': 'director_tvet',
    'NEWS_AUDITOR': 'news_auditor',
}

def migrate_roles():
    print("Starting role migration...")
    profiles = StaffProfile.objects.all()
    updated_count = 0
    for profile in profiles:
        old_role = profile.role
        if old_role in ROLE_MAPPING:
            profile.role = ROLE_MAPPING[old_role]
            profile.save()
            print(f"Updated user {profile.user.username}: {old_role} -> {profile.role}")
            updated_count += 1
        elif old_role not in ROLE_MAPPING.values():
            print(f"Unknown role {old_role} for user {profile.user.username}, leaving as is.")
            
    print(f"Finished role migration. Updated {updated_count} profiles.")

if __name__ == "__main__":
    migrate_roles()
