from django import forms
from .models import TemplateFile

class TemplateUploadForm(forms.ModelForm):
    class Meta:
        model = TemplateFile
        fields = ['name', 'file']