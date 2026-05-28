from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from hms.models import StaffProfile

class Command(BaseCommand):
    help = 'Sets up the 15 RBAC Staff Roles and seeds staff users'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting RBAC setup...")

        roles = [
            'SUPER_ADMIN', 'HEALTH_MGR', 'MAINT_SUP', 'WARDEN', 'FINANCE',
            'SECURITY', 'NEWS_EDITOR', 'AUDITOR', 'EMERGENCY', 'SUPPORT',
            'DIPLOMA', 'DEAN_HHS', 'DEFERMENT', 'DEPT_MCS', 'DVC_ASA'
        ]

        for role in roles:
            Group.objects.get_or_create(name=role)
            self.stdout.write(f"Group created/verified: {role}")

        # Seed staff
        staff_data = [
            {'name': 'Omar Abdalla', 'email': 'omar@campus.edu', 'role': 'DEAN_HHS'},
            {'name': 'Moses Isutsa', 'email': 'moses@campus.edu', 'role': 'DEFERMENT'},
            {'name': 'Musa Shile', 'email': 'musa@campus.edu', 'role': 'DEPT_MCS'},
            {'name': 'Troy Tsuma', 'email': 'troy@campus.edu', 'role': 'DVC_ASA'},
            {'name': 'John Kariuki', 'email': 'john@campus.edu', 'role': 'HEALTH_MGR'},
            {'name': 'Mary Wanjiku', 'email': 'mary@campus.edu', 'role': 'WARDEN'},
            {'name': 'Peter Odhiambo', 'email': 'peter@campus.edu', 'role': 'FINANCE'},
            {'name': 'Sarah Chebet', 'email': 'sarah@campus.edu', 'role': 'SECURITY'},
            {'name': 'James Kariuki', 'email': 'james@campus.edu', 'role': 'DIPLOMA'}
        ]

        for s in staff_data:
            username = s['email'].split('@')[0]
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': s['email'],
                    'first_name': s['name'].split()[0],
                    'last_name': ' '.join(s['name'].split()[1:]) if len(s['name'].split()) > 1 else ''
                }
            )
            if created:
                user.set_password('Staff123!')
                user.save()
                
            group = Group.objects.get(name=s['role'])
            user.groups.add(group)

            StaffProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': s['role'],
                    'national_id': f"ID_{username.upper()}",
                    'phone': '0700000000',
                    'is_approved': True
                }
            )
            self.stdout.write(f"Seeded staff user: {s['name']} as {s['role']}")

        self.stdout.write(self.style.SUCCESS("Successfully set up RBAC roles and staff!"))
