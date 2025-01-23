from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from plan.models import Plan, UserBalance, UserPlan

User = get_user_model()

class PlanAPITest(APITestCase):
    def setUp(self):
        self.plan1 = Plan.objects.create(name="free plan", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        self.plan2 = Plan.objects.create(name="silver premium", price= 10.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        self.plan3 = Plan.objects.create(name="gold premium", price= 20.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)

        self.user = User.objects.create_user(
            password="password123", email="testuser@example.com"
        )
        self.client.force_authenticate(user=self.user)


        self.user.balance.balance = 50
        self.user.save()

    def test_assign_plan_success(self):
        response = self.client.post(
            "/plan/assign-plan/", 
            data={"plan_id": 2},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.balance.refresh_from_db()
        self.assertEqual(self.user.balance.balance, 40.0)
        self.assertTrue(UserPlan.objects.filter(user=self.user, plan=self.plan2).exists())

    def test_get_user_plans_success(self):
        response = self.client.get("/plan/user-plans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assign_plan_insufficient_balance(self):
        self.user.balance.balance = 5.0 
        self.user.save()

        response = self.client.post(
            "/plan/assign-plan/",
            data={"plan_id": self.plan2.id},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Insufficient balance.")

    def test_assign_plan_invalid_plan_id(self):
        response = self.client.post(
            "/plan/assign-plan/",  
            data={"plan_id": 999}, 
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

