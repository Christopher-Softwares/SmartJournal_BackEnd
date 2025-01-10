from django.core.management.base import BaseCommand
from plan.models import Plan
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed the database with default plans"

    def handle(self, *args, **kwargs):
        plans = [
            {"name": "free plan", "price": 0.00, "ai_access": False, "duration": None, "max_workspaces_count": 3, "max_notes_count": 30, "max_collaborator_count": 1},
            {"name": "silver premium", "price": 9.99, "ai_access": True, "duration": timedelta(days=30), "max_workspaces_count": 5, "max_notes_count": 50, "max_collaborator_count": 5},
            {"name": "gold premium", "price": 19.99, "ai_access": True, "duration": timedelta(days=90), "max_workspaces_count": 10, "max_notes_count": 100, "max_collaborator_count": 10},
        ]
        for plan_data in plans:
            plan, created = Plan.objects.update_or_create(
                name=plan_data["name"],
                defaults=plan_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created plan: {plan.name}"))
            else:
                self.stdout.write(f"Plan {plan.name} already exists.")
