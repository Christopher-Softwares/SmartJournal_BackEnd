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

    def get_queryset(self):
        workspace_id = self.kwargs.get('workspace_id')
        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            return None  
        return workspace.chats.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response(
                {"message": "Workspace with this id does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
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
                msg_type="client", 
            )

            reply_chat = Chat.objects.create(
                workspace=workspace,
                message=f"Reply to: {prompt_chat.message}",
                order=prompt_chat.order + 1,
                replied_to=prompt_chat,
                msg_type="server"
                )

            response_data = ChatSerializer(reply_chat).data
            return Response({"reply": response_data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
