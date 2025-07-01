from .models import Store, Category
from rest_framework import serializers, permissions
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StoreSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    owner = serializers.StringRelatedField(read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews = serializers.Serializer

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
            'created_at',
            'updated_at',
            'owner',
            'category',
            'category_id',
            'average_rating',
            'reviews'

        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'owner']

    def averate_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)
    
    def get_reviews(self, obj):
        from review.serializers import ReviewSerializer
        return ReviewSerializer(obj.reviews.all(), many=True).data