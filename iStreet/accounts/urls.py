from django.urls import path
from .views import *

urlpatterns = [
    path("", register, name='register'),
    path("accounts/login/", login_page, name='login'),
    path("home/", home, name='home'),
    path("logout/", logout_page, name='logout'),
    path("accounts/admin/", admin, name='admins'),
    path("executive/", executive, name='executive'),
    path("otp/", otp, name="otp"),
    path("department/", department, name='department'),
    path("userrole/", user_role, name='role'),
    path("expenses/", expenses, name='expense'),
    path("employee/", employee, name='employee'),
    path("dept-table/", dtable, name='dtable'),
    path("role-table/", role_table, name='roletable'),
    path("ex-table/", expense_table, name='extable'),
    path("emp-table/", emp_table, name='emp-table'),
    path("profile/", profile, name='profile'),
    path("activity/", activity, name='activity'),
    path("all-users/", all_users, name='all-users'),
    path("all-admins/", all_admins, name='all-admins'),
    path("all-ex/", all_executive, name='all-ex'),
    path("chart/", chart, name='chart'),
]
