from rest_framework import serializers
from plan.models import Plan, UserPlan, UserBalance
from rest_framework.validators import UniqueValidator


class AssignPlanSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

    def validate_plan_id(self, value):
        user = self.context["request"].user

        if UserPlan.objects.filter(user=user).exists() and UserPlan.objects.filter(user=user).name != "free plan":
            raise serializers.ValidationError("User already has a plan.")
        
        if not Plan.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid plan ID.")
        
        return value
class UserPlanSerializer(serializers.ModelSerializer):
    plan = serializers.StringRelatedField()
    class Meta:
        read_only_fields = ["start_date"]
        model = UserPlan
        fields = ["plan", "is_active", "start_date"]

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        read_only_fields = ["updated_at"]
        fields = "__all__"