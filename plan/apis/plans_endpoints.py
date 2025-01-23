from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from plan.models import UserPlan, Plan
from plan.serializers import AssignPlanSerializer, UserPlanSerializer, BalanceSerializer
from plan.models import UserBalance
from django.shortcuts import get_object_or_404


class AssignPlanView(APIView):
    """
    valid plan IDs are: 1, 2, 3.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AssignPlanSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            plan_id = serializer.validated_data["plan_id"]
            plan = Plan.objects.get(id=plan_id)
            user = request.user

            if not getattr(user,"balance", None):
                return Response({"message": "User does not have balance relation, handle later with signal"})
            
            balance = getattr(user, "balance", None)
            if balance.balance  < plan.price:
                return Response({"message": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)
            
            UserPlan.objects.create(user=user, plan=plan)

            balance.balance -= plan.price
            balance.save()

            return Response({"message": f"Plan '{plan.name}' assigned successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPlansView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPlanSerializer
    def get(self, request):
        user_plans = UserPlan.objects.filter(user=request.user, is_active=True)
        serializer = self.serializer_class(user_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetUserBalanceView(APIView):
    serializer_class = BalanceSerializer
    authentication_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        balance = get_object_or_404(UserBalance, user=user)
        serializer = self.serializer_class(instance=balance)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)