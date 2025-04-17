from django.contrib import admin

from . import models


admin.site.register(models.Review)
admin.site.register(models.Amenity)
admin.site.register(models.Apartment)
admin.site.register(models.Photo)