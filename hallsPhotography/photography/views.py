from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def members(request):
    template = loader.get_template('myfirst.html')
    if request.user.is_authenticated:
        return HttpResponse(template.render())
    else:
        return HttpResponse("Bad Auth")
