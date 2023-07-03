import pandas as pd
import os
import io
import random

from pathlib import Path
from docxtpl import DocxTemplate
from django.conf import settings
from .models import TemplateFile, GeneratedFile
from django.core.files.base import ContentFile

def generate_files(template_path, datafile, user):      #these should be filepaths
    file = template_path.file.path
    file_path = settings.MEDIA_ROOT.joinpath(file)
    
    data_df = pd.read_csv(datafile, index_col=0).transpose()
    data_df.dropna(axis=0, thresh=1)
    for index, row in data_df.iterrows():
        file_id = random.randint(0, 999)
        context = {}
        for column in data_df.columns:
            var = row[column]
            context[column] = var

        file_bytes = io.BytesIO()

        template = DocxTemplate(file_path)
        template.render(context)
        template.save(file_bytes)

        file_bytes.seek(0)
        f = GeneratedFile.objects.create(name=f'gen-test{template_path.name}{file_id}', created_by=user)     # to change name to smtg else
        f.file.save(f'gen-test{file_id}.docx', ContentFile(file_bytes.read()))