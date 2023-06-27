from django.db import models

# Create your models here.
class TemplateFile(models.Model):
    name = models.CharField(max_length=500)
    file = models.FileField(upload_to='files/templates', null=True)

    def __str__(self):
        return self.name