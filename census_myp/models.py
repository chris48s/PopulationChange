from django.db import models

#import fixture myp_superseded.json to populate
#DB with superseded mid year population estimates

class stat(models.Model):
	LACode = models.CharField(max_length=9)
	year = models.DateField('year')
	population = models.IntegerField(default=0)
