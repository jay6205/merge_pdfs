from django.urls import path
from .views import merge_pdfs

urlpatterns = [
    path('', merge_pdfs, name='merge_pdfs'),
]
