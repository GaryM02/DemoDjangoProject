from django.db import models
from profiles.models import Profile
from django.db.models import Q






STATUS = (
    (0,"uncompleted"),
    (1,"completed")
)
# Create your models here.
class Project(models.Model):
    vendor = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='vendor')
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='client')
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    duration = models.DurationField()
    startdate = models.DateField()
    completiondate = models.DateField()
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.IntegerField(choices=STATUS, default=0)
    updated = models.DateTimeField(auto_now=True)