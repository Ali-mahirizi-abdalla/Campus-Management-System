from hms.models import Permission, RolePermission

# Define the 11 modules/permissions
PERMISSIONS = [
    {'code': 'view_dashboard', 'name': 'View Dashboard', 'module': 'Dashboard'},
    {'code': 'view_students', 'name': 'View Students', 'module': 'Students'},
    {'code': 'view_health', 'name': 'View Health', 'module': 'Health'},
    {'code': 'view_payments', 'name': 'View Payments', 'module': 'Payments'},
    {'code': 'view_accommodation', 'name': 'View Accommodation', 'module': 'Accommodation'},
    {'code': 'view_maintenance', 'name': 'View Maintenance', 'module': 'Maintenance'},
    {'code': 'view_visitors', 'name': 'View Visitors', 'module': 'Visitors'},
    {'code': 'view_news', 'name': 'View News', 'module': 'News'},
    {'code': 'view_audit', 'name': 'View Audit', 'module': 'Audit'},
    {'code': 'view_emergency', 'name': 'View Emergency', 'module': 'Emergency'},
    {'code': 'view_reports', 'name': 'View Reports', 'module': 'Reports'},
    {'code': 'library_dashboard', 'name': 'Library Dashboard', 'module': 'Library'},
    {'code': 'borrowed_books', 'name': 'Borrowed Books', 'module': 'Library'},
    {'code': 'fine_management', 'name': 'Fine Management', 'module': 'Library'},
    {'code': 'student_library_accounts', 'name': 'Student Library Accounts', 'module': 'Library'},
    {'code': 'library_reports', 'name': 'Library Reports', 'module': 'Library'},
]

for p_data in PERMISSIONS:
    Permission.objects.get_or_create(code=p_data['code'], defaults={'name': p_data['name'], 'module': p_data['module']})

# Matrix mapping (Role -> List of allowed permissions)
ROLE_MATRIX = {
    'super_admin': ['view_dashboard', 'view_students', 'view_health', 'view_payments', 'view_accommodation', 'view_maintenance', 'view_visitors', 'view_news', 'view_audit', 'view_emergency', 'view_reports', 'library_dashboard', 'borrowed_books', 'fine_management', 'student_library_accounts', 'library_reports'],
    'vice_chancellor': ['view_dashboard', 'view_students', 'view_reports'],
    'deputy_vice_chancellor': ['view_dashboard', 'view_students', 'view_reports'],
    'register_admin': ['view_dashboard', 'view_students', 'view_reports'],
    'register_user': ['view_dashboard', 'view_students'],
    'dean_of_students': ['view_dashboard', 'view_students', 'view_reports'],
    'dean_graduate_school': ['view_dashboard', 'view_students', 'view_reports'],
    'director_resource': ['view_dashboard', 'view_reports'],
    'director_tvet': ['view_dashboard', 'view_students', 'view_reports'],
    'deferment_officer': ['view_dashboard', 'view_reports'],
    'dept_mcs': ['view_dashboard', 'view_students', 'view_reports'],
    'health_manager': ['view_dashboard', 'view_health', 'view_reports'],
    'maintenance_sup': ['view_dashboard', 'view_maintenance', 'view_reports'],
    'warden': ['view_dashboard', 'view_accommodation', 'view_reports'],
    'finance_officer': ['view_dashboard', 'view_payments', 'view_reports'],
    'security_officer': ['view_dashboard', 'view_visitors', 'view_reports'],
    'news_editor': ['view_dashboard', 'view_news', 'view_reports'],
    'news_auditor': ['view_dashboard', 'view_news', 'view_reports'],
    'emergency_coord': ['view_dashboard', 'view_emergency'],
    'support_agent': ['view_dashboard', 'view_reports'],
    'auditor': ['view_dashboard', 'view_audit', 'view_reports'],
    'diploma_coordinator': ['view_dashboard', 'view_students', 'view_reports'],
    'dept_coordinator': ['view_dashboard', 'view_students', 'view_reports'],
    'librarian': ['library_dashboard', 'borrowed_books', 'fine_management', 'student_library_accounts', 'library_reports'],
}

RolePermission.objects.all().delete()

for role, perms in ROLE_MATRIX.items():
    for p_code in perms:
        perm = Permission.objects.get(code=p_code)
        RolePermission.objects.create(role=role, permission=perm)

print("Successfully seeded permissions for all 23 roles.")
