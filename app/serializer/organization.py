from rest_framework.serializers import ModelSerializer
from app.models.organization import Organization

class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ["name", "description"]
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["slug"] =  instance.slug
        representation["owner"] = {"email": instance.owner.email,"user_id": instance.owner.id}
        return representation