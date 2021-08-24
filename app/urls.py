from django.urls import path
from app import views
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Swagger API')

urlpatterns = [
    path('home/', views.home, name='home'),
    path('processGeneticFile', views.processGeneticFile, name='processGeneticFile'),
    path('generateGeneticReport', views.generateReport, name='generateGeneticReport'),
    path('processGeneticFileReport', views.processGeneticFileReport, name='processGeneticFileReport'),
    path('generateReport', views.generateReport, name='generateReport'),
    url(r'^$', schema_view)
]