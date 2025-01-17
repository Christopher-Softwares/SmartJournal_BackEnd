from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from plan.models import UserBalance, UserPlan, Plan


@receiver(post_save, sender=CustomUser)
def assign_default_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(user=instance, balance=0)
        print(f"balance created for new user {instance}")

@receiver(post_save, sender=CustomUser)
def assign_default_plan(sender, instance, created, **kwargs):
    if created:
        try:
            plan = Plan.objects.get(name="free plan")
        except CustomUser.DoesNotExist:
            print("the plan does not exist")

        UserPlan.objects.create(user=instance, plan=plan)
        print(f"default plan assgined for {instance}")