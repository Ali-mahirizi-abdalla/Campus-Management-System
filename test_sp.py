import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swms.settings')
django.setup()
from django.contrib.auth.models import User
from hms.models import StaffProfile

u = User.objects.filter(username='test_admin').first()
print(f'test_admin has staff_profile: {hasattr(u, "staff_profile")}')
print(f'Total StaffProfiles: {StaffProfile.objects.count()}')
for sp in StaffProfile.objects.all():
    print(f'Staff: {sp.user.username}, Role: {sp.role}')
