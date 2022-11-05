from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Place)
admin.site.register(Region)
admin.site.register(PlaceImage)
admin.site.register(PlaceTag)
admin.site.register(TagToPlace)

