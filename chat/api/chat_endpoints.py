from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from chat.serializer import ChatSerializer, PromptSerializer
from workspace.models import Workspace
from chat.models import Chat

class ListWorkspaceChats(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        workspace = Workspace.objects.filter(id=id)
        if workspace:
            serializer  = self.serializer_class(workspace.chats.all(), many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"message": "Workspace with this id does not exists"}, status=status.HTTP_404_NOT_FOUND)
    
class NewPrompt(APIView):
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                workspace = Workspace.objects.get(id=request.data['workspace_id'], owner=request.user)
            except Workspace.DoesNotExist:
                return Response({"error": "Workspace not found or does not belong to you."}, status=status.HTTP_404_NOT_FOUND)

            last_order = workspace.chats.last().order if workspace.chats.exists() else 0

            prompt_chat = Chat.objects.create(
                workspace=workspace,
                message=serializer.validated_data['prompt'],
                order=last_order + 1,
                message_type="client", 
            )

            reply_chat = Chat.objects.create(
                workspace=workspace,
                message=f"Reply to: {prompt_chat.message}",
                order=prompt_chat.order + 1,
                replied_to=prompt_chat,
                message_type="server"
                )

            response_data = ChatSerializer(reply_chat).data
            return Response({"reply": response_data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
