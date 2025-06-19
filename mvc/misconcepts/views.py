from django.shortcuts import render

# Create your views here.
def dkq_pqc_view(request):
    return render(request, 'misconcepts/dkq_pqc.html')

# Create your views here.
def diff_helman_view(request):
    return render(request, 'misconcepts/diff_helman.html')