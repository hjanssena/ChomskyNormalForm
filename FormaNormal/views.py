from django.shortcuts import render

def mainView(request):
    if request.method == "POST":
        lenguaje = request.POST['lenguaje']
        print(lenguaje)
    context = {}
    return render(request, "new.html", context)
