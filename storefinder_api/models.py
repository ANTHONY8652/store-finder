from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

slug = models.SlugField(unique=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="stores")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Categories")
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    opening_hours = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)    
            slug = base_slug
            count = 1
            while Store.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)


# Create your models here.
