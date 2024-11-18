from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('individuals/', views.individual_all, name='individuals'),
    path('create-individual/', views.create_individual, name='create-individual'),
    # API
    path('api/create-individual/', views.create_individual_api, name='create-individual-api'),
    # HTMX Requests
    path('htmx/responsive-sitio/', views.sitio_htmx, name='sitio-htmx'),
    # PDF Downloadables
    path('individual-ids/', views.individual_ids_pdf, name='individual-ids')
]
