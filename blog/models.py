from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE) #on delete of user delete author

    def __str__(self):
        return self.title #object name will be replace by the title
    
    #this will redirect the url to post-detail when the CreateView is submitted
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
