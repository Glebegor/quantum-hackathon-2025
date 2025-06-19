from django.shortcuts import render

def page_misconcept_pqc(request):
    """
    Render the misconceptions page.
    """
    return render(request, 'misconcepts/misconceptions_pqc.html')