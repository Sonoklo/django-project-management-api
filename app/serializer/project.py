from rest_framework.serializers import ModelSerializer
from app.models.project import Project

class ProjectSerializer(ModelSerializer):
    
    class Meta:
        model = Project
        fields = ["title", "description", "status", "visibillity", "start_date", "due_date"] #due_date ???
    

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)  
        instance.visibillity = validated_data.get('visibillity', instance.visibillity)
        instance.due_date = validated_data.get('due_date', instance.due_date)  
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["project_id"] = instance.id
        representation["start_date"] = instance.start_date
        representation["organization"] = {"id": instance.organization.id, "slug":instance.organization.slug }
        representation["created_by"] = {"user_id": instance.created_by.id}

        return representation