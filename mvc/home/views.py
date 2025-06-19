from django.shortcuts import render

def page_home(request):
    """
    Render the home page.
    """
    return render(request, 'home/home.html')