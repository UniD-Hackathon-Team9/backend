from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=20)
    region_large = models.CharField(max_length=20)
    latitude = models.IntegerField()
    longtitude = models.IntegerField()

    def __str__(self):
        return self.name

class PlaceType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    latitude = models.IntegerField()
    longtitude = models.IntegerField()
    place_type = models.ForeignKey(PlaceType, verbose_name="place_type", on_delete=models.CASCADE)
    region = models.ForeignKey(Region, verbose_name="region", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
