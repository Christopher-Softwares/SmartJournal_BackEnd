from django.contrib import admin
from plan.models import Plan, UserPlan
from plan.models import UserBalance

admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(UserBalance)