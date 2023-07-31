from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TemplateUploadForm, DocGenerateForm, DatafileDownload, LabelForm
from .models import TemplateFile, DataFile, GeneratedFile
from .utils import generate_files, get_vars
from django.conf import settings
import os
import io
import csv

# Create your views here.
def index(request):
    return render(request, 'app/index.html')

@login_required
def upload(request):
    if request.method == 'POST':
        labelform = LabelForm(request.POST)
        template = TemplateUploadForm(request.POST, request.FILES)
        if labelform.is_valid():
            labelform.save()
            messages.success(request, ('Group Added'))
            return HttpResponseRedirect(reverse('app:upload'))

        elif template.is_valid():
            template.save()
            return HttpResponseRedirect(reverse('app:index'))
        else:
            print(template.errors)
            messages.success(request, (template.errors))
            return HttpResponseRedirect(reverse('app:upload'))

    else:
        form = TemplateUploadForm()
        labelform = LabelForm()

        return render(request, 'app/upload.html', {
            'form': form,
            'labelform': labelform
        })

@login_required
def generate(request):
    templates = TemplateFile.objects.all()
    if request.method == 'POST':
        form = DocGenerateForm(templates, request.POST, request.FILES)
        if form.is_valid():
            temp_choices = form.cleaned_data.get('templates')
            datafile = form.cleaned_data.get('datafile')
            # name = form.cleaned_data.get('name')
            for temp in temp_choices:
                datafile.seek(0)
                temp_file = TemplateFile.objects.get(pk=temp)
                generate_files(temp_file, datafile, request.user)
            
            return HttpResponseRedirect(reverse('app:documents'))
        else:
            return HttpResponse('not valid')
    
    
    form = DocGenerateForm(templates)
    
    return render(request, 'app/generate.html', {
        'form': form
    })

@login_required
def documents(request):
    if request.user.is_staff:
        document_list = GeneratedFile.objects.all()
    
    else:
        username = request.user
        document_list = GeneratedFile.objects.filter(created_by=username)

    return render(request, 'app/documents.html', {
        'documents': document_list,
    })

@login_required
def doc_download(request, doc_id, template):
    if template == 1:
        doc = TemplateFile.objects.get(pk=doc_id)
    else:
        doc = GeneratedFile.objects.get(pk=doc_id)
    with open(doc.file.path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if template == 1:
            response['Content-Disposition'] = f'attachment; filename={doc.name} template.docx'
        else:
            response['Content-Disposition'] = f'attachment; filename={doc.name}.docx'
        return response

@login_required
def delete_document(request, doc_id):
    doc = GeneratedFile.objects.get(pk=doc_id)
    doc.delete()
    os.remove(os.path.join(settings.MEDIA_ROOT, doc.file.name))
    
    return HttpResponseRedirect(reverse('app:documents'))

@login_required
def delete_all_documents(request):
    user = request.user
    doc_list = GeneratedFile.objects.filter(created_by=user)
    for doc in doc_list:
        doc.delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, doc.file.name))
    
    return HttpResponseRedirect(reverse('app:documents'))

@login_required
def manage(request):
    template_list = sorted(TemplateFile.objects.all(), key=lambda x: x.name)
    superuser = request.user.is_superuser

    return render(request, 'app/manage.html', {
        'templates': template_list,
        'superuser': superuser
    })

@login_required
def delete_template(request, temp_id):
    template = TemplateFile.objects.get(pk=temp_id)
    template.delete()
    os.remove(os.path.join(settings.MEDIA_ROOT, template.file.name))
    
    return HttpResponseRedirect(reverse('app:manage'))

@login_required
def get_csv_all(request):
    template_list = TemplateFile.objects.all()
    vars_df = get_vars(template_list)
    
    with io.BytesIO() as buf:
        vars_df.to_csv(buf, index=False, header=False)
        buf.seek(0)
        response = HttpResponse(buf, content_type='txt/csv')
        response['Content-Disposition'] = 'attachment; filename=data_file.csv'
        return response

@login_required
def get_csv_byid(request, temp_id):
    template = [TemplateFile.objects.get(pk=temp_id)]       # List to allow for iteration in getvars function
    var_df = get_vars(template)

    with io.BytesIO() as buf:
        var_df.to_csv(buf, index=False, header=False)
        buf.seek(0)
        response = HttpResponse(buf, content_type='txt/csv')
        response['Content-Disposition'] = f'attachment; filename={template[0].name} data_file.csv'
        return response
    
@login_required
def get_csv_multi(request):
    templates = TemplateFile.objects.all()

    if request.method == "POST":
        form = DatafileDownload(templates, request.POST)
        if form.is_valid():
            templates_selected = form.cleaned_data.get('templates')
            if templates_selected:
                template_list = [TemplateFile.objects.get(pk=template_id) for template_id in templates_selected]
                vars_df = get_vars(template_list)
                
                with io.BytesIO() as buf:
                    vars_df.to_csv(buf, index=False, header=False)
                    buf.seek(0)
                    response = HttpResponse(buf, content_type='txt/csv')
                    response['Content-Disposition'] = 'attachment; filename=data_file.csv'
                    return response
        else:
            messages.success(request, ('Please select at least one template'))

            form = DatafileDownload(templates)
            return render(request, 'app/datafiles.html', {
                'form': form
            })
                


    else:
        form = DatafileDownload(templates)

        return render(request, 'app/datafiles.html', {
            'form': form
        })

