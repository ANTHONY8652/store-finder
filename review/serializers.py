from rest_framework import serializers
from .models import Review
from django.contrib.auth import get_user_model


user = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    store = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'store', 'user', 'comment', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
