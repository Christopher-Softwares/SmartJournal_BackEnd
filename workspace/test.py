from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from workspace.models import Workspace, Folder
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

    

class FolderViewsTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.plan = Plan.objects.create(name="free plan", price=0, ai_access=True, duration=None, max_notes_count=100, max_collaborator_count=100, max_workspaces_count=100)
        
        self.user = User.objects.create(email="testuser@test.com", password="aA!123456789")
        self.user2 = User.objects.create(email="testuser2@test.com", password="aA!123456789")
        
        self.workspace1 = Workspace.objects.create(
            name="test workspace",
            description="test desc",
            owner=self.user,
        )
        
        self.workspace2 = Workspace.objects.create(
            name="test workspace 2",
            description="test desc 2",
            owner=self.user2,
        )
        
        self.folder1 = Folder.objects.create(title="test folder", workspace=self.workspace1)
        self.folder2 = Folder.objects.create(title="test folder 2", workspace=self.workspace2)
        
    
    def test_create_folder_valid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("create-folder")
        
        valid_data = {
            "folder_name": "new folder",
            "workspace_id": self.workspace1.id,
        }
        
        response = self.client.post(url, valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_create_folder_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("create-folder")
        
        forbidden_data = {
            "folder_name": "new folder",
            "workspace_id": self.workspace2.id,
        }
        
        response = self.client.post(url, forbidden_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    
    def test_create_folder_invalid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("create-folder")
        
        invalid_data1 = {
            "name": "folder name",
            "workspace_id": self.workspace1.id,
        }
        
        invalid_data2 = {
            "folder_name": "new folder"
        }
        
        response1 = self.client.post(url, invalid_data1)
        response2 = self.client.post(url, invalid_data2)
        
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_update_folder_valid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("update-folder")
        
        valid_data = {
            "folder_id": self.folder1.id,
            "folder_name": "new name",
        }
        
        response = self.client.put(url, valid_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_update_folder_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("update-folder")
        
        forbidden_data = {
            "folder_id": self.folder2.id,
            "folder_name": "new name",
        }
        
        response = self.client.put(url, forbidden_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
    def test_update_folder_invalid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("update-folder")
        
        not_found_data = {
            "folder_id": self.folder1.id + 1000,
            "folder_name": "new name",
        }
        
        invalid_data = {
            "folder_name": "new name"
        }
        
        response1 = self.client.put(url, not_found_data)
        response2 = self.client.put(url, invalid_data)
        
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)        

    
    def test_delete_folder_valid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('delete-folder', kwargs={"pk": self.folder1.id})

        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    
    def test_delete_folder_forbidden(self):
        self.client.force_authenticate(user=self.user)
        forbidden_url = reverse('delete-folder', kwargs={"pk": self.folder2.id})

        response = self.client.delete(forbidden_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_delete_folder_invalid(self):
        self.client.force_authenticate(user=self.user)
        invalid_url1 = reverse('delete-folder', kwargs={"pk": self.folder1.id + 100})

        response1 = self.client.delete(invalid_url1)
        
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
