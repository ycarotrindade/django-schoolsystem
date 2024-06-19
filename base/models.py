from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=200,unique=True)
    grade = models.PositiveSmallIntegerField()
    cl = models.CharField(max_length=4)
    birth = models.DateField()
    score1 = models.DecimalField(max_digits=3,decimal_places=1,null=True,blank=True)
    score2 = models.DecimalField(max_digits=3,decimal_places=1,null=True,blank=True)
    score3 = models.DecimalField(max_digits=3,decimal_places=1,null=True,blank=True)
    STATUS_CHOICE = {
        'approved': 'APROVED',
        'failed': 'FAILED',
        'analysis': 'ANALYSIS',
        'undefined':'UNDEFINED',
    }
    status = models.CharField(max_length=20,choices=STATUS_CHOICE)
    