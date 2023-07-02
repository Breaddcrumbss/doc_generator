from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TemplateUploadForm, DocGenerateForm
from .models import TemplateFile, DataFile, GeneratedFile
from .utils import generate_files
from django.conf import settings
import os


# Create your views here.
def index(request):
    return render(request, 'app/index.html')

@login_required
def upload(request):
    if request.method == 'POST':
        template = TemplateUploadForm(request.POST, request.FILES)
        if template.is_valid():
            template.save()
            return HttpResponseRedirect(reverse('app:index'))

    else:
        form = TemplateUploadForm()

        return render(request, 'app/upload.html', {
            'form': form
        })

@login_required
def generate(request):
    templates = TemplateFile.objects.all()
    if request.method == 'POST':
        form = DocGenerateForm(templates, request.POST, request.FILES)
        if form.is_valid():
            temp_choices = form.cleaned_data.get('templates')
            datafile = form.cleaned_data.get('datafile')
            print(temp_choices)
            for temp in temp_choices:
                datafile.seek(0)
                temp_path = TemplateFile.objects.get(pk=temp).file.path
                print('before generate', datafile)
                generate_files(temp_path, datafile, request.user)
                print(temp, 'after generate')
            
            return HttpResponseRedirect(reverse('app:index'))
        else:
            return HttpResponse('not valid')
    
    
    form = DocGenerateForm(templates)
    
    return render(request, 'app/generate.html', {
        'form': form
    })

@login_required
def documents(request):
    if request.user.is_superuser:
        document_list = GeneratedFile.objects.all()
    
    else:
        username = request.user
        document_list = GeneratedFile.objects.filter(created_by=username)

    return render(request, 'app/documents.html', {
        'documents': document_list,
    })

@login_required
def doc_download(request, doc_id):
    doc = GeneratedFile.objects.get(pk=doc_id)
    with open(doc.file.path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
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
    template_list = TemplateFile.objects.all()

    return render(request, 'app/manage.html', {
        'templates': template_list
    })

@login_required
def delete_template(request, temp_id):
    template = TemplateFile.objects.get(pk=temp_id)
    template.delete()
    os.remove(os.path.join(settings.MEDIA_ROOT, template.file.name))
    
    return HttpResponseRedirect(reverse('app:manage'))

@login_required
def get_csv(request, id):
    pass