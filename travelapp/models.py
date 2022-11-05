from django.db import models

TRAVEL_TYPE = (
    ('A', 'ROCK'),
    ('B', 'ORANGE'),
    ('C', 'SUNSET'),
    ('D', 'PIG'),
    ('E', 'FLOWER')
)

PLACE_TYPE = (
    ('RESTAURANT', 'RESTAURANT'),
    ('CAFE', 'CAFE'),
)

# Create your models here.
class Region(models.Model):
    region_small = models.CharField(max_length=20, null=False)   # address [1]
    region_large = models.CharField(max_length=20, null=False)   # address [0]

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(null=True, default="")
    latitude = models.IntegerField(null=False)
    longtitude = models.IntegerField(null=False)
    region = models.ForeignKey(Region, verbose_name="region", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, verbose_name="place", on_delete=models.CASCADE)
    src = models.URLField(null=True, blank=True)
    index = models.IntegerField(null=True, default=1)
    
    def __str__(self):
        return self.src

class PlaceTag(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name

class TagToPlace(models.Model):
    place_id = models.ForeignKey(Place, verbose_name="place_id", on_delete=models.CASCADE)
    tag_id = models.ForeignKey(PlaceTag, verbose_name="tag_id", on_delete=models.CASCADE)
    def __str__(self):
        return self.name
