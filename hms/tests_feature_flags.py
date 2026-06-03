from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from hms.models import FeatureFlag, StaffProfile, AuditLog
from hms.feature_flags import feature_flags, EXISTING_FEATURES, NEW_FEATURES
import json

class FeatureFlagsTestCase(TestCase):
    def setUp(self):
        # Create users
        self.super_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        # Create staff profile for super admin
        self.super_profile = StaffProfile.objects.create(
            user=self.super_user,
            role='super_admin',
            national_id='11223344',
            phone='0711223344'
        )
        
        self.regular_user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='studentpassword'
        )
        
        self.client = Client()

    def test_feature_flags_python_helper(self):
        # 1. Existing (locked) features should always be True
        for feature in EXISTING_FEATURES:
            name = feature['name']
            self.assertTrue(feature_flags.is_enabled(name))
            self.assertTrue(feature_flags.is_enabled[name])
            self.assertTrue(getattr(feature_flags, name))
            self.assertTrue(getattr(feature_flags.is_enabled, name))

        # 2. New features should default to their default value (usually False)
        for feature in NEW_FEATURES:
            name = feature['name']
            default_val = feature['default']
            self.assertEqual(feature_flags.is_enabled(name), default_val)
            self.assertEqual(getattr(feature_flags, name), default_val)
            self.assertEqual(getattr(feature_flags.is_enabled, name), default_val)

        # 3. Toggling a feature flag
        feature_name = NEW_FEATURES[0]['name']
        
        # Enable it
        feature_flags.set_enabled(feature_name, True)
        self.assertTrue(feature_flags.is_enabled(feature_name))
        self.assertTrue(getattr(feature_flags, feature_name))
        self.assertTrue(getattr(feature_flags.is_enabled, feature_name))
        
        # Disable it
        feature_flags.set_enabled(feature_name, False)
        self.assertFalse(feature_flags.is_enabled(feature_name))

    def test_feature_flags_views_permissions(self):
        # 1. Anonymous access to control panel should redirect to login
        url = reverse('hms:feature_flags')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # 2. Student access should redirect (not authorized)
        self.client.login(username='student', password='studentpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirects to dashboard
        self.client.logout()

        # 3. Super Admin access should work
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hms/admin/feature_flags.html')
        self.client.logout()

    def test_feature_flags_api_endpoints(self):
        self.client.login(username='admin', password='adminpassword')
        api_url = reverse('hms:update_feature_flags_api')
        
        feature_name = NEW_FEATURES[0]['name']
        
        # 1. Toggle feature flag ON
        payload = {
            'action': 'toggle',
            'name': feature_name,
            'enabled': True
        }
        response = self.client.post(
            api_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertTrue(feature_flags.is_enabled(feature_name))
        
        # Check audit log was created
        self.assertTrue(AuditLog.objects.filter(action='UPDATE', model_name='FeatureFlag', object_repr=f"Feature: {feature_name}").exists())

        # 2. Toggle feature flag OFF
        payload = {
            'action': 'toggle',
            'name': feature_name,
            'enabled': False
        }
        response = self.client.post(
            api_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(feature_flags.is_enabled(feature_name))

        # 3. Enable all features
        payload = {'action': 'enable_all'}
        response = self.client.post(
            api_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        for f in NEW_FEATURES:
            self.assertTrue(feature_flags.is_enabled(f['name']))

        # 4. Disable all features
        payload = {'action': 'disable_all'}
        response = self.client.post(
            api_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        for f in NEW_FEATURES:
            self.assertFalse(feature_flags.is_enabled(f['name']))

        # 5. Reset features
        # Manually enable one first
        feature_flags.set_enabled(feature_name, True)
        payload = {'action': 'reset'}
        response = self.client.post(
            api_url, 
            data=json.dumps(payload), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        for f in NEW_FEATURES:
            self.assertEqual(feature_flags.is_enabled(f['name']), f['default'])
