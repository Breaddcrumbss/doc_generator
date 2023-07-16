import pandas as pd
import os
import io
import random
import csv

from pathlib import Path
from docxtpl import DocxTemplate
from django.conf import settings
from .models import TemplateFile, GeneratedFile
from django.core.files.base import ContentFile

def generate_files(template_path, datafile, user, doc_name):      #these should be filepaths
    file = template_path.file.path
    file_path = settings.MEDIA_ROOT.joinpath(file)
    
    data_df = pd.read_csv(datafile, index_col=0, header=None).transpose()
    data_df.dropna(axis=0, thresh=1)
    for index, row in data_df.iterrows():
        # file_id = random.randint(0, 999)
        context = {}
        for column in data_df.columns:
            var = row[column]
            context[column] = var

        file_bytes = io.BytesIO()

        template = DocxTemplate(file_path)
        template.render(context)
        template.save(file_bytes)

        file_bytes.seek(0)
        name = f'{doc_name} | {template_path.name}'
        f = GeneratedFile.objects.create(name=name, created_by=user)     # to change name to smtg else
        f.file.save(f'{name}.docx', ContentFile(file_bytes.read()))

def get_vars(templates):        # writes a csv file as bytes
    all_vars = set()
    for template in templates:
        file_path = settings.MEDIA_ROOT.joinpath(template.file.path)
        doc = DocxTemplate(file_path)
        vars = doc.get_undeclared_template_variables()
        for var in vars:
            all_vars.add(var)
    
    df = pd.DataFrame(sorted(list(all_vars)))

    return df
