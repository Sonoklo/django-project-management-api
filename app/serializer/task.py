from rest_framework.serializers import ModelSerializer
from app.models.task import Task

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status", "due_date"]
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["reporter"] = {"user_id": instance.reporter.id}
        if instance.assignee is not None:
            representation["assignee"] = {"user_id": instance.assignee.id}
        else:
            representation["assignee"] = None
        if instance.deleted_at is not None:
            representation["deleted_at"] = instance.deleted_at
        representation["project"] = {"id": instance.id, "organization":{"id": instance.project.organization.id, "slug":instance.project.organization.slug}, "created_by":{"user_id": instance.project.created_by.id} }

        return representation
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)  
        instance.priority = validated_data.get('priority', instance.priority)
        instance.due_date = validated_data.get('due_date', instance.due_date)  
        instance.assignee = validated_data.get('assignee', instance.assignee)
        instance.save()
        return instance