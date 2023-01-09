from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def associationRules(request):
    return render(request, 'associationRule.html')

