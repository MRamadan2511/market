from django.contrib import admin

from .models import User, UserRole, UserType, Customer, CustomerProfile,  Employee, EmployeeProfile

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(UserType)
admin.site.register(Customer)
admin.site.register(CustomerProfile)
admin.site.register(Employee)
admin.site.register(EmployeeProfile)