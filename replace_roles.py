import re

with open('hms/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add permission_required import if missing
if 'permission_required' not in content:
    content = content.replace('role_required,', 'role_required, permission_required,')

# Function name to permission mapping
mappings = {
    'admin_dashboard': 'view_dashboard',
    'diploma_students': 'view_students',
    'tvet_students': 'view_students',
    'students_list': 'view_students',
    'manage_payments': 'view_payments',
    'manage_health': 'view_health',
    'manage_maintenance': 'view_maintenance',
    'manage_announcements': 'view_news',
    'audit_log_list': 'view_audit',
    'audit_log_export': 'view_audit',
    'emergency_broadcast': 'view_emergency',
    'visitor_management': 'view_visitors',
    'checkout_visitor': 'view_visitors',
    'analytics_dashboard': 'view_reports',
    'admin_deferment_all': 'view_reports',
    'admin_deferment_pending': 'view_reports',
    'admin_deferment_under_review': 'view_reports',
    'admin_deferment_approved': 'view_reports',
    'admin_deferment_rejected': 'view_reports',
    'admin_deferment_resumed': 'view_reports',
    'review_deferment': 'view_reports',
    'delete_room': 'view_accommodation',
    'room_assignments': 'view_accommodation',
    'assign_room': 'view_accommodation',
    'room_change_requests': 'view_accommodation',
    'approve_room_change': 'view_accommodation',
    'lost_found_list': 'view_reports',
    
    # Missing from this list will fall back to a default or be left alone.
}

# Regex to find @role_required(...) followed by def function_name
pattern = re.compile(r'@role_required\([^)]*\)\s*def\s+([a-zA-Z0-9_]+)\(', re.MULTILINE)

def replacer(match):
    func_name = match.group(1)
    perm = mappings.get(func_name)
    if perm:
        return f"@permission_required('{perm}')\ndef {func_name}("
    else:
        # Default fallback to view_dashboard or just leave it?
        # The prompt says "update main admin views".
        # Let's map any remaining known ones to view_dashboard just in case.
        return match.group(0) # leave unchanged if not in mapping

new_content = pattern.sub(replacer, content)

with open('hms/views.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replacement complete.")
