from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.  
  
class ArtWork(models.Model):
    art_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    publish_date = models.DateField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    length = models.FloatField(blank = True)  # Assuming these are dimensions in standard units
    width = models.FloatField()
    height = models.FloatField()
    style = models.TextField(blank = True)
    material = models.TextField(blank = True)
    main_img =  models.ImageField(blank = True, null = True ,upload_to='artwork_images/')
    availability = models.TextField(default='In Stock')

    # Add any additional fields you may need

    def __str__(self):
        return f'{self.name} by {self.author.username}'
    class Meta:
        ordering = ['-date_created']  # Order by publish_date descending



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artwork')  # Ensure each artwork can only be in the wishlist once per user

    def __str__(self):
        return f'{self.user.username} - {self.artwork.name}'



class ArtworkImage(models.Model):
    artwork = models.ForeignKey(ArtWork, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artwork_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artwork = models.ForeignKey(ArtWork, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artwork')  # Ensure each artwork can only be in the cart once per user

    def __str__(self):
        return f'{self.user.username} - {self.artwork.name}'