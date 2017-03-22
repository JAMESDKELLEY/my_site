from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_user(self, post):
        errors = []
        isValid = True
    	if not EMAIL_REGEX.match(post.get('email')):
    		errors.append('Invalid email')
    		isValid = False
        if len(post.get('name')) == 0 or len(post.get('email')) == 0 or len(post.get('password')) == 0 or len(post.get('alias')) == 0:
            errors.append('Please fill in all fields')
            isValid = False
        if len(post.get('password')) < 8:
        	errors.append('Password must be at least 8 characters')
        	isValid = False
        if post.get('password') != post.get('password_confirmation'):
            isValid = False
        return (isValid, errors)

    def login_user(self, post):
        user = self.filter(email=post.get('email')).first()
        if user and bcrypt.hashpw(post.get('password').encode(), user.password.encode()) == user.password:
            return (True, user)
        return (False, None)

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    user = models.ForeignKey(User, related_name='quotes')
    quote = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites')
    quote = models.ForeignKey(Quote, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


