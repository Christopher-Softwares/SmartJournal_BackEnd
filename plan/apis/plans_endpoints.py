from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from plan.models import UserPlan, Plan
from plan.serializers import AssignPlanSerializer, UserPlanSerializer


class AssignPlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssignPlanSerializer(data=request.data)
        if serializer.is_valid():
            plan_id = serializer.validated_data["plan_id"]
            plan = Plan.objects.get(id=plan_id)
            
            # Check user balance
            if request.user.balance.balance < plan.price:
                return Response({"message": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

            # Deduct balance
            user_balance = request.user.balance
            user_balance.balance -= plan.price
            user_balance.save()

            # Assign the plan
            UserPlan.objects.create(user=request.user, plan=plan)

            return Response({"message": f"Plan '{plan.name}' assigned successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPlansView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_plans = UserPlan.objects.filter(user=request.user, is_active=True)
        serializer = UserPlanSerializer(user_plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)