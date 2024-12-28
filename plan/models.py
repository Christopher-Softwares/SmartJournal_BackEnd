from django.db import models
from users.models import CustomUser


class UserBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="balance")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"

class Plan(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    features = models.JSONField(default=dict)  
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserPlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="plans")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="user_plans")
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
