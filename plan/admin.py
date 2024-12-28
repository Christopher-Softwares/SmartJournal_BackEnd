from django.contrib import admin
from .models import Plan, UserBalance, UserPlan


# Register your models here.
admin.site.register(Plan)
admin.site.register(UserBalance)
admin.site.register(UserPlan)
