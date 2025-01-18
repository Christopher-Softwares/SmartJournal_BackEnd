from django.contrib import admin
from django.db import models
from django import forms
from .models import Plan, UserBalance, UserPlan

admin.site.register(Plan)
admin.site.register(UserBalance)
admin.site.register(UserPlan)
