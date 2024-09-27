from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICE = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('executive', 'Executive')
    )
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.IntegerField(null=True)
    city = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=USER_TYPE_CHOICE, default='admin')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Department(models.Model):
    department_name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.department_name


class UserRole(models.Model):
    role_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.role_name


class Expense(models.Model):
    e_date = models.DateField()
    amount = models.FloatField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()


class Employee(models.Model):
    emp_name = models.CharField(max_length=255)
    emp_email = models.EmailField()
    emp_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    emp_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    emp_city = models.CharField(max_length=255)

    def __str__(self):
        return self.emp_name


class ActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)












