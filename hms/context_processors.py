from django.conf import settings
from .models import Message, Notification

def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'unread_notifications': notifications,
            'unread_notification_count': unread_count
        }
    return {'unread_notifications': [], 'unread_notification_count': 0}


def unread_messages(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_messages': count}
    return {'unread_messages': 0}

def staff_role_info(request):
    if request.user.is_authenticated:
        staff_profile = getattr(request.user, 'staff_profile', None)
        if staff_profile:
            category = staff_profile.get_category()
            return {
                'staff_category': category.replace('_', ' ').title() if category else "Staff",
                'staff_category_raw': category,
                'staff_role': staff_profile.get_role_display()
            }
    return {'staff_category': None, 'staff_category_raw': None, 'staff_role': None}

def telegram_info(request):
    """Makes Telegram Chat ID / Username available to all templates."""
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    # Clean @ if present for the join link
    clean_handle = chat_id.lstrip('@')
    return {
        'TELEGRAM_CHAT_ID': chat_id,
        'TELEGRAM_JOIN_LINK': f"https://t.me/{clean_handle}" if clean_handle else None
    }

def role_permissions(request):
    """Provides a list of allowed menu items based on the user's staff role."""
    ROLE_MENU_ITEMS = {
        'SUPER_ADMIN': [
            'dashboard', 'staff_management', 'role_management', 'students', 
            'health', 'maintenance', 'accommodation', 'payments', 
            'visitors', 'news', 'audit_logs', 'emergency', 'settings', 'reports'
        ],
        'VC': [
            'dashboard', 'all_staff', 'reports', 'analytics', 'academic_overview'
        ],
        'DVC': [
            'dashboard', 'all_staff', 'academic_reports', 'department_analytics'
        ],
        'REG_ADMIN': [
            'dashboard', 'all_staff', 'student_registrations', 'reports'
        ],
        'REG_USER': [
            'dashboard', 'all_staff_view', 'student_list'
        ],
        'DEAN_HHS': [
            'dashboard', 'all_students', 'welfare_cases', 'disciplinary', 'student_chat'
        ],
        'DEAN_GRAD': [
            'dashboard', 'graduate_students', 'thesis_tracking', 'graduate_reports'
        ],
        'DIR_RESOURCE': [
            'dashboard', 'graduate_funding', 'grants', 'donor_reports'
        ],
        'DIR_TVET': [
            'dashboard', 'tvet_students', 'attachment_placement', 'tvet_reports'
        ],
        'DEFERMENT': [
            'dashboard', 'deferment_requests', 'approvals', 'deferment_letters'
        ],
        'DEPT_MCS': [
            'dashboard', 'mcs_students', 'mcs_courses', 'mcs_reports'
        ],
        'HEALTH_MGR': [
            'dashboard', 'appointments', 'patients', 'prescriptions', 'health_reports'
        ],
        'MAINT_SUP': [
            'dashboard', 'maintenance_requests', 'assignments', 'inventory', 'maintenance_reports'
        ],
        'WARDEN': [
            'dashboard', 'room_allocation', 'deferments', 'checkin_checkout', 'accommodation_reports'
        ],
        'FINANCE': [
            'dashboard', 'payments', 'mpesa_records', 'dues', 'receipts', 'subscriptions', 'financial_reports'
        ],
        'SECURITY': [
            'dashboard', 'visitor_logs', 'entry_exit', 'blacklist', 'security_reports'
        ],
        'NEWS_EDITOR': [
            'dashboard', 'create_news', 'schedule_posts', 'send_alerts', 'news_analytics', 'archive'
        ],
        'NEWS_AUDITOR': [
            'dashboard', 'news_audit_logs', 'export_reports'
        ],
        'EMERGENCY': [
            'dashboard', 'send_alert', 'alert_presets', 'alert_history'
        ],
        'SUPPORT': [
            'dashboard', 'active_chats', 'support_tickets', 'faq_library'
        ],
        'AUDITOR': [
            'dashboard', 'system_audit_logs', 'export_audit_reports'
        ],
        'DIPLOMA': [
            'dashboard', 'diploma_students', 'diploma_deferments', 'graduates', 'attachment', 'diploma_reports'
        ],
        'DEPT_COORD': [
            'dashboard', 'department_students', 'department_courses', 'department_reports'
        ]
    }
    
    if request.user.is_authenticated and hasattr(request.user, 'staff_profile'):
        role = request.user.staff_profile.role
        # Superuser always gets super admin permissions
        if request.user.is_superuser:
            role = 'SUPER_ADMIN'
        return {'allowed_menus': ROLE_MENU_ITEMS.get(role, [])}
    
    return {'allowed_menus': []}
