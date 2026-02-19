from rest_framework.serializers import ModelSerializer
from app.models.membership import Membership

class MembershipSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ["user", "role", "organization"]
        extra_kwargs = {'organization': {'read_only': True}, }

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["member_id"] = instance.id
        representation["organization"] = {"id": instance.organization.id, "slug":instance.organization.slug }
        representation["user"] = {"user_id": instance.user.id}
        return representation