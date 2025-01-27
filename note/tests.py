from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.forms.models import model_to_dict
from note.models import Note, Tag
from workspace.models import Workspace
from note.serializers import TagSerializer
from users.models import CustomUser
from plan.models import Plan, UserPlan
import datetime as dt


class CreateNoteViewTests(APITestCase):
    
    def setUp(self):

        self.plan = Plan.objects.create(
            name="free plan", 
            price=0, 
            ai_access=True, 
            duration=dt.timedelta(days=100), 
            max_workspaces_count=20, 
            max_notes_count=100, 
            max_collaborator_count=100
        )

        self.user = CustomUser.objects.create_user(email="testuser@test.com", password="aA!12345678")
        
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            description="A workspace for testing",
            owner=self.user,
        )
        
        self.client = APIClient()
        self.url = reverse("create-note")
        
        self.valid_payload = {
            "title": "string",
            "description": "string",
            "workspace_id": self.workspace.id
            }
        
        self.invalid_payload = {
            "title": "hello",
            "description": "desc"
        }

    def test_post_valid_data(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_invalid_data(self):
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SaveNoteContentTests(APITestCase):
    def setUp(self):

        self.plan = Plan.objects.create(
            name="free plan", 
            price=0, 
            ai_access=True, 
            duration=dt.timedelta(days=100), 
            max_workspaces_count=20, 
            max_notes_count=100, 
            max_collaborator_count=100
        )

        self.user = CustomUser.objects.create_user(email="testuser@test.com", password="aA!12345678")
        
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            description="A workspace for testing",
            owner=self.user,
        )
        
        self.note = Note.objects.create(
            title="test note",
            description="note for testing",
            workspace=self.workspace
        )
        
        self.client = APIClient()
        self.url = reverse("save-note")

        self.valid_payload = {
            "note_id": self.note.id,
            "content": "new content"
        }
        
        self.invalid_payload = {
            "note_id": self.note.id + 1,
            "content": "bad request"
        }


    def test_put_unathorized(self):
        response = self.client.put(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_valid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_put_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, data=self.invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FilterNotesViewTests(APITestCase):
    
    def setUp(self):

        self.plan = Plan.objects.create(
            name="free plan", 
            price=0, 
            ai_access=True, 
            duration=dt.timedelta(days=100), 
            max_workspaces_count=20, 
            max_notes_count=100, 
            max_collaborator_count=100
        )

        self.user = CustomUser.objects.create_user(email="testuser@test.com", password="aA!12345678")
        self.user2 = CustomUser.objects.create_user(email="testuser2@test.com", password="aA!123456789")
        
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            description="A workspace for testing",
            owner=self.user,
        )
        
        self.workspace2 = Workspace.objects.create(
            name="test workspace 2",
            description="A workspace for testing",
            owner=self.user2,
        )
        
        self.workspace3 = Workspace.objects.create(
            name="test workspace 3",
            description="A workspace for testing",
            owner=self.user2,
        )
        
        self.workspace3.members.add(self.user)
        
        self.note1 = Note.objects.create(
            title="mine",
            description="note for testing",
            workspace=self.workspace
        )

        self.note2 = Note.objects.create(
            title="not mine",
            description="note for testing",
            workspace=self.workspace2
        )
        
        self.note3 = Note.objects.create(
            title="im a member",
            description="note for testing",
            workspace=self.workspace3
        )
        
        self.note4 = Note.objects.create(
            title="hello world",
            description="test",
            workspace=self.workspace
        )
        
        self.client = APIClient()
        self.url = reverse("filter-notes")


        self.valid_payload = {
            "title": "mine",
            "workspace_id": self.workspace.id
        }

        self.valid_payload2 = {
            "title": "member",
            "workspace_id": self.workspace3.id
        }
        
        self.invalid_payload = {
            "title": "not mine",
            "workspace_id": self.workspace2.id
        }
        
    
    def test_post_owner_filter(self):
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.url, data=self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # check the data
        self.assertEqual(response.json()["data"]["notes"][0]["note_id"], self.note1.id)
        
    
    def test_post_member_filter(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.url, data=self.valid_payload2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check the data
        self.assertEqual(response.json()["data"]["notes"][0]["note_id"], self.note3.id)
        
    
    def test_post_not_owner_or_member(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(self.url, data=self.invalid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetNoteContentTests(APITestCase):
    
    def setUp(self):
        
        self.plan = Plan.objects.create(
            name="free plan", 
            price=0, 
            ai_access=True, 
            duration=dt.timedelta(days=100), 
            max_workspaces_count=20, 
            max_notes_count=100, 
            max_collaborator_count=100
        )

        self.user = CustomUser.objects.create_user(email="testuser@test.com", password="aA!12345678")
        self.user2 = CustomUser.objects.create_user(email="testuser2@test.com", password="aA!123456789")
        
        self.workspace = Workspace.objects.create(
            name="Test Workspace",
            description="A workspace for testing",
            owner=self.user,
        )
        
        self.workspace2 = Workspace.objects.create(
            name="test workspace 2",
            description="A workspace for testing",
            owner=self.user2,
        )
        
        self.note1 = Note.objects.create(
            title="mine",
            description="note for testing",
            content="content1",
            workspace=self.workspace
        )

        self.note2 = Note.objects.create(
            title="not mine",
            description="note for testing",
            content="content2",
            workspace=self.workspace2
        )
        
        self.client = APIClient()
        self.valid_url = reverse("get-note-content", kwargs={"note_id": self.note1.id})
        self.invalid_url = reverse("get-note-content", kwargs={"note_id": self.note2.id})


        
    def test_get_my_note(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.valid_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.json()["data"]["content"], "content1")
    
    def test_get_others_note(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.invalid_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        