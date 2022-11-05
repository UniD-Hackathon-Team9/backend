from django.db import models

# Create your models here.
class Region:
    name = models.CharField(max_length=20)
    region_large = models.CharField(max_length=20)
    latitude = models.DecimalField()

    def __str__(self):
        return self.name
        
class PlaceType:
    name = models.TextField()

    def __str__(self):
        return self.place_type


class Place:
    name = models.CharField(max_length=30)
    description = models.TextField()
    latitude = models.DecimalField()
    longtitude = models.DecimalField()
    place_type = models.ForeignKey(PlaceType, verbose_name="place_type")
    region = models.ForeignKey(Region, verbose_name="region", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
