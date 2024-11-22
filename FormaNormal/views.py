from django.shortcuts import render

def mainView(request):
    context = {}
    return render(request, "html", context)
