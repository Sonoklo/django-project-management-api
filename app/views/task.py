from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView
from app.views.organization import OrganizationBaseMixin
from rest_framework import status
from rest_framework.response import Response
from app.serializer.task import TaskSerializer
from app.views.utils import StandardResultsSetPagination
from app.models.project import Project
from app.models.task import Task
from app.models.membership import Membership


    
class TaskCreateAPIView(CreateAPIView, OrganizationBaseMixin):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_object_project(self, id):
        project = get_object_or_404(Project, id=id)
        return project
    def get_object_member(self,org,user):
        member = get_object_or_404(Membership, organization=org, user=user)
        return member
    
    def get(self, request, project_id): #pagi
        project = self.get_object_project(project_id)
        self.check_organization_membership(request.user, project.organization)
        tasks = Task.objects.filter(project=project, deleted_at=None).all()
        if not tasks:
            return Response(data="No task is created", status=status.HTTP_404_NOT_FOUND)
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        sr_tasks = self.get_serializer(tasks, many=True)
        return Response(sr_tasks.data, status=status.HTTP_200_OK)
    
    def post(self, request, project_id):
        project = self.get_object_project(project_id)
        member = self.get_object_member(project.organization, request.user)
        allowed_roles = ['admin', 'owner', 'manager', 'developer']
        self.check_role_permission(member, allowed_roles)
        sr_task = TaskSerializer(data=request.data, context={'project': project})
        sr_task.is_valid(raise_exception=True)
        sr_task.save(project=project, reporter=request.user)
        return Response(sr_task.data, status=status.HTTP_201_CREATED)
    
class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, OrganizationBaseMixin):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        self.check_organization_membership(request.user, task.project.organization)
        if task.deleted_at:
            return Response(data="task not found", status=status.HTTP_404_NOT_FOUND)
        sr_task = TaskSerializer(task)
        return Response(sr_task.data, status=status.HTTP_200_OK)
    
    def patch(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        member = self.check_organization_membership(request.user, task.project.organization)
        if member.role == 'developer':
            if task.assignee != request.user and task.reporter != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        elif member.role == 'viewer':
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif member.role not in ['admin', 'owner', 'manager']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        sr_task = TaskSerializer(task, data=request.data, partial=True)
        sr_task.is_valid(raise_exception=True)
        sr_task.save()
        return Response(sr_task.data, status=status.HTTP_200_OK)

    def put(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        member = self.check_organization_membership(request.user, task.project.organization)
        
        if member.role not in ['admin', 'owner', 'manager']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        sr_task = TaskSerializer(task, data=request.data)
        sr_task.is_valid(raise_exception=True)
        sr_task.save()
        return Response(sr_task.data, status=status.HTTP_200_OK)
    
    def delete(self, request, task_id):
        task = Task.objects.filter(id=task_id).first()
        if task.reporter == request.user or task.assignee == request.user:
            task.status = "archived"
            task.save() 
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
class RestoreTaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request,task_id):
        task = Task.objects.filter(id=task_id).first()
        member = self.check_organization_membership(request.user, task.project.organization)
        if member.role not in ['admin', 'owner', 'manager'] and task.reporter != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        task.status = "todo"
        task.deleted_at = None
        task.save()
        sr_task = TaskSerializer(task)
        return Response(sr_task.data, status=status.HTTP_200_OK)