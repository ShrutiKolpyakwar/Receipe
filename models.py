from django.db import models

class Receipe(models.Model):
    receipe_name = models.CharField(max_length=255)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)  # Ensure upload_to is correct
