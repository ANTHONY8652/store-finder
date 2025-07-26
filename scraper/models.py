from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    source_site = models.CharField(max_length=100)
    product_url = models.URLField(unique=True)
    search_term = models.CharField(max_length=255)
    #image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.source_site})"

# Create your models here.
