from django.test import TestCase
from django.contrib.auth.models import User
from hms.models import StaffProfile
from hms.decorators import role_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

class RBACTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststaff', password='Password123!')
        self.profile = StaffProfile.objects.create(
            user=self.user,
            role='dean_of_students',
            national_id='12345678',
            phone='0700000000'
        )

    def test_role_categorization(self):
        """Test that roles are correctly mapped to categories"""
        # Dean of Students should be ACADEMIC_ADMIN
        self.assertEqual(self.profile.get_category(), 'ACADEMIC_ADMIN')
        
        # Test a Finance role
        self.profile.role = 'auditor'
        self.profile.save()
        self.assertEqual(self.profile.get_category(), 'FINANCE_ADMIN')
        
        # Test an Executive role
        self.profile.role = 'vice_chancellor'
        self.profile.save()
        self.assertEqual(self.profile.get_category(), 'EXECUTIVE')

    def test_role_required_decorator(self):
        """Test the decorator with allowed_roles"""
        
        @role_required(allowed_roles=['dean_of_students'])
        def dummy_view(request):
            return "Success"

        # 1. Access granted
        self.profile.role = 'dean_of_students'
        self.profile.save()
        request = HttpRequest()
        request.user = self.user
        self.assertEqual(dummy_view(request), "Success")

        # 2. Access denied (auditor) should return a redirect (302)
        self.profile.role = 'auditor'
        self.profile.save()
        response = dummy_view(request)
        self.assertEqual(response.status_code, 302)

        # 3. Superuser should always have access
        self.user.is_superuser = True
        self.user.save()
        self.assertEqual(dummy_view(request), "Success")

    def test_staff_registration_form_searchable_role(self):
        """Test that the form correctly handles typed roles"""
        from hms.forms import StaffRegistrationForm
        
        # 1. Valid by Value
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'role': 'vice_chancellor',
            'national_id': 'ID123',
            'phone': '0700000000'
        }
        form = StaffRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['role'], 'vice_chancellor')

        # 2. Valid by Label (typing the human-readable string)
        form_data['role'] = 'Vice Chancellor'
        form_data['email'] = 'john2@example.com' # must be unique
        form = StaffRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['role'], 'vice_chancellor')

        # 3. Invalid role
        form_data['role'] = 'Invalid Role'
        form_data['email'] = 'john3@example.com'
        form = StaffRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('role', form.errors)

    def test_vice_chancellor_full_access_restricted(self):
        """Test that Vice Chancellor has full admin access except DB/Control System"""
        from hms.decorators import super_admin_required
        from hms.middleware import ViceChancellorRestrictionMiddleware
        from django.http import HttpResponse
        
        @super_admin_required
        def dummy_admin_view(request):
            return HttpResponse("Admin Success")

        # 1. VC has access to super_admin_required views
        self.profile.role = 'vice_chancellor'
        self.profile.save()
        
        request = HttpRequest()
        request.user = self.user
        
        # Mock requests framework expects request to have path/method
        request.path = '/manage/dashboard/'
        request.method = 'GET'
        
        # Test decorator allowing VC
        response = dummy_admin_view(request)
        self.assertEqual(response.content.decode(), "Admin Success")
        
        # 2. Test middleware restrictions
        middleware = ViceChancellorRestrictionMiddleware(get_response=lambda req: HttpResponse("Success"))
        
        # Should raise PermissionDenied for /admin/
        request.path = '/admin/auth/user/'
        with self.assertRaises(PermissionDenied):
            middleware(request)
            
        # Should raise PermissionDenied for control system
        request.path = '/manage/feature-flags/'
        with self.assertRaises(PermissionDenied):
            middleware(request)
            
        # Should pass for other admin views (like dashboard)
        request.path = '/manage/dashboard/'
        response = middleware(request)
        self.assertEqual(response.content.decode(), "Success")
