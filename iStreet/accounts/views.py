from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model, logout
import random
from django.db.models import Count, Sum

import datetime

# Create your views here.


# def register(request):
#     print("Register Starting")
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('password1')
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         city = request.POST.get('city')
#         role = request.POST.get('user_type')
#
#         if password != confirm_password:
#             messages.error(request, "Your passwords didn't match!")
#             return redirect('register.html')
#         elif CustomUser.objects.filter(email=email).filter(is_active=True):
#             print("You are coming here")
#             messages.error(request, f'{email} is already exists! Please try with another email!!')
#
#         else:
#             otp = ""
#             for i in range(6):
#                 otp += str(random.randint(0, 9))
#
#             my_user = CustomUser(username=username, email=email, password=password, name=name, phone=phone, city=city, role=role, otp=otp)
#             my_user.set_password(password)
#             my_user.save()
#             subject = 'OTP Verification'
#             message = f'Dear {my_user.name}, Your OTP is: {otp}'
#             from_email = settings.EMAIL_HOST_USER
#             recipient_list = [my_user.email]
#             send_mail(subject, message, from_email, recipient_list)
#             messages.success(request, f'OTP sent successfully on {email}')
#         return render(request, 'otp.html', )
#     return render(request, 'register.html',)

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password1')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        role = request.POST.get('user_type')

        if password != confirm_password:
            messages.error(request, "Your passwords didn't match!")
            return redirect('register.html')
        elif CustomUser.objects.filter(email=email):
            messages.error(request, f'{email} is already exists! Please try with another email!!')
        else:
            otp = ""
            for i in range(6):
                otp += str(random.randint(0, 9))

            my_user = CustomUser(username=username, email=email, password=password, name=name, phone=phone, city=city, role=role, otp=otp)
            my_user.set_password(password)
            my_user.save()
            subject = 'OTP Verification'
            message = f'Dear {my_user.name}, Your OTP is: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [my_user.email]
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, f'OTP sent successfully on {email}')
            return redirect('otp')
    return render(request, 'register.html')


def otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        if CustomUser.objects.filter(otp=input_otp):
            messages.success(request, 'Thank you for registering on iStreet!!!')
            return redirect('login')
        else:
            messages.error(request, 'OTP verification failed!!')
    return render(request, 'otp.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.role == 'user':
                login(request, user)
                log = ActivityLog(user=user, activity="login")
                log.save()
                return redirect('home')
            elif user.role == 'admin':
                login(request, user)
                log = ActivityLog(user=user, activity="login")
                log.save()
                return redirect('admins')
            else:
                login(request, user)
                log = ActivityLog(user=user, activity="login")
                log.save()
                return redirect('executive')
        elif not email or not password:
            messages.error(request, "Please enter email and password")
        else:
            failed_user = CustomUser.objects.get(email=email)
            if failed_user is not None:
                log = ActivityLog(user=failed_user, activity="login failed")
                log.save()
            messages.error(request, "Invalid Email or Password!!")
    return render(request, 'login.html')

@login_required
def home(request):
    activity = ActivityLog.objects.filter(user=request.user)
    login_list = ActivityLog.objects.filter(activity='login').filter(user=request.user).count()
    logout_list = ActivityLog.objects.filter(activity='logout').filter(user=request.user).count()
    login_failed = ActivityLog.objects.filter(activity='login failed').filter(user=request.user).count()

    activity_names = ['login', 'logout', 'login failed']
    activity_nums = [login_list, logout_list, login_failed]

    context = {'activity_names': activity_names, 'activity_nums': activity_nums, 'activity': activity}

    return render(request, 'home.html', context)

@login_required
def logout_page(request):
    log = ActivityLog(user=request.user, activity="logout")
    log.save()
    logout(request)
    messages.success(request, 'You are logged out successfully!')
    return redirect('login')

@login_required
def admin(request):
    activity = ActivityLog.objects.filter(user=request.user)
    user = CustomUser.objects.filter(role='user').count()
    admin = CustomUser.objects.filter(role='admin').count()
    executive = CustomUser.objects.filter(role='executive').count()
    total_users = (CustomUser.objects.filter(role='user').values('city').annotate(count=Count('id')))

    role_list = ['user', 'admin', 'executive']
    role_num = [user, admin, executive]
    cities = []
    users = []

    for user in total_users:
        cities.append(user['city'])
        users.append(user['count'])
        print(f"City: {user['city']}, User Count: {user['count']}")

    context = {'role_list': role_list, 'role_num': role_num, 'activity': activity, 'cities': cities, 'users': users}

    return render(request, 'admin.html', context)

@login_required
def executive(request):
    user = CustomUser.objects.filter(role='user').count()
    admin = CustomUser.objects.filter(role='admin').count()
    executive = CustomUser.objects.filter(role='executive').count()

    total_expenses = Department.objects.annotate(total_amount=Sum('expense__amount')).values('department_name', 'total_amount')

    department_name = []
    department_expense = []

    for entry in total_expenses:
        department_name.append(entry['department_name'])
        department_expense.append(entry['total_amount'])

    dept = Department.objects.all()
    dept_list = []
    emp_count = []
    for d in dept:
        emp = Employee.objects.filter(emp_department=d).count()
        emp_count.append(emp)
        dept_list.append(d.department_name)

    role_list = ['user', 'admin', 'executive']
    role_num = [user, admin, executive]

    activity = ActivityLog.objects.filter(user=request.user)
    context = {'activity': activity, 'dept_list': dept_list, 'emp_count': emp_count, 'department_name':department_name, 'department_expense':department_expense}

    return render(request, 'executive.html', context)

@login_required
def department(request):
    activity = ActivityLog.objects.filter(user=request.user)
    if request.method == 'POST':
        dept = request.POST.get('department')
        description = request.POST.get('description')
        location = request.POST.get('location')

        if not description:
            messages.error(request, "Please enter department name!")
        else:
            my_dept = Department(department_name=dept, description=description, location=location)
            my_dept.save()
            log = ActivityLog(user=request.user, activity='New Department Created')
            log.save()
            messages.success(request, "Department added successfully!")
            return redirect('dtable')
    return render(request, 'department.html', {'activity': activity})

@login_required
def user_role(request):
    if request.method == 'POST':
        urole = request.POST.get('role')

        if not urole:
            messages.error(request, "Please enter Role")
            return redirect('role')
        else:
            my_role = UserRole(role_name = urole)
            my_role.save()
            messages.success(request, "Role added successfully!")
            return redirect('roletable')
    return render(request, 'UserRole.html')

@login_required
def expenses(request):
    depart = Department.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        dept = request.POST.get('dept')
        desc = request.POST.get('description')
        depart1 = Department.objects.get(pk=dept)
        if not amount:
            messages.error(request, "Please enter the amount")
            return redirect('expense')
        else:
            my_expense = Expense(e_date=date, amount=amount, department=depart1, description=desc)
            my_expense.save()
            log = ActivityLog(user=request.user, activity='New Expenses Added')
            log.save()
            messages.success(request, "Expenses added successfully!")
            return redirect('extable')
    return render(request, 'expense.html', {'depart': depart})

@login_required
def employee(request):
    dp = Department.objects.all()
    myrole = UserRole.objects.all()
    if request.method == 'POST':
        ename = request.POST.get('emp')
        email = request.POST.get('email')
        edept = request.POST.get('dept')
        erole = request.POST.get('role')
        ecity = request.POST.get('city')
        dept1 = Department.objects.get(pk=edept)
        role1 = UserRole.objects.get(pk=erole)
        if not ename or not email:
            messages.error(request, "Please enter all fields")
            return redirect('employee')
        else:
            my_emp = Employee(emp_name=ename, emp_email=email, emp_department=dept1, emp_role= role1, emp_city=ecity)
            my_emp.save()
            log = ActivityLog(user=request.user, activity='New Employee Added')
            log.save()
            messages.success(request, "Employee added successfully!")
            return redirect('emp-table')
    return render(request, "employee.html", {'dp': dp, 'myrole': myrole})

@login_required
def dtable(request):
    department_list = Department.objects.all()
    return render(request, "DepartmentTable.html", {'department_list': department_list})

@login_required
def role_table(request):
    role_list = UserRole.objects.all()
    return render(request, 'RoleTable.html', {'role_list': role_list})

@login_required
def expense_table(request):
    expense_list = Expense.objects.all()
    return render(request, 'ExpenseTable.html', {'expense_list': expense_list})


@login_required
def emp_table(request):
    emp_list = Employee.objects.all()
    return render(request, 'EmpTable.html', {'emp_list': emp_list})


@login_required
def profile(request):
    profiles = CustomUser.objects.filter(email=request.user)
    activity = ActivityLog.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profiles': profiles, 'activity': activity})


@login_required
def activity(request):
    active = ActivityLog.objects.filter(user=request.user)
    admins = ActivityLog.objects.all()
    return render(request, 'activity.html', {'active': active, 'admins': admins})


@login_required
def all_users(request):
    users = CustomUser.objects.filter(role='user')
    return render(request, 'all-users.html', {'users': users})


@login_required
def all_admins(request):
    admins = CustomUser.objects.filter(role='admin')
    return render(request, 'all-admins.html', {'admins': admins})


@login_required
def all_executive(request):
    executives = CustomUser.objects.filter(role='executive')
    return render(request, 'all-executive.html', {'executives': executives})


def chart(request):
    total_users = (CustomUser.objects.filter(role='user').values('city').annotate(count=Count('id')))

    cities = []
    users = []

    for user in total_users:
        cities.append(user['city'])
        users.append(user['count'])
        print(f"City: {user['city']}, User Count: {user['count']}")

    context = {'cities': cities, 'users': users}
    return render(request, 'Chart.html', context)
