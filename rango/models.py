# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):  # For Python 2, use __unicode__ too
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self): # For Python 2, use __unicode__ too
        return self.title

class Fish(models.Model):
    name = models.CharField(max_length=128, unique=True)
    fishType = models.CharField(max_length=128)
    description = models.CharField
    price = models.FloatField
    area = models.CharField
    sustainability = models.IntegerField(default=3)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='fish_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Fish, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128, unique=True)
    fish = models.ForeignKey(Fish)
    cost = models.FloatField(blank=True)
    time = models.FloatField
    serves = models.IntegerField(blank=True)
    avgRating = models.FloatField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='recipe_images', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(User)
    rating = models.FloatField
    comment = models.CharField
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return self.comment
    

class UserProfile(models.Model):
    # This line is requred- links UserProfile to a User model instance
    user = models.OneToOneField(User)

    # The additional attributes asked to be included
    # if using python 2.7 define __unicode__ too
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful
    def __str__(self):
        return self.user.username
