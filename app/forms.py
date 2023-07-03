from django import forms
from .models import TemplateFile, GeneratedFile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, MultiField, Div, Field
from crispy_forms.bootstrap import InlineCheckboxes


class TemplateUploadForm(forms.ModelForm):
    class Meta:
        model = TemplateFile
        fields = ['name', 'file']
    
    helper = FormHelper()

class DocGenerateForm(forms.Form):
    def __init__(self, templates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        template_choices = [(template.id, template.name) for template in templates]
        self.fields['templates'] = forms.MultipleChoiceField(choices=template_choices, widget=forms.CheckboxSelectMultiple(attrs={}) ,label='Choose Templates')
        self.fields['datafile'] = forms.FileField(label='Data File')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            InlineCheckboxes('templates'),
            Field('datafile')
        )
        
        

class DocDownloadForm(forms.Form):                 # In case batch download is required
    pass