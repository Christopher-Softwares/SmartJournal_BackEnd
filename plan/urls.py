from django.urls import path
from plan.views import AssignPlanView, UserPlansView, GetUserBalanceView

urlpatterns = [
    path('assign-plan/', AssignPlanView.as_view(), name='assign-plan'),
    path('user-plans/', UserPlansView.as_view(), name='user-plans'),
    path('get-user-balance/', GetUserBalanceView.as_view(), name='user-balance'),
]
