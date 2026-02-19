from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from app.views.membership import MembershipCreateAPIView, MembershipRetrieveUpdateDestroyAPIView
from app.views.user import UserRetrieveUpdateAPIView, AuthCreateAPIView
from app.views.organization import OrganizationCreateAPIView, OrganizationRetrieveUpdateDestroyAPIView
from app.views.project import ProjectRetrieveUpdateDestroyAPIView, ProjectsCreateAPIView
from app.views.task import TaskCreateAPIView, TaskRetrieveUpdateDestroyAPIView, RestoreTaskCreateAPIView

urlpatterns = [ 
    # Auth/User
    path('auth/register/', AuthCreateAPIView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('users/me/', UserRetrieveUpdateAPIView.as_view()),

    # Organization
    path('organizations/', OrganizationCreateAPIView.as_view() ),
    path('organizations/<slug:slug>/', OrganizationRetrieveUpdateDestroyAPIView.as_view()),

    # Membership
    path('organizations/<slug:slug>/members/', MembershipCreateAPIView.as_view()),
    path('organizations/<slug:slug>/members/<int:user_id>/', MembershipRetrieveUpdateDestroyAPIView.as_view()),

    # Project
    path('organizations/<slug:slug>/projects/', ProjectsCreateAPIView.as_view()),
    path('projects/<int:project_id>/', ProjectRetrieveUpdateDestroyAPIView.as_view()),

    # Task
    path('projects/<int:project_id>/tasks/', TaskCreateAPIView.as_view()),
    path('tasks/<int:task_id>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('tasks/<int:task_id>/restore/', RestoreTaskCreateAPIView.as_view())
]