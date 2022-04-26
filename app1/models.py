from distutils.command.upload import upload
from django.db import models

# Create your models here.
class data(models.Model):
    date = models.DateTimeField(auto_now = True)
    patient_name = models.TextField(max_length=35)
    age = models.IntegerField()
    temp = models.FloatField()
    cough = models.IntegerField()
    sore_throat = models.IntegerField()
    breathing = models.IntegerField()
    headache = models.IntegerField()
    image = models.ImageField(upload_to= 'image')
    result_from_xray = models.TextField(max_length=20,null=True,blank=True)
    result_from_symp = models.TextField(max_length=20,null=True,blank=True)



    def __str__(self):
        return self.patient_name


class contact(models.Model):
    name = models.TextField(max_length=20)
    email = models.EmailField()
    subject = models.TextField(max_length=30)
    message = models.TextField(max_length=100)

    def _str_(self):
        return self.subject