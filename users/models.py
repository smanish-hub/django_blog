from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()
        image=Image.open(self.image.path)

        if image.height>300 and image.width>300:
            image.thumbnail((300,300))
            image.save(self.image.path)

