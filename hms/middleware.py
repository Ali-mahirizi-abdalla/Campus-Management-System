from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.core.cache import cache
from django.utils import timezone
import threading
from .models import AdminSubscription

# Thread-local storage to pass request info to signals
_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

class AuditMiddleware:
    """
    Middleware to capture request details (User, IP) for Audit Logging.
    Stores request in thread-local storage for access in signals.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        
        # Cleanup
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
            
        return response

class PresenceMiddleware:
    """
    Middleware to track user 'online' status using Django Cache.
    A user is considered online if they've made a request within the last 5 minutes.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Mark user as active by storing a timestamp in cache
            # Key: 'seen_[user_id]', Value: 'online', Expiry: 300 seconds (5 min)
            cache_key = f'seen_{request.user.id}'
            cache.set(cache_key, 'online', 300)
            
        response = self.get_response(request)
        return response

class SubscriptionLockMiddleware:
    """
    Middleware to lock the system if the admin subscription has expired.
    Whitelists logic for payment, login, and static files.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Scheduled Activation Check: Features start May 1st, 2026
        activation_date = timezone.datetime(2026, 5, 1, tzinfo=timezone.get_current_timezone())
        if timezone.now() < activation_date:
            return self.get_response(request)

        # Static and media files are always whitelisted
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Try to match whitelisted named URLs
        try:
            whitelisted_urls = [
                reverse('hms:login'),
                reverse('hms:logout'),
                reverse('hms:mpesa_callback'),
            ]
            # These might not be defined yet, so we handle NoReverseMatch
            try:
                whitelisted_urls.append(reverse('hms:admin_subscription_pay'))
                whitelisted_urls.append(reverse('hms:system_locked'))
                whitelisted_urls.append(reverse('hms:check_registration_status', kwargs={'checkout_id': 'dummy'}))
            except NoReverseMatch:
                pass
        except NoReverseMatch:
            whitelisted_urls = []

        if request.path in whitelisted_urls:
            return self.get_response(request)

        # Check subscription status
        active_sub = AdminSubscription.objects.filter(status='Active', expiry_date__gt=timezone.now()).exists()

        if not active_sub:
            # If the user is staff, redirect to payment page
            if request.user.is_authenticated and request.user.is_staff:
                try:
                    pay_url = reverse('hms:admin_subscription_pay')
                    if request.path != pay_url:
                        return redirect(pay_url)
                except NoReverseMatch:
                    pass
            else:
                try:
                    lock_url = reverse('hms:system_locked')
                    if request.path != lock_url:
                        return redirect(lock_url)
                except NoReverseMatch:
                    pass

        return self.get_response(request)

class StrictRoleAccessMiddleware:
    """
    Enforces strict Role-Based Access Control (RBAC) at the URL level.
    No staff member can access any feature, module, or data not explicitly assigned to their role.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Matrix of 23 roles and their permitted URL path prefixes
        self.role_url_map = {
            'SUPER_ADMIN': [
                '/manage/', '/health/', '/chat/'
            ],
            'VC': [
                '/manage/staff/', '/manage/reports/', '/manage/analytics/', '/manage/academic-overview/'
            ],
            'DVC': [
                '/manage/staff/', '/manage/academic-reports/', '/manage/department-analytics/'
            ],
            'REG_ADMIN': [
                '/manage/staff/', '/manage/registrations/', '/manage/reports/'
            ],
            'REG_USER': [
                '/manage/staff/list/', '/manage/students/'
            ],
            'DEAN_HHS': [
                '/manage/students/', '/manage/welfare-cases/', '/manage/disciplinary/', '/chat/'
            ],
            'DEAN_GRAD': [
                '/manage/graduate-students/', '/manage/thesis-tracking/', '/manage/graduate-reports/'
            ],
            'DIR_RESOURCE': [
                '/manage/graduate-funding/', '/manage/grants/', '/manage/donor-reports/'
            ],
            'DIR_TVET': [
                '/manage/tvet-students/', '/manage/attachment-placement/', '/manage/tvet-reports/'
            ],
            'DEFERMENT': [
                '/manage/deferments/', '/manage/deferment-requests/', '/manage/deferment-letters/'
            ],
            'DEPT_MCS': [
                '/manage/mcs-students/', '/manage/mcs-courses/', '/manage/mcs-reports/'
            ],
            'HEALTH_MGR': [
                '/health/', '/manage/appointments/', '/manage/patients/', '/manage/prescriptions/', '/manage/health-reports/'
            ],
            'MAINT_SUP': [
                '/manage/maintenance-requests/', '/manage/assignments/', '/manage/inventory/', '/manage/maintenance-reports/'
            ],
            'WARDEN': [
                '/manage/room-allocation/', '/manage/deferments/', '/manage/checkin-checkout/', '/manage/accommodation-reports/'
            ],
            'FINANCE': [
                '/manage/payments/', '/manage/mpesa-records/', '/manage/dues/', '/manage/receipts/', '/manage/subscriptions/', '/manage/financial-reports/'
            ],
            'SECURITY': [
                '/manage/visitor-logs/', '/manage/entry-exit/', '/manage/blacklist/', '/manage/security-reports/'
            ],
            'NEWS_EDITOR': [
                '/manage/news/', '/manage/create-news/', '/manage/schedule-posts/', '/manage/send-alerts/', '/manage/news-analytics/', '/manage/archive/'
            ],
            'NEWS_AUDITOR': [
                '/manage/news-audit-logs/', '/manage/export-reports/'
            ],
            'EMERGENCY': [
                '/manage/send-alert/', '/manage/alert-presets/', '/manage/alert-history/'
            ],
            'SUPPORT': [
                '/manage/active-chats/', '/manage/support-tickets/', '/manage/faq-library/', '/chat/'
            ],
            'AUDITOR': [
                '/manage/system-audit-logs/', '/manage/export-audit-reports/', '/manage/audit/'
            ],
            'DIPLOMA': [
                '/manage/diploma-students/', '/manage/diploma-deferments/', '/manage/graduates/', '/manage/attachment/', '/manage/diploma-reports/'
            ],
            'DEPT_COORD': [
                '/manage/department-students/', '/manage/department-courses/', '/manage/department-reports/'
            ]
        }
    
    def __call__(self, request):
        user = request.user
        path = request.path
        
        # Only apply restrictions to staff members on management routes
        # Skip for superusers
        if user.is_authenticated and hasattr(user, 'staff_profile') and not user.is_superuser:
            role = user.staff_profile.role
            
            # Identify if this is a restricted path
            is_restricted_area = path.startswith('/manage/') or path.startswith('/health/') or path.startswith('/chat/')
            
            if is_restricted_area:
                allowed_paths = self.role_url_map.get(role, [])
                
                # Global allowed management paths for all roles
                allowed_paths.extend([
                    '/manage/dashboard/', 
                    '/manage/profile/', 
                    '/notifications/'
                ])
                
                # Check if current path matches any allowed path prefix
                is_allowed = False
                for allowed in allowed_paths:
                    if path.startswith(allowed):
                        is_allowed = True
                        break
                
                if not is_allowed and role != 'SUPER_ADMIN':
                    return redirect('hms:unauthorized')
        
        return self.get_response(request)
