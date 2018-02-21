# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from rango.models import Category, Page, Fish, Recipe, Review
from rango.models import UserProfile


class PageAdmin (admin.ModelAdmin):
    list_display=('title', 'category', 'url')

# Adding this class to customise the admin interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
# update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(Fish)
admin.site.register(Recipe)
admin.site.register(Review)


