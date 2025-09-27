from rest_framework import serializers
from .models import Ticket, TicketComment
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketCommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketComment
        fields = ['id', 'author', 'content', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), required=False, allow_null=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'priority', 'status', 'created_by', 'assigned_to', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'comments']
