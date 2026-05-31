import os

BASE_DIR = os.path.join(os.path.dirname(__file__), 'hms', 'templates', 'hms')

ROLES = [
    {
        'code': 'super_admin',
        'dir': 'admin',
        'name': 'dashboard_super_admin.html',
        'title': 'Super Admin Dashboard',
        'features': ['📊 All System Metrics', '👥 Staff Management (Add, Edit, Delete)', '👑 Role Management (Assign Permissions)', '🎓 All Students (View, Edit, Delete)', '🏥 Health Management (Full Access)', '🔧 Maintenance Management (Full Access)', '🏠 Accommodation Management (Full Access)', '💰 Payments & M-Pesa (Full Access)', '👤 Visitor Management (Full Access)', '📢 News & Alerts (Full Access)', '📜 Audit Logs (Full Access)', '🚨 Emergency Alerts (Full Access)', '💬 Student Chat (Monitor All)', '⚙️ System Settings']
    },
    {
        'code': 'vice_chancellor',
        'dir': 'executive',
        'name': 'dashboard_vc.html',
        'title': 'Vice Chancellor Dashboard',
        'features': ['📊 Institution Analytics', '👥 View All Staff (Read-Only)', '📈 Department Performance Reports', '🏫 Campus Overview', '📋 Strategic Reports']
    },
    {
        'code': 'deputy_vice_chancellor',
        'dir': 'executive',
        'name': 'dashboard_dvc.html',
        'title': 'Deputy Vice Chancellor Dashboard',
        'features': ['📊 Academic Analytics', '👥 View All Staff (Read-Only)', '📚 Academic Department Reports', '🎓 Student Academic Performance', '📋 Accreditation Reports']
    },
    {
        'code': 'register_admin',
        'dir': 'registration',
        'name': 'dashboard_register_admin.html',
        'title': 'Register Admin Dashboard',
        'features': ['👥 View All Staff', '📝 Manage Student Registrations', '🎓 Student Enrollment', '📊 Registration Reports', '📋 Generate Registration Documents']
    },
    {
        'code': 'register_user',
        'dir': 'registration',
        'name': 'dashboard_register_user.html',
        'title': 'Register User Dashboard',
        'features': ['👥 View All Staff (Read-Only)', '📋 Staff Directory', '🔍 Search Staff']
    },
    {
        'code': 'dean_of_students',
        'dir': 'student_affairs',
        'name': 'dashboard_dean.html',
        'title': 'Dean of Students Dashboard',
        'features': ['👥 All Students (Full Access)', '📋 Welfare Cases Management', '⚖️ Disciplinary Cases', '💬 Student Chat', '📊 Student Reports', '🏠 Accommodation Requests']
    },
    {
        'code': 'dean_graduate_school',
        'dir': 'graduate',
        'name': 'dashboard_dean_graduate.html',
        'title': 'Dean - Graduate School Dashboard',
        'features': ['👥 Masters Students Only', '👥 PhD Students Only', '📝 Thesis/Dissertation Tracking', '🎓 Graduate Supervision', '📊 Graduate Reports']
    },
    {
        'code': 'director_resource',
        'dir': 'graduate',
        'name': 'dashboard_resource.html',
        'title': 'Director - Resource Mobilization Dashboard',
        'features': ['💰 Graduate School Funding', '📝 Grant Applications', '📊 Resource Reports', '🤝 Donor Management', '💵 Budget Tracking (Graduate Only)']
    },
    {
        'code': 'director_tvet',
        'dir': 'tvet',
        'name': 'dashboard_tvet.html',
        'title': 'Director - TVET Dashboard',
        'features': ['👥 Diploma Students Only', '💼 Attachment/Internship Placement', '📊 TVET Reports', '🎓 TVET Graduates', '📋 Industry Partnerships']
    },
    {
        'code': 'deferment_officer',
        'dir': 'academic',
        'name': 'dashboard_deferment.html',
        'title': 'Deferment Officer Dashboard',
        'features': ['⏳ Pending Deferment Requests', '✅ Approve Deferments', '❌ Reject Deferments', '📜 Deferment History', '📄 Generate Deferment Letters', '📧 Notify Students']
    },
    {
        'code': 'dept_mcs',
        'dir': 'departments',
        'name': 'dashboard_mcs.html',
        'title': 'Dept MCS Coordinator Dashboard',
        'features': ['👥 Computer Science Students Only', '📚 CS Courses Management', '📊 CS Department Reports', '🎓 CS Student Progress']
    },
    {
        'code': 'health_manager',
        'dir': 'health',
        'name': 'dashboard_health.html',
        'title': 'Health Manager Dashboard',
        'features': ['📅 Appointments (Create, View, Edit)', '👥 Patient Records', '💊 Prescriptions', '📋 Medical History', '📊 Health Reports', '🏥 Clinic Status']
    },
    {
        'code': 'maintenance_sup',
        'dir': 'facilities',
        'name': 'dashboard_maintenance.html',
        'title': 'Maintenance Supervisor Dashboard',
        'features': ['🔧 Open Maintenance Requests', '⚡ Urgent Requests', '👷 Assign Technicians', '✅ Completed Requests', '📦 Inventory Management', '📊 Maintenance Reports']
    },
    {
        'code': 'warden',
        'dir': 'accommodation',
        'name': 'dashboard_warden.html',
        'title': 'Warden Dashboard',
        'features': ['🛏️ Room Allocation', '📋 Deferment Requests (Accommodation)', '🚪 Check-in/Check-out', '🏢 Building Status', '📊 Occupancy Report', '👥 Student Housing Records']
    },
    {
        'code': 'finance_officer',
        'dir': 'finance',
        'name': 'dashboard_finance.html',
        'title': 'Finance Officer Dashboard',
        'features': ['💵 Today\'s Collections', '📱 M-Pesa Records', '📋 Pending Dues', '🧾 Generate Receipts', '📊 Financial Reports', '🔄 Subscription Management']
    },
    {
        'code': 'security_officer',
        'dir': 'security',
        'name': 'dashboard_security.html',
        'title': 'Security Officer Dashboard',
        'features': ['📝 Log Visitor Entry', '📝 Log Visitor Exit', '👥 Visitors Currently Inside', '⛔ Blacklist Management', '🚗 Vehicle Log', '📊 Security Reports']
    },
    {
        'code': 'news_editor',
        'dir': 'communications',
        'name': 'dashboard_news_editor.html',
        'title': 'News Editor Dashboard',
        'features': ['📝 Create News Articles', '📅 Schedule Posts', '🔔 Send Push Alerts', '📋 Drafts Management', '📊 Engagement Analytics', '📁 Archive']
    },
    {
        'code': 'news_auditor',
        'dir': 'communications',
        'name': 'dashboard_news_auditor.html',
        'title': 'News Auditor Dashboard',
        'features': ['📋 View News Audit Logs', '📥 Export Audit Reports', '🔍 Search News History']
    },
    {
        'code': 'emergency_coord',
        'dir': 'safety',
        'name': 'dashboard_emergency.html',
        'title': 'Emergency Coordinator Dashboard',
        'features': ['🚨 Send Emergency Alert', '🔥 Fire Alert Preset', '🚔 Security Alert Preset', '🏥 Medical Alert Preset', '📋 Alert History', '📝 Template Management']
    },
    {
        'code': 'support_agent',
        'dir': 'support',
        'name': 'dashboard_support.html',
        'title': 'Support Agent Dashboard',
        'features': ['💬 Active Chats', '⏳ Waiting Tickets', '✅ Resolved Today', '📚 FAQ Library', '📊 Support Analytics', '⚡ Quick Response Templates']
    },
    {
        'code': 'auditor',
        'dir': 'audit',
        'name': 'dashboard_auditor.html',
        'title': 'Auditor Dashboard',
        'features': ['📜 System Audit Logs', '🔍 Search Logs', '📥 Export Reports', '📊 Activity Trends', '👤 User Action History']
    },
    {
        'code': 'diploma_coordinator',
        'dir': 'diploma',
        'name': 'dashboard_diploma.html',
        'title': 'Diploma Coordinator Dashboard',
        'features': ['👥 Diploma Students Only', '📋 Diploma Deferments', '🎓 Diploma Graduates', '💼 Attachment Placement', '📊 Program Reports', '📧 Bulk Email to Diploma Students']
    },
    {
        'code': 'dept_coordinator',
        'dir': 'departments',
        'name': 'dashboard_dept_coordinator.html',
        'title': 'Department Coordinator Dashboard',
        'features': ['👥 Own Department Students Only', '📚 Department Courses', '📊 Department Reports', '🎓 Department Student Progress']
    }
]

