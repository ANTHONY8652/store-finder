from rest_framework import serializers
from .models import Review
from django.contrib.auth import get_user_model
from storefinder_api.models import Category, Store


user = get_user_model
store = Store

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'store', 'comment', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
