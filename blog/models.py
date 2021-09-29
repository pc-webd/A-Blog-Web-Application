from typing import KeysView
from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
from django.conf import settings
from django.shortcuts import reverse

class BlogModel(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    content=FroalaField()
    slug=AutoSlugField(populate_from='title')
    image=models.ImageField(upload_to='blog')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model): 
    blog = models.ForeignKey(BlogModel,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.blog) 