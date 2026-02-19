from rest_framework.serializers import ModelSerializer
from app.models.user import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "full_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)