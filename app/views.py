from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import TemplateUploadForm
from .models import TemplateFile

# Create your views here.
def index(request):
    return render(request, 'app/index.html')


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


def generate(request):
    pass

def manage(request):

    template_list = TemplateFile.objects.all()

    return render(request, 'app/manage.html', {
        'templates': template_list
    })

def delete_template(request, id):
    template = TemplateFile.objects.get(pk=id)
    # template.delete()
    
    return render(request, 'app/delete.html', {
        'id': id
    })