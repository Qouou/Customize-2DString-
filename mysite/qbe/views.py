from django.shortcuts import render

# Create your views here.
def qbe(request):
    # return HttpResponse("Hello, world. You're at the query index.")
    # return 30 data (100) 
    return render(request, 'qbe.html')