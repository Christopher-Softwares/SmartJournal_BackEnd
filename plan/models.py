from django.db import models
from users.models import CustomUser
from datetime import datetime

class UserBalance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="balance")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.balance}"

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ai_access = models.BooleanField(default=False)
    duration = models.DurationField(null=True)
    max_workspaces_count = models.IntegerField(null=True)
    max_notes_count = models.IntegerField(null=True)
    max_collaborator_count = models.IntegerField(null=True)


    def __str__(self):
        return self.name


class UserPlan(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_plan")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan")
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_expired(self):
        if self.plan.name == "free plan":
            return None
        expiration_date = self.start_date + self.plan.duration 
        if expiration_date > datetime.now():
            return True
        return False
        
    @property
    def expiration_time(self):
        if self.plan.name == "free plan":
            return None
        return self.start_date + self.plan.duration
    
    @property
    def can_add_workspace(self):
        workspace_left = self.plan.max_workspaces_count - self.user.workspaces.count()
        if workspace_left > 0:
            return True
        return False

    @property
    def can_add_note(self, workspace):
        note_left = self.plan.max_notes_count - workspace.notes.count()
        if note_left > 0:
            return True
        return False
    
    @property
    def can_add_member(self, workspace, n):
        memeber_left = self.plan.max_collaborator_count - workspace.memebers.count() - n
        if memeber_left > 0:
            return True
        return False

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.plan.name}"

