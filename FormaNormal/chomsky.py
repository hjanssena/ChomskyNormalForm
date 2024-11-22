from nltk import CFG

def parseLang(lenguaje):
    gramatica = CFG.fromstring(lenguaje)
    producciones = []
    for produccion in gramatica.productions():
        x = produccion.__str__().split(" -> ")
        producciones.append(x)
    return producciones

#LISTO
def eliminarEpsilon(producciones):
    for produccion in producciones:
        if produccion[1] == "'epsilon'":
            variable = produccion[0]
            producciones.remove(produccion)

            for prod in producciones:
                x = prod[1]
                while variable in x:
                    x = x.replace(variable, "", 1).strip().replace("  ", " ")
                    if [prod[0],x] not in producciones:
                        producciones.append([prod[0],x])
    return producciones

def eliminarUnitarios(producciones):
    for produccion in producciones:
        if " " not in produccion[1] and "'" not in produccion[1]:
            ubicacion = produccion[0]
            variable = produccion[1]
            producciones.remove(produccion)
            for prod in producciones:
                if variable in prod[0]:
                    if [ubicacion, prod[1]] not in producciones:
                        producciones.append([ubicacion, prod[1]])
    return producciones






lenguaje = """
 S -> A A C D
 A -> 'a'A'b' | 'epsilon'
 C -> 'a'C | 'a'
 D -> 'a'D'a' | 'b'D'b' | 'epsilon'
 """

producciones = parseLang(lenguaje)
producciones = eliminarEpsilon(producciones)
producciones = eliminarUnitarios(producciones)
print(producciones)