from django.urls import path
from .views import dkq_pqc_view, diff_helman_view

urlpatterns = [
    path('dkq_pqc', dkq_pqc_view, name='misconcepts_dkq_pqc_view'),
    path('diff_helman', diff_helman_view, name='misconcepts_diff_helman_view'),
]
