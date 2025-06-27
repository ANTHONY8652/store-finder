from .models import Store, Category
from rest_framework import serializers
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class StoreSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Store
        fields = [
            'id',
            'name',
            'slug',
            'address',
            'latitude',
            'longitude',
            'opening_hours',
            'is_active',
            'created_at',
            'updated_at',
            'owner',
            'category',
            'category_id'

        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'owner']