TEMPLATE_STR = """{{% extends 'hms/base.html' %}}

{{% block title %}}{title} - Campus Care{{% endblock %}}

{{% block content %}}
<div class="space-y-6">
    <div class="flex justify-between items-center">
        <div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{title}</h1>
            <p class="text-gray-500 dark:text-gray-400">Welcome back, {{{{ user.get_full_name }}}}</p>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {feature_blocks}
    </div>
</div>
{{% endblock %}}
"""

FEATURE_STR = """
        <!-- Feature: {feature_name} -->
        <div class="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 p-6 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 rounded-full bg-indigo-50 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-400 flex items-center justify-center mb-4 text-2xl">
                {icon}
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">{feature_title}</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Manage and view details for this module.</p>
            <button class="mt-4 px-4 py-2 bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400 rounded-lg text-sm font-medium hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors">Access Module</button>
        </div>
"""

def generate_dashboards():
    # Make sure default template exists too
    default_path = os.path.join(BASE_DIR, 'dashboard_default.html')
    if not os.path.exists(default_path):
        with open(default_path, 'w', encoding='utf-8') as f:
            f.write(TEMPLATE_STR.format(title="Staff Dashboard", feature_blocks="<p>No specific modules assigned to your role.</p>"))
            
    for role in ROLES:
        dir_path = os.path.join(BASE_DIR, role['dir'])
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, role['name'])
        
        feature_blocks = []
        for feature in role['features']:
            # Try to extract icon
            parts = feature.split(' ', 1)
            icon = '📌'
            feature_title = feature
            if len(parts) == 2 and len(parts[0]) <= 2: # Assume first part is emoji if short
                icon = parts[0]
                feature_title = parts[1]
            
            feature_blocks.append(FEATURE_STR.format(
                feature_name=feature,
                icon=icon,
                feature_title=feature_title
            ))
            
        content = TEMPLATE_STR.format(
            title=role['title'],
            feature_blocks="\\n".join(feature_blocks)
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Created {file_path}")

if __name__ == "__main__":
    generate_dashboards()
