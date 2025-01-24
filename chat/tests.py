from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from workspace.models import Workspace
from chat.models import Chat
from plan.models import Plan

User = get_user_model()

class ChatAPITests(APITestCase):
    def setUp(self):
        Plan.objects.create(name="free plan", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        Plan.objects.create(name="silver premium", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        Plan.objects.create(name="gold premium", price= 0.00, ai_access= False, duration= None, max_workspaces_count= 3, max_notes_count= 30, max_collaborator_count= 1)
        self.user = User.objects.create_user(email="testuser@example.com", password="password123")
        self.client.force_authenticate(user=self.user)

        self.other_user = User.objects.create_user(email="otheruser@example.com", password="password123")
        self.workspace = Workspace.objects.create(name="Test Workspace", owner=self.user)
        self.chat1 = Chat.objects.create(workspace=self.workspace, message="Hello", order=1, msg_type="client")
        self.chat2 = Chat.objects.create(workspace=self.workspace, message="Reply to Hello", order=2, msg_type="server", replied_to=self.chat1)

    def test_list_workspace_chats_success(self):
        response = self.client.get(f"/1/messages/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response['data']), 2)
        self.assertEqual(response['data'][0]['message'], "Hello")

    def test_list_workspace_chats_non_existent_workspace(self):
        response = self.client.get("/999/messages/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Workspace with this id does not exist.", response.data['message'])

    def test_new_prompt_success(self):
        response = self.client.post("/new_prompt/", {"workspace_id": self.workspace.id, "prompt": "New prompt message"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("reply", response.data)
        self.assertEqual(response.data['reply']['message'], "Reply to: New prompt message")

    def test_new_prompt_non_existent_workspace(self):
        response = self.client.post("/new_prompt/", {"workspace_id": 999, "prompt": "Invalid workspace"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Workspace not found or does not belong to you.", response.data['error'])

    def test_new_prompt_invalid_prompt(self):
        response = self.client.post("/new_prompt/", {"workspace_id": self.workspace.id, "prompt": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Prompt message should not be empty", response.data['prompt'])

    def test_new_prompt_workspace_does_not_belong_to_user(self):
        other_workspace = Workspace.objects.create(name="Other Workspace", owner=self.other_user)
        response = self.client.post("/new_prompt/", {"workspace_id": other_workspace.id, "prompt": "Forbidden access"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Workspace not found or does not belong to you.", response.data['error'])
