from django.db import models
from django.contrib import messages
from django.core.validators import validate_email
from django.db.models.deletion import CASCADE
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['fname']) < 2 or not post_data['fname'].isalpha():
            errors['fname'] = "First name should be at least 2 characters; letters only."
        if len(post_data['lname']) < 2 or not post_data['lname'].isalpha():
            errors['lname'] = "Last name should be at least 2 characters; letters only."
        try:
            validate_email(post_data['email'])
        except:
            errors['email'] = "Please enter a valid email address."
        if len(post_data['password']) < 8:
            errors['password'] = 'Passwords should be at least 8 characters.'
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = "Passwords do not match."
        return errors


class User(models.Model):
    email = models.EmailField()
    fname = models.TextField()
    lname = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 3:
            errors['title'] = 'Wish must be at least 3 characters.'
        if len(post_data['desc']) < 3:
            errors['desc'] = 'Description must be at least 3 characters.'
        return errors

class Wish(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    granted = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, related_name='wishes_uploaded', on_delete=CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_wishes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()