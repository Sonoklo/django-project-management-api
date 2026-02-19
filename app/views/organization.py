from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from app.serializer.organization import OrganizationSerializer
from app.views.utils import StandardResultsSetPagination
from app.models.organization import Organization
from app.models.membership import Membership

class OrganizationBaseMixin:
    def check_organization_membership(self, user, organization):
        membership = Membership.objects.filter(user=user, organization=organization).first()
        if not membership:
            return Response(status=status.HTTP_403_FORBIDDEN,data="You are not a member of organization")
        return membership
    def check_organization_owner(self, user, organization):
        if organization.owner != user:
            return Response(status=status.HTTP_403_FORBIDDEN, data="Only owner can do that")
    def check_role_permission(self, membership, allowed_roles):
        if membership.role not in allowed_roles:
            return Response(status=status.HTTP_403_FORBIDDEN,data="Your not allowed to do that")
    
class OrganizationCreateAPIView(CreateAPIView, OrganizationBaseMixin):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request): #pagi
        orgs = Organization.objects.filter(owner = request.user).all()
        page = self.paginate_queryset(orgs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        sr_org = self.get_serializer(orgs, many=True)
        return Response(sr_org.data)
    def post(self,request):
    
        sr_org = OrganizationSerializer(data=request.data)
        sr_org.is_valid(raise_exception=True)
        organization = sr_org.save(owner=request.user)
        membership_owner = Membership.objects.create(user=request.user, organization=organization, role="owner")
        membership_owner.save()
        return Response(sr_org.data, status=status.HTTP_201_CREATED)


class OrganizationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, OrganizationBaseMixin):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, slug, user):
        org = get_object_or_404(Organization, slug=slug)
        self.check_organization_membership(user, org)
        return org
    
    def get(self, request, slug):
        org = self.get_object(slug, request.user)
        sr_org = OrganizationSerializer(org)
        return Response(sr_org.data)
    
    def patch(self, request, slug):
        org = self.get_object(slug, request.user)
        self.check_organization_owner(request.user, org)
        sr_org = OrganizationSerializer(org, data=request.data, partial=True)
        sr_org.is_valid(raise_exception=True)
        sr_org.save()
        return Response(sr_org.data, status=status.HTTP_200_OK)
    
    def delete(self, request, slug):
        org = self.get_object(slug, request.user)
        if org is None: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        org.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    