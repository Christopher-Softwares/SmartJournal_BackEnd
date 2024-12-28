from rest_framework import serializers
from plan.models import Plan, UserPlan

class AssignPlanSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

    def validate_plan_id(self, value):
        # Ensure the plan exists
        if not Plan.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid plan ID.")
        return value

class UserPlanSerializer(serializers.ModelSerializer):
    plan = serializers.StringRelatedField()

    class Meta:
        model = UserPlan
        fields = ["plan", "is_active", "start_date", "end_date"]