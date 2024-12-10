from django.shortcuts import render, redirect
from .chomskyLib import *

def mainView(request):
    if request.method == "POST":
        lenguaje = request.POST['lenguaje']
        lenguaje = lenguaje.replace('"""', "").replace("\r", "").replace("...", "").replace("'''", "")
        producciones = parseLang(lenguaje)
        inicio = copiarProd(producciones)
        terminales = parseTerminales(producciones)
        producciones = eliminarEpsilon(producciones)
        primero = copiarProd(producciones)
        producciones = eliminarUnitarios(producciones)
        segundo = copiarProd(producciones)
        producciones = restringirTerminales(producciones, terminales)
        tercero = copiarProd(producciones)
        producciones = reducirReglas(producciones)
        cuarto = copiarProd(producciones)
        context = {"inicio": inicio, "primero": primero, "segundo": segundo, "tercero": tercero, "cuarto": cuarto}
        return render(request, "result.html", context)
        
    else:
        context = {}
        return render(request, "new.html", context)

def red(request):
    return redirect("fnc/")