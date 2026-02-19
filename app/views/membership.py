from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from app.views.organization import OrganizationBaseMixin
from rest_framework import status
from rest_framework.response import Response
from app.serializer.membership import MembershipSerializer
from app.views.utils import StandardResultsSetPagination
from app.models.organization import Organization
from app.models.membership import Membership
from app.models.user import User

class MembershipCreateAPIView(CreateAPIView, OrganizationBaseMixin):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        slug = self.kwargs['slug']
        user_id = self.kwargs['user_id']
        org = get_object_or_404(Organization, slug=slug)
        return Membership.objects.filter(organization=org, user_id=user_id)

    def get_object_org(self, slug):
        return get_object_or_404(Organization, slug=slug)
    
    def get(self,request, slug): #pagi
        members = Membership.objects.filter(organization=self.get_object_org(slug)).all()
        page = self.paginate_queryset(members)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        sr_members = self.get_serializer(members, many=True)
        return Response(sr_members.data, status=status.HTTP_200_OK)
    def post(self,request,slug):
        org = self.get_object_org(slug)
        self.check_organization_owner(request.user, org)
        user = User.objects.filter(id=request.data["user"]).first()
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="User id is out of range or incorrect ")
        member = Membership.objects.filter(user=request.data["user"],organization=org).first()
        if member:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Member is in organization you can`t create member twice")
        sr_member = MembershipSerializer(data=request.data)
        sr_member.is_valid(raise_exception=True)
        sr_member.save(organization=org)

        return Response(sr_member.data, status=status.HTTP_201_CREATED)
        
class MembershipRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, OrganizationBaseMixin):
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object_org(self, slug):
        return get_object_or_404(Organization, slug=slug)
    def get_object_member(self, org, user_id):
       return get_object_or_404(Membership,organization=org, user_id=user_id)
    
    def get(self,request,slug, user_id):
        org = self.get_object_org(slug)
        self.check_organization_owner(request.user, org)  
        member = self.get_object_member(org, user_id)
        sr_member = MembershipSerializer(member)
        return Response(sr_member.data)
    
    def patch(self, request, slug, user_id):
        org = self.get_object_org(slug)
        self.check_organization_owner(request.user, org)  
        membership = self.get_object_member(org, user_id)
        if membership.role == "owner":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        sr_member = MembershipSerializer(membership, data=request.data, partial=True)
        sr_member.is_valid(raise_exception=True)
        sr_member.save()
        
        return Response(sr_member.data)
    def delete(self, request, slug, user_id):
        org = self.get_object_org(slug)
        self.check_organization_owner(request.user, org)
        membership = self.get_object_member(org, user_id)
        if membership.role == "owner":
            return Response(status=status.HTTP_400_BAD_REQUEST)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)