from django.urls import path
from . import views

urlpatterns = [
    path('pqc', views.page_misconcept_pqc, name='Misconceptions pqc')
]