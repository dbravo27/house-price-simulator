from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def input_form_view(request):
    return render(request, 'input_form.html')


