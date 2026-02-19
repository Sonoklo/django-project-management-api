from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from app.views.organization import OrganizationBaseMixin
from rest_framework import status
from rest_framework.response import Response
from app.serializer.project import ProjectSerializer
from app.views.utils import StandardResultsSetPagination
from app.models.project import Project
from app.models.organization import Organization
from app.models.membership import Membership

class ProjectsCreateAPIView(CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_object_org(self, slug):
        return get_object_or_404(Organization, slug=slug)
    def get_object_member(self, member):
        return get_object_or_404(Membership, user=member)
    
    def get(self, request, slug):
        projects = Project.objects.filter(organization=self.get_object_org(slug), visibillity=True).all()
        if not projects:
            return Response(data="Projects have not created at that moment", status=status.HTTP_404_NOT_FOUND)
        page = self.paginate_queryset(projects)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        sr_project = self.get_serializer(projects, many=True)
        return Response(sr_project.data, status=status.HTTP_200_OK)
    
    def post(self, request, slug):
        org = self.get_object_org(slug)
        user = request.user
        member = self.get_object_member(user)
        if member.role != "admin":
            return Response(data="Only admin can create project", status=status.HTTP_403_FORBIDDEN)
        sr_project = ProjectSerializer(data=request.data)
        sr_project.is_valid(raise_exception=True)
        sr_project.save(organization=org, created_by=request.user)
        return Response(sr_project.data, status=status.HTTP_201_CREATED)

class ProjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, OrganizationBaseMixin):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object_member(self, user):
        return get_object_or_404(Membership, user=user)
    
    def get(self, request, project_id): #pagi
        project = Project.objects.filter(id=project_id).first()
        membership = self.check_organization_membership(request.user, project.organization)
        if not project.visibillity and membership.role == "viewer" and project.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        sr_projects = ProjectSerializer(project)
        return Response(sr_projects.data, status=status.HTTP_200_OK)
    
    def patch(self, request, project_id):
        member = self.get_object_member(request.user)
        project = Project.objects.filter(created_by=member.user, id=project_id).first()
        allowed_roles = ['admin', 'owner']
        if project.created_by == request.user:
            allowed_roles.append('manager')  
        self.check_role_permission(member, allowed_roles)
        sr_project = ProjectSerializer(project, data=request.data, partial=True)
        sr_project.is_valid(raise_exception=True)
        sr_project.save()
        return Response(sr_project.data, status=status.HTTP_200_OK)
    def delete(self, request, project_id):
        project = self.get_project(project_id)
        membership = self.check_organization_membership(request.user, project.organization)
        if membership.role not in ['admin', 'owner'] and project.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)    