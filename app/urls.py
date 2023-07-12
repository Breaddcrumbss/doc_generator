from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('generate/', views.generate, name='generate'),
    path('manage/', views.manage, name='manage'),
    path('delete_temp/<int:temp_id>/', views.delete_template, name='delete-template'),
    path('get_csv_all/', views.get_csv_all, name='get-csv-all'),
    path('get_csv/<int:temp_id>/', views.get_csv_byid, name='get-csv'),
    path('documents/', views.documents, name='documents'),
    path('download_doc/<int:doc_id>/', views.doc_download, name='doc-download'),
    path('delete_doc/<int:doc_id>/', views.delete_document, name='delete-doc'),
    path('delete_all_docs/', views.delete_all_documents, name='delete-doc-all')


]
