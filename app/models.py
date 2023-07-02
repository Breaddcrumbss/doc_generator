from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TemplateFile(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='files/templates', null=True)

    def __str__(self):
        return self.name
    
class GeneratedFile(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='files/generated', null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class DataFile(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='files/data', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    