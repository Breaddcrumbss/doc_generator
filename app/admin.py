from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TemplateFile)
admin.site.register(GeneratedFile)
admin.site.register(GroupLabel)
admin.site.register(DataFile)