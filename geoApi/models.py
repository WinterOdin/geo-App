from django.db import models

# Create your models here.
class Location(models.Model):

    ip = models.CharField(max_length=15)
    type = models.CharField(max_length=6)
    latitude = models.FloatField()# decimal field wont work 
    longitude = models.FloatField()
    continent_code = models.CharField(max_length=2)
    continent_name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=10)
    country_name = models.CharField(max_length=70)
    region_code = models.CharField(max_length=10)
    region_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)



    def __str__(self):
        return str(self.ip)
