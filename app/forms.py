from django import forms
from .models import TemplateFile, GeneratedFile

class TemplateUploadForm(forms.ModelForm):
    class Meta:
        model = TemplateFile
        fields = ['name', 'file']

class DocGenerateForm(forms.Form):
    def __init__(self, templates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        template_choices = [(template.id, template.name) for template in templates]
        self.fields['templates'] = forms.MultipleChoiceField(choices=template_choices, widget=forms.CheckboxSelectMultiple ,label='Choose Templates')
        self.fields['datafile'] = forms.FileField(label='Data File')

class DocDownloadForm(forms.Form):                 # In case batch download is required
    pass