from django.db import models
from workspace.models import Workspace

MSG_TYPE_CHOICE = [
    ('client', 'Client'),
    ('server', 'Server'),
]

class Chat(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='chats')
    replied_to = models.ForeignKey("Chat",on_delete=models.DO_NOTHING, related_name='replies', null=True, blank=True)
    order = models.IntegerField(null=False)
    message = models.TextField(max_length=2000)
    msg_type = models.CharField(choices=MSG_TYPE_CHOICE, null=False, blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content