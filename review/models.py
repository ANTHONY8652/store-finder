from django.db import models
from storefinder_api.models import Store
from django.contrib.auth import get_user_model

class Review(models.Model):
    store = models.ForeignKey("Store", on_delete=models.CASCADE, related_name='stores')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='users')
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField() #1 to 5 or 10 to be decuded baadae
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("store", "user") # ! more than 1 Review per store per user
        ordering = ["-created_at"]

    def __str___(self):
        return f"{self.user} rated {self.store} - {self.rating}/5"

# Create your models here.
