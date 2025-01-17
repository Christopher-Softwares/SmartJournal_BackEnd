from django.http import JsonResponse
from rest_framework import status
from plan.models import Plan, UserPlan


class CheckPlanExpiration:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user
        plan = getattr(user, 'user_plan', None)               
        backup_plan = Plan.objects.get(name="free plan")
        
        if not plan:
            UserPlan.objects.create(
                    plan = backup_plan,
                    user = user,
            )
            print("user had no plan")

        if plan.is_expired:
            user.user_plan.delete()
            
            UserPlan.objects.create(
                    plan = backup_plan,
                    user = user,
            )
            return JsonResponse(
                {
                    "message": "User plan has expired."
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

    
        response = self.get_response(request)
        
        return response
