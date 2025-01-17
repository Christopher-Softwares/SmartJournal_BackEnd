from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from workspace.models import Workspace
from plan.models import Plan
from users.models import CustomUser

User = CustomUser

class WorkspaceViewSetTests(APITestCase):
    def setUp(self):
        Plan.objects.create(name="free plan", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        Plan.objects.create(name="silver premium", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        Plan.objects.create(name="gold premium", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        self.user = User.objects.create_user(email="testuser@example.com", password="password123")
        self.user.save()
        self.user_no_plan = User.objects.create_user(email="noplanuser@example.com", password="password123")
        self.user_no_plan.save()
        self.user1 = User.objects.create_user(email="testuser1@example.com", password="password123")
        self.user1.save()

        self.workspace_data = { 
            "name": "Test Workspace",
            "description": "This is a test workspace",
            "owner": self.user.id,
            "members": [self.user.email],
        }
        self.workspace_data1 = { 
            "name": "Test Workspace1",
            "description": "This is a test workspace",
            "owner": self.user1.id,
            "members": [self.user1.email],
        }
        self.workspace_data2 = { 
            "name": "Test Workspace2",
            "description": "This is a test workspace",
            "owner": self.user1.id,
            "members": [self.user1.email],
        }
        self.workspace_data3 = { 
            "name": "Test Workspace3",
            "description": "This is a test workspace",
            "owner": self.user1.id,
            "members": [self.user1.email],
        }
        self.workspace_data4 = { 
            "name": "Test Workspace4",
            "description": "This is a test workspace",
            "owner": self.user1.id,
            "members": [self.user1.email],
        }

    def test_create_workspace_authenticated_user_with_valid_plan(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/workspace/workspaces/", self.workspace_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test Workspace")

    def test_retrieve_workspace_details(self):
        self.client.force_authenticate(user=self.user)
        workspace = Workspace.objects.create(name="Test Workspace", owner=self.user)
        response = self.client.get(f"/workspace/workspaces/{workspace.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Workspace")

    def test_create_workspace_unauthenticated_user(self):
        response = self.client.post("/workspace/workspaces/", self.workspace_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_workspace_user_without_valid_plan(self):
        self.client.force_authenticate(user=self.user_no_plan)
        response = self.client.post("/workspace/workspaces/", self.workspace_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_workspace_more_than_limitaion(self):
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.post("/workspace/workspaces/", self.workspace_data1)
        response2 = self.client.post("/workspace/workspaces/", self.workspace_data2)
        response3 = self.client.post("/workspace/workspaces/", self.workspace_data3)
        response4 = self.client.post("/workspace/workspaces/", self.workspace_data4)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)               
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)               
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)               
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)               