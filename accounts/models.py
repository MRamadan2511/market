from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone



class UserRole(models.Model):
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.role


class UserType(models.Model):
    type =  models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type
    



class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField(blank=True, default='', unique=True)
    name        = models.CharField(max_length=255, blank=True, default='')

    is_active   = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login  = models.DateTimeField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    user_type   = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='user_type', blank=True, null=True)
    user_role   = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='user_role', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
    def __str__(self):
        return self.name or self.email.split('@')[0]




class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        customer_type = UserType.objects.get(type="Customer")
        return super().get_queryset(*args, **kwargs).filter(user_type=customer_type)


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.TextField()


class Customer(User):
    objects = CustomerManager()

    class Meta:
        proxy = True

    def get_base_type(self):
        # Perform the query here when needed
        return UserType.objects.get(type="Customer")
    

    def whisper(self):
        return "whisper"

    def get_profile(self):
        # Helper method to get the profile for this customer
        return self.customerprofile



class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        employee_type = UserType.objects.get(type="Employee")
        return super().get_queryset(*args, **kwargs).filter(user_type=employee_type)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.TextField()


class Employee(User):
    objects = EmployeeManager()

    class Meta:
        proxy = True

    def get_base_type(self):
        # Perform the query here when needed
        return UserType.objects.get(type="Employee")
    

    def get_profile(self):
        # Helper method to get the profile for this customer
        return self.employeeprofile